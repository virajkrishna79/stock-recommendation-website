"""API package initialization.

Exports blueprints for external imports.
"""

try:
    from backend.api.routes import main_bp, api_bp  # type: ignore
except Exception:  # pragma: no cover - fallback when running from backend cwd
    from api.routes import main_bp, api_bp  # type: ignore

__all__ = ["main_bp", "api_bp"]
