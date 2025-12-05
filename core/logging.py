import inspect
import logging
import time
from logging.handlers import RotatingFileHandler

from core.constants import (LOG_BACKUP_COUNT, LOG_FILENAME,
                            LOG_FORMAT_DETAILED, LOG_MAX_SIZE)


def get_current_method():
    return inspect.currentframe().f_code.co_name


def log_task_start(task_name: str):
    logger.info(f"Scheduled task {task_name} to run.")


def log_task_end(task_name: str, duration: float):
    logger.info(
        f"Task {task_name} completed, duration: {duration:.4f} seconds."
    )


def log_task_time(task_func):
    async def wrapper(self, *args, **kwargs):
        task_name = get_current_method()
        start_time = time.time()

        log_task_start(task_name)

        try:
            return await task_func(self, *args, **kwargs)
        finally:
            end_time = time.time()
            duration = end_time - start_time
            log_task_end(task_name, duration)

    return wrapper


file_handler = RotatingFileHandler(
    LOG_FILENAME, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT
)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(LOG_FORMAT_DETAILED)
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
