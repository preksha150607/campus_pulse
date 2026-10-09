"""pytest configuration for CampusPulse test suite.

Ensures stdout uses UTF-8 to safely print multilingual characters on all platforms.
"""
import sys


def pytest_configure(config):
    """Reconfigure stdout/stderr to UTF-8 for multilingual test output."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
