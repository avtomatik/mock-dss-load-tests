import asyncio

from locust import User, constant

from clients.postgresql import AsyncPostgresClient
from clients.rabbitmq import AsyncRabbitMQClient
from clients.redis import AsyncRedisClient

from .config import settings


class AsyncBackendUser(User):
    abstract = True
    wait_time = constant(1)

    async def _connect_clients(self):
        self.db = AsyncPostgresClient(settings.db_dsn)
        self.mq = AsyncRabbitMQClient(settings.mq_url)
        self.cache = AsyncRedisClient(settings.redis_url)

        await asyncio.gather(
            self.db.connect(), self.mq.connect(), self.cache.connect()
        )

    async def _close_clients(self):
        await asyncio.gather(
            self.db.close(), self.mq.close(), self.cache.close()
        )

    async def on_start(self):
        await self._connect_clients()

    async def on_stop(self):
        await self._close_clients()
