from pathlib import Path
import logging
import logging.config

log_file_path = Path('/logs/api.log')

log_file_path.parent.mkdir(parents=True, exist_ok=True)

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": str(log_file_path),
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"],
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)
