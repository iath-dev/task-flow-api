from loguru import logger
import sys

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

logger.remove()  # Quita el handler por defecto
logger.add(
    sys.stdout,
    format=log_format,
    level="INFO",  # Cambia a INFO o WARNING en producción
)

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    format="log_format",
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)
