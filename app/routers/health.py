from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def live() -> dict:
    return {"status": "live"}


@router.get("/ready")
def ready() -> dict:
    return {"status": "ready"}
