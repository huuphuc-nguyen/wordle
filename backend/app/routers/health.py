"""Health route — simple ping to confirm the server is running."""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/health")
def health():
    """Returns 200 with a status flag — used by load balancers and monitoring."""
    return {"status": "ok"}
