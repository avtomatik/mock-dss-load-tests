import inspect
import logging
import time
from logging.handlers import RotatingFileHandler

from locust import task

from core.constants import SECONDS_TO_MILLISECONDS
from core.helpers import generate_current_date_str
from core.users import AsyncBackendUser

log_filename = "locust_test_logs.log"
log_max_size = 10 * 1024 * 1024
log_backup_count = 5

file_handler = RotatingFileHandler(
    log_filename, maxBytes=log_max_size, backupCount=log_backup_count
)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


class DSSLoadUser(AsyncBackendUser):
    def get_current_method(self):
        return inspect.currentframe().f_code.co_name

    async def on_task_start(self, task_name: str):
        logger.info(f"Scheduled task {task_name} to run.")

    async def on_task_end(self, task_name: str, duration: float):
        logger.info(
            f"Task {task_name} completed, duration: {duration:.4f} seconds."
        )

    @task(3)
    async def query_db(self):
        task_name = self.get_current_method()
        start_time = time.time()

        await self.on_task_start(task_name)

        async with self.environment.events.request.request(
            request_type="postgres", name="select_count"
        ) as req:
            val = await self.db.get_signature_count_for_day(
                generate_current_date_str()
            )
            req.response_length = len(str(val))

        end_time = time.time()
        duration = end_time - start_time
        await self.on_task_end(task_name, duration)

    @task(2)
    async def insert_db(self):
        task_name = self.get_current_method()
        start_time = time.time()

        await self.on_task_start(task_name)

        async with self.environment.events.request.request(
            request_type="postgres", name="insert_document"
        ) as req:
            await self.db.insert_document()
            req.response_length = 0

        end_time = time.time()
        duration = end_time - start_time
        await self.on_task_end(task_name, duration)

    @task(4)
    async def publish_message(self):
        task_name = self.get_current_method()
        start_time = time.time()

        await self.on_task_start(task_name)

        payload = {"ts": time.time(), "payload": "sync_test"}

        async with self.environment.events.request.request(
            request_type="rabbitmq", name="publish"
        ) as req:
            await self.mq.publish(payload)
            req.response_length = len(str(payload))

        end_time = time.time()
        duration = end_time - start_time
        await self.on_task_end(task_name, duration)

    @task(3)
    async def redis_ops(self):
        task_name = self.get_current_method()
        start_time = time.time()

        await self.on_task_start(task_name)

        key = f"test:{int(time.time() * SECONDS_TO_MILLISECONDS)}"

        async with self.environment.events.request.request(
            request_type="cache", name="set_get"
        ) as req:
            await self.cache.set_key(key, "value", expire=120)
            val = await self.cache.get_key(key)
            req.response_length = len(val or "")

        end_time = time.time()
        duration = end_time - start_time
        await self.on_task_end(task_name, duration)
