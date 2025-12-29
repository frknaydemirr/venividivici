import logging
import os
from pathlib import Path
from typing import Any, Optional

from sanic.log import LOGGING_CONFIG_DEFAULTS

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_MAX_BYTES = 5 * 1024 * 1024
DEFAULT_BACKUP_COUNT = 5


def _clone(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _clone(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clone(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_clone(item) for item in value)
    if isinstance(value, set):
        return {_clone(item) for item in value}
    return value


def _sanitize_app_name(app_name: Optional[str]) -> str:
    safe_name = (app_name or "venividivici").strip().lower().replace(" ", "_")
    return safe_name or "app"


def _parse_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _resolve_log_level(raw_level: str) -> str:
    level = getattr(logging, (raw_level or DEFAULT_LOG_LEVEL).upper(), logging.INFO)
    return logging.getLevelName(level)


def build_log_config(app_name: Optional[str] = None) -> dict:
    """Create a logging configuration dict with file handlers for Sanic."""

    config = _clone(LOGGING_CONFIG_DEFAULTS)

    log_dir = Path(os.getenv("LOG_DIR", os.path.join(os.getcwd(), "logs")))
    log_dir.mkdir(parents=True, exist_ok=True)

    max_bytes = _parse_int(os.getenv("LOG_MAX_BYTES"), DEFAULT_MAX_BYTES)
    backup_count = _parse_int(os.getenv("LOG_BACKUP_COUNT"), DEFAULT_BACKUP_COUNT)
    log_level = _resolve_log_level(os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL))
    safe_name = _sanitize_app_name(app_name)

    app_log_path = str(log_dir / f"{safe_name}.log")
    error_log_path = str(log_dir / f"{safe_name}_error.log")
    access_log_path = str(log_dir / f"{safe_name}_access.log")

    config["handlers"]["app_file"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "formatter": "generic",
        "level": log_level,
        "filename": app_log_path,
        "maxBytes": max_bytes,
        "backupCount": backup_count,
        "encoding": "utf-8",
    }

    config["handlers"]["error_file"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "formatter": "generic",
        "level": "ERROR",
        "filename": error_log_path,
        "maxBytes": max_bytes,
        "backupCount": backup_count,
        "encoding": "utf-8",
    }

    config["handlers"]["access_file"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "formatter": "access",
        "level": log_level,
        "filename": access_log_path,
        "maxBytes": max_bytes,
        "backupCount": backup_count,
        "encoding": "utf-8",
    }

    if "sanic.root" in config["loggers"]:
        root_logger = config["loggers"]["sanic.root"]
        root_handlers = root_logger.setdefault("handlers", [])
        if "app_file" not in root_handlers:
            root_handlers.append("app_file")
        root_logger["level"] = log_level

    if "sanic.error" in config["loggers"]:
        error_logger = config["loggers"]["sanic.error"]
        error_handlers = error_logger.setdefault("handlers", [])
        if "error_file" not in error_handlers:
            error_handlers.append("error_file")

    if "sanic.access" in config["loggers"]:
        access_logger = config["loggers"]["sanic.access"]
        access_handlers = access_logger.setdefault("handlers", [])
        if "access_file" not in access_handlers:
            access_handlers.append("access_file")
        access_logger["level"] = log_level

    root_handlers = config["root"].setdefault("handlers", [])
    if "app_file" not in root_handlers:
        root_handlers.append("app_file")
    config["root"]["level"] = log_level

    return config
