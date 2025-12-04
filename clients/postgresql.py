from psycopg_pool import ConnectionPool

from core.constants import SQL_INSERT_DOCUMENT, SQL_SELECT_COUNT
from core.helpers import generate_random_content, generate_random_id


class AsyncPostgresClient:
    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10):
        self.dsn: str = dsn
        self.pool: ConnectionPool | None = None
        self.min_size: int = min_size
        self.max_size: int = max_size

    async def connect(self):
        if self.pool is None:
            self.pool = await ConnectionPool(
                self.dsn,
                min_size=self.min_size,
                max_size=self.max_size,
                timeout=30,
            )

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def get_signature_count_for_day(self, day: str) -> int:
        async with self.pool.connection() as conn:
            result = await conn.fetchval(SQL_SELECT_COUNT, (day,))
            return result or 0

    async def insert_document(self) -> None:
        async with self.pool.connection() as conn:
            document_id = generate_random_id()
            content = generate_random_content()
            await conn.execute(SQL_INSERT_DOCUMENT, (document_id, content))
