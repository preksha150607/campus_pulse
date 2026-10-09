"""CampusPulse Serverless API — Starlette ASGI entry point.

Serves:
  POST /api/triage   — Multimodal incident triage (AI + deterministic rules)
  GET  /api/health   — Liveness probe
  GET  /             — Static HTML frontend (public/)

Security controls:
  - Rate-limit: max 30 requests per IP per minute (in-memory, resets on cold start)
  - Input size guard: JSON body ≤ 4 MB, base64 image ≤ 3 MB
  - Security response headers (X-Content-Type-Options, X-Frame-Options, CSP)
  - CORS: open for demo; restrict in production via ALLOWED_ORIGINS env var
"""
import base64
import collections
import os
import sys
import time
from typing import Deque

# ---------------------------------------------------------------------------
# Ensure triage.py in repo root is importable from api/ sub-directory
# ---------------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from triage import DEFAULT_MODEL, triage

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_BODY_BYTES = 4 * 1024 * 1024       # 4 MB
MAX_IMAGE_B64_BYTES = 3 * 1024 * 1024  # 3 MB (encoded)
RATE_LIMIT = 30                         # requests per minute per IP
RATE_WINDOW = 60                        # seconds

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

DEFAULT_PLACES = [
    "Main Gate & Bus Bay",
    "Academic Block",
    "Computer Labs",
    "Library",
    "Cafeteria",
    "Auditorium",
    "Medical Centre",
    "Girls Hostel",
    "Boys Hostel",
    "Sports Ground & Gym",
]

# ---------------------------------------------------------------------------
# In-memory rate limiter (per IP, sliding window)
# ---------------------------------------------------------------------------
_rate_store: dict[str, Deque[float]] = collections.defaultdict(collections.deque)


def _is_rate_limited(ip: str) -> bool:
    """Returns True if *ip* has exceeded RATE_LIMIT requests within RATE_WINDOW seconds."""
    now = time.monotonic()
    dq: Deque[float] = _rate_store[ip]
    # Purge stale entries
    while dq and now - dq[0] > RATE_WINDOW:
        dq.popleft()
    if len(dq) >= RATE_LIMIT:
        return True
    dq.append(now)
    return False


def _security_headers(response: Response) -> Response:
    """Attach common security headers to a response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com; "
        "font-src https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self';"
    )
    return response


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

async def health(request: Request) -> JSONResponse:
    """Liveness probe — returns 200 OK with basic metadata."""
    return _security_headers(JSONResponse({
        "status": "ok",
        "service": "CampusPulse Triage API",
        "version": "2.0.0",
    }))


async def handle_triage(request: Request) -> JSONResponse:
    """
    POST /api/triage

    Request body (JSON):
        text        str  — Incident description (any supported language)
        image       str  — Base64-encoded photo (optional, with or without data-URI prefix)
        mime        str  — MIME type of image (default: image/jpeg)
        places      list — Campus place names (optional, defaults to university list)
        api_key     str  — Gemini API key (optional if set in env)
        model       str  — Gemini model ID (optional)
        use_ai      bool — Whether to invoke Gemini (default: True)

    Returns:
        200 — Triage result dict
        400 — Bad request (malformed JSON / oversized payload)
        429 — Rate limit exceeded
        500 — Internal triage failure
    """
    # --- Rate limiting ---
    client_ip = request.client.host if request.client else "unknown"
    if _is_rate_limited(client_ip):
        return _security_headers(JSONResponse(
            {"error": "Rate limit exceeded. Please wait before retrying.", "code": "RATE_LIMITED"},
            status_code=429,
            headers={"Retry-After": str(RATE_WINDOW)},
        ))

    # --- Body size guard ---
    body = await request.body()
    if len(body) > MAX_BODY_BYTES:
        return _security_headers(JSONResponse(
            {"error": f"Request body exceeds {MAX_BODY_BYTES // 1024 // 1024} MB limit.", "code": "PAYLOAD_TOO_LARGE"},
            status_code=400,
        ))

    try:
        data = await request.json()
    except Exception:
        return _security_headers(JSONResponse(
            {"error": "Invalid JSON payload.", "code": "INVALID_JSON"},
            status_code=400,
        ))

    text: str = data.get("text", "")
    image_b64: str = data.get("image", "")
    mime: str = data.get("mime", "image/jpeg")
    places = data.get("places") or DEFAULT_PLACES
    api_key: str = data.get("api_key") or os.getenv("GEMINI_API_KEY", "")
    model: str = data.get("model") or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    use_ai: bool = bool(data.get("use_ai", True))

    # --- Image decoding ---
    image_bytes = None
    if image_b64:
        if len(image_b64.encode()) > MAX_IMAGE_B64_BYTES:
            return _security_headers(JSONResponse(
                {"error": "Image exceeds 3 MB limit.", "code": "IMAGE_TOO_LARGE"},
                status_code=400,
            ))
        try:
            raw = image_b64.split(",", 1)[1] if "," in image_b64 else image_b64
            image_bytes = base64.b64decode(raw)
        except Exception as exc:
            return _security_headers(JSONResponse(
                {"error": f"Invalid base64 image: {exc}", "code": "INVALID_IMAGE"},
                status_code=400,
            ))

    # --- Triage execution ---
    try:
        result = triage(
            text=text,
            image=image_bytes,
            mime=mime,
            places=places,
            api_key=api_key or None,
            model=model,
            use_ai=use_ai,
        )
        return _security_headers(JSONResponse(result))
    except Exception as exc:
        return _security_headers(JSONResponse(
            {"error": f"Triage engine failure: {exc}", "code": "TRIAGE_ERROR"},
            status_code=500,
        ))


# ---------------------------------------------------------------------------
# Application assembly
# ---------------------------------------------------------------------------
routes = [
    Route("/api/health", health, methods=["GET"]),
    Route("/api/triage", handle_triage, methods=["POST"]),
]

PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
if os.path.isdir(PUBLIC_DIR):
    routes.append(Mount("/", app=StaticFiles(directory=PUBLIC_DIR, html=True), name="static"))

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Authorization"],
    )
]

app = Starlette(debug=False, routes=routes, middleware=middleware)
