import time

from locust import task

from core.constants import SECONDS_TO_MILLISECONDS
from core.helpers import generate_current_date_str
from core.users import BackendUser


class DSSLoadUser(BackendUser):
    @task(3)
    def query_db(self):
        start_time = time.time()
        try:
            val = self.db.get_signature_count_for_day(
                generate_current_date_str()
            )

            response_length = len(str(val))

            self.environment.events.request.fire(
                request_type="postgres",
                name="select_count",
                response_time=(time.time() - start_time)
                * SECONDS_TO_MILLISECONDS,
                response_length=response_length,
                exception=None,
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="postgres",
                name="select_count",
                response_time=(time.time() - start_time)
                * SECONDS_TO_MILLISECONDS,
                response_length=0,
                exception=e,
            )
            raise

    @task(2)
    def insert_db(self):
        start_time = time.time()
        try:
            self.db.insert_document()

            self.environment.events.request.fire(
                request_type="postgres",
                name="insert_document",
                response_time=(time.time() - start_time)
                * SECONDS_TO_MILLISECONDS,
                response_length=0,
                exception=None,
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="postgres",
                name="insert_document",
                response_time=(time.time() - start_time)
                * SECONDS_TO_MILLISECONDS,
                response_length=0,
                exception=e,
            )
            raise

    @task(4)
    def publish_message(self):
        payload = {"ts": time.time(), "payload": "sync_test"}
        start_time = time.time()

        try:
            self.mq.publish(payload)

            self.environment.events.request.fire(
                request_type="rabbitmq",
                name="publish",
                response_time=(time.time() - start_time)
                * SECONDS_TO_MILLISECONDS,
                response_length=len(str(payload)),
                exception=None,
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="rabbitmq",
                name="publish",
                response_time=(time.time() - start_time)
                * SECONDS_TO_MILLISECONDS,
                response_length=0,
                exception=e,
            )
            raise

    @task(3)
    def redis_ops(self):
        key = f"test:{int(time.time() * SECONDS_TO_MILLISECONDS)}"
        start_time = time.time()

        try:
            self.cache.set_key(key, "value", expire=120)
            val = self.cache.get_key(key)

            self.environment.events.request.fire(
                request_type="cache",
                name="set_get",
                response_time=(time.time() - start_time)
                * SECONDS_TO_MILLISECONDS,
                response_length=len(val or ""),
                exception=None,
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="cache",
                name="set_get",
                response_time=(time.time() - start_time)
                * SECONDS_TO_MILLISECONDS,
                response_length=0,
                exception=e,
            )
            raise
