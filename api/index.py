import base64
import os
import sys

# Add root directory to sys.path so triage.py can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from triage import DEFAULT_MODEL, triage

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


async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "CampusPulse API"})


async def handle_triage(request: Request) -> JSONResponse:
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)

    text = data.get("text", "")
    image_b64 = data.get("image")
    mime = data.get("mime", "image/jpeg")
    places = data.get("places") or DEFAULT_PLACES
    api_key = data.get("api_key") or os.getenv("GEMINI_API_KEY", "")
    model = data.get("model") or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    use_ai = data.get("use_ai", True)

    image_bytes = None
    if image_b64:
        try:
            if "," in image_b64:
                image_b64 = image_b64.split(",", 1)[1]
            image_bytes = base64.b64decode(image_b64)
        except Exception as e:
            return JSONResponse({"error": f"Invalid base64 image: {e}"}, status_code=400)

    try:
        result = triage(
            text=text,
            image=image_bytes,
            mime=mime,
            places=places,
            api_key=api_key if api_key else None,
            model=model,
            use_ai=bool(use_ai),
        )
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": f"Triage failed: {str(e)}"}, status_code=500)


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
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = Starlette(debug=False, routes=routes, middleware=middleware)
