"""Simple helper to wait for the database to be ready before launching the app."""
import os
import time
import logging

from sqlalchemy import create_engine

logger = logging.getLogger("wait_for_db")


def wait_for_database(url: str, timeout: int = 60, interval: int = 1) -> None:
    """Try to connect repeatedly until timeout seconds have passed.

    Raises a RuntimeError if unable to connect within the timeout.
    """
    engine = create_engine(url)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with engine.connect():
                logger.info("Database is available: %s", url)
                return
        except Exception as exc:
            logger.debug("Database not ready yet: %s", exc)
            time.sleep(interval)
    raise RuntimeError(f"Could not connect to database within {timeout} seconds: {url}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medbridge.db")
    try:
        wait_for_database(DATABASE_URL, timeout=60, interval=1)
    except RuntimeError as exc:
        logger.error("%s", exc)
        raise
