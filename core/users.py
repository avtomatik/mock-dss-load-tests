import time

import gevent
from locust import User, constant

from clients.postgresql import PostgresClient
from clients.rabbitmq import RabbitMQClient
from clients.redis import RedisClient

from .config import settings
from .constants import SECONDS_TO_MILLISECONDS


class BackendUser(User):
    abstract = True
    wait_time = constant(1)

    def _connect_clients(self):
        self.db = PostgresClient(settings.db_url)
        self.mq = RabbitMQClient(settings.mq_url)
        self.cache = RedisClient(settings.cache_url)

        gevent.spawn(self.db.connect)
        gevent.spawn(self.mq.connect)
        gevent.spawn(self.cache.connect)

    def _close_clients(self):
        gevent.spawn(self.db.close)
        gevent.spawn(self.mq.close)
        gevent.spawn(self.cache.close)

    def on_start(self):
        self._connect_clients()

    def on_stop(self):
        self._close_clients()

    def fire_event(
        self, request_type, name, start_time, response_length, exception=None
    ):
        self.environment.events.request.fire(
            request_type=request_type,
            name=name,
            response_time=(time.perf_counter() - start_time)
            * SECONDS_TO_MILLISECONDS,
            response_length=response_length,
            exception=exception,
        )
