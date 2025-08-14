from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Check service status",
    status_code=status.HTTP_200_OK,
)
def health_check():
    """
    Check service status
    """
    return {"status": "ok"}
