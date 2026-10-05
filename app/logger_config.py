import logging
import sys

from app.settings import settings

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("fastapi_app")

    logger.setLevel(
        logging.DEBUG if settings.debug else logging.INFO
    )

    formatter = logging.Formatter(
        fmt=(
            "LOG:      %(asctime)s "
            "| %(levelname)s "
            "| %(filename)s:%(lineno)d "
            "| %(message)s"
        ),
        datefmt="%y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


logger = setup_logging()
