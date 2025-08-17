from fastapi import APIRouter, status

from app.schemas.response import ResponseBase

router = APIRouter()


@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Check service status",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase,
)
def health_check():
    """
    Check service status
    """
    return ResponseBase(success=True, message="Server up")
