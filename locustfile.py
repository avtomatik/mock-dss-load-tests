import time

from locust import task

from core.constants import SECONDS_TO_MILLISECONDS
from core.helpers import generate_current_date_str
from core.users import AsyncBackendUser


class DSSLoadUser(AsyncBackendUser):
    @task(3)
    async def query_db(self):
        async with self.environment.events.request.request(
            request_type="postgres", name="select_count"
        ) as req:
            val = await self.db.get_signature_count_for_day(
                generate_current_date_str()
            )
            req.response_length = len(str(val))

    @task(2)
    async def insert_db(self):
        async with self.environment.events.request.request(
            request_type="postgres", name="insert_document"
        ) as req:
            await self.db.insert_document()
            req.response_length = 0

    @task(4)
    async def publish_message(self):
        payload = {"ts": time.time(), "payload": "sync_test"}

        async with self.environment.events.request.request(
            request_type="rabbitmq", name="publish"
        ) as req:
            await self.mq.publish(payload)
            req.response_length = len(str(payload))

    @task(3)
    async def redis_ops(self):
        key = f"test:{int(time.time() * SECONDS_TO_MILLISECONDS)}"

        async with self.environment.events.request.request(
            request_type="cache", name="set_get"
        ) as req:
            await self.cache.set_key(key, "value", expire=120)
            val = await self.cache.get_key(key)
            req.response_length = len(val or "")
