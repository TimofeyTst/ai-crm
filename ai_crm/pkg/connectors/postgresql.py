"""PostgreSQL connector with connection pool management."""

import asyncpg
from typing import Optional

from ai_crm.pkg.configuration import settings
from ai_crm.pkg.logger import logger as logger_lib

logger = logger_lib.get_logger(__name__)


# TODO: 
# 1) хочу в settings указание HOSTS постгреса, в одном массиве через запятую
# 2) Хочу при инициализации класса инициализировать хосты мастером (строго один мастер) или слейвами (несколько) путем запросов в них, для примера можешь выполнить:
# SELECT pg_is_in_recovery() as is_in_recovery, NOW() - pg_last_xact_replay_timestamp() as replication_delay;
# Или более лучшую другую штуку, как сочтешь лучше
# 3) Хочу для read_only транзакции использовать SLAVE_HOSTS RoundRobin политику, для не read_only один пул к MASTER_HOST
# Надо реализовать@psql.py @settings.py 
class PostgreSQL:
    """PostgreSQL connection pool manager."""
    
    def __init__(self):
        self._pool: Optional[asyncpg.Pool] = None
        
    async def on_startup(self) -> None:
        """Initialize connection pool on startup."""
        try:
            logger.info("Initializing PostgreSQL connection pool...")
            self._pool = await asyncpg.create_pool(
                dsn=settings.ai_crm_env.POSTGRES.DSN,
                min_size=settings.ai_crm_env.POSTGRES.MIN_CONNECTION,
                max_size=settings.ai_crm_env.POSTGRES.MAX_CONNECTION,
                command_timeout=60
            )
            logger.info("PostgreSQL connection pool initialized successfully")
        except Exception as error:
            logger.error(f"Failed to initialize PostgreSQL connection pool: {error}")
            raise error
    
    async def on_shutdown(self) -> None:
        """Close connection pool on shutdown."""
        if self._pool:
            try:
                logger.info("Closing PostgreSQL connection pool...")
                await self._pool.close()
                logger.info("PostgreSQL connection pool closed successfully")
            except Exception as error:
                logger.error(f"Error while closing PostgreSQL connection pool: {error}")
                raise error
        else:
            logger.warning("PostgreSQL connection pool was not initialized")
    
    def get_pool(self, read_only: bool = False) -> asyncpg.Pool:
        """Get connection pool with validation."""
        if not self._pool:
            raise RuntimeError("PostgreSQL connection pool is not initialized")
        return self._pool
