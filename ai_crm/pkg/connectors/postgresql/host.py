
import asyncpg

from ai_crm.pkg.configuration import settings
from ai_crm.pkg.logger import logger as logger_lib

logger = logger_lib.get_logger(__name__)

CHECK_SLAVE_QUERY = "SELECT pg_is_in_recovery() as is_in_recovery, NOW() - pg_last_xact_replay_timestamp() as replication_delay;"


class PostgreSQLHost:
    host: str
    dsn: str
    is_master: bool = False
    replication_delay: int = 0
    is_healthy: bool = False
    pool: asyncpg.Pool | None = None

    def __init__(self, host: str):
        self.host = host
        self.dsn = settings.ai_crm_env.POSTGRES.build_dsn_for_host(host)
        self.is_master = False
        self.replication_delay = 0
        self.is_healthy = False
        self.pool = None

    async def open_pool_and_fill_status(self) -> bool:
        self.pool = await self.get_pool()
        self.is_healthy = False
        self.is_master = False
        self.replication_delay = 0

        try:
            async with self.pool.acquire(timeout=10) as new_connection:
                result = await new_connection.fetchrow(CHECK_SLAVE_QUERY)
                self.is_healthy = True
                self.is_master = not result["is_in_recovery"]
                self.replication_delay = result["replication_delay"]
        except Exception as error:
            logger.error(
                f"Error checking host {self.host} role: {str(type(error))}: {error}"
            )
            raise error

    async def get_pool(self) -> asyncpg.Pool:
        if self.pool:
            return self.pool

        return await asyncpg.create_pool(
            dsn=self.dsn,
            min_size=settings.ai_crm_env.POSTGRES.MIN_CONNECTION,
            max_size=settings.ai_crm_env.POSTGRES.MAX_CONNECTION,
            command_timeout=30,
        )

    async def close_pool(self) -> None:
        if self.pool:
            await self.pool.close()
            self.pool = None
