import time

from locust import task

from core.constants import SECONDS_TO_MILLISECONDS
from core.helpers import generate_current_date_str
from core.users import BackendUser


class DSSLoadUser(BackendUser):

    @task(3)
    def query_db(self):
        start_time = time.perf_counter()
        try:
            val = self.db.get_signature_count_for_day(
                generate_current_date_str()
            )
            self.fire_event(
                "postgres",
                "select_count",
                start_time,
                response_length=len(str(val)),
            )
        except Exception as e:
            self.fire_event("postgres", "select_count", start_time, 0, e)
            raise

    @task(2)
    def insert_db(self):
        start_time = time.perf_counter()
        try:
            self.db.insert_document()
            self.fire_event(
                "postgres",
                "insert_document",
                start_time,
                response_length=0,
            )
        except Exception as e:
            self.fire_event(
                "postgres",
                "insert_document",
                start_time,
                response_length=0,
                exception=e,
            )
            raise

    @task(4)
    def publish_message(self):
        payload = {"ts": time.perf_counter(), "payload": "sync_test"}
        start_time = time.perf_counter()

        try:
            self.mq.publish(payload)
            self.fire_event(
                "rabbitmq",
                "publish",
                start_time,
                response_length=len(str(payload)),
            )
        except Exception as e:
            self.fire_event(
                "rabbitmq",
                "publish",
                start_time,
                response_length=0,
                exception=e,
            )
            raise

    @task(3)
    def redis_ops(self):
        key = f"test:{int(time.perf_counter() * SECONDS_TO_MILLISECONDS)}"
        start_time = time.perf_counter()

        try:
            self.cache.set_key(key, "value", expire=120)
            val = self.cache.get_key(key)

            self.fire_event(
                "cache",
                "set_get",
                start_time,
                response_length=len(val or ""),
            )
        except Exception as e:
            self.fire_event(
                "cache",
                "set_get",
                start_time,
                response_length=0,
                exception=e,
            )
            raise
