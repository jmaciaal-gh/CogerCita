"""Logging setup utilities."""

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure a predictable logger format for diagnostics."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
