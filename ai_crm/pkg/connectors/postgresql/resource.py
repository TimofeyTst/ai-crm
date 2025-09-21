import asyncpg
from typing import Optional, Dict, List

from ai_crm.pkg.configuration import settings
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.connectors.postgresql.host import PostgreSQLHost

logger = logger_lib.get_logger(__name__)

class Resource:
    """PostgreSQL connection pool manager with master-slave support."""

    def __init__(self):
        self._hosts: List[PostgreSQLHost] = []
        self._master_host: Optional[PostgreSQLHost] = None
        self._slave_hosts: List[PostgreSQLHost] = []
        self._slave_round_robin_index: int = 0
        self._config = settings.ai_crm_env.POSTGRES

    async def on_startup(self) -> None:
        logger.info("Initializing PostgreSQL connection pools...")

        try:
            await self._initialize_hosts() 
        except Exception as error:
            logger.error(f"Failed to initialize PostgreSQL connection pools: {error}")
            raise error

        logger.info(f"PostgreSQL pools initialized successfully. Master: {self._master_host.host if self._master_host else 'None'}, Slaves: {[h.host for h in self._slave_hosts]}")

    async def on_shutdown(self) -> None:
        logger.info("Closing PostgreSQL connection pools...")
        
        for host in self._hosts:
            try:
                logger.info(f"Closing pool for {host.host}")
                await host.close_pool()
            except Exception as error:
                logger.error(f"Error while closing pool for {host.host}: {error}")
        
        logger.info("All PostgreSQL pools closed")

    async def _initialize_hosts(self) -> None:
        self._hosts = []
        self._slave_hosts = []

        for host in self._config.get_hosts_list():
            pg_host = PostgreSQLHost(host=host)
            self._hosts.append(pg_host)

            try:
                await pg_host.open_pool_and_fill_status()
            except Exception as error:
                logger.error(f"Failed to open pool and fill status for host {host}: {str(type(error))}: {error}")

            if not pg_host.is_healthy:
                logger.warning(f"Host {host} is unhealthy, skipping...")
                continue

            if pg_host.is_master:
                self._master_host = pg_host
                logger.info(f"Host {host}: Master")
            else:
                self._slave_hosts.append(pg_host)
                logger.info(f"Host {host}: Slave")
        
        if not self._master_host:
            raise RuntimeError("No master host found or all masters are unhealthy")

    def get_pool(self, read_only: bool = False) -> asyncpg.Pool:
        """Get connection pool with master/slave selection and RoundRobin for slaves."""
        if read_only:
            return self._get_slave_pool_round_robin()
        else:
            return self._get_master_pool()

    def _get_master_pool(self) -> asyncpg.Pool:
        if not self._master_host or not self._master_host.pool:
            raise RuntimeError("Master PostgreSQL pool is not initialized or unhealthy")
        
        logger.debug(f"Using master pool: {self._master_host.host}")
        return self._master_host.pool

    def _get_slave_pool_round_robin(self) -> asyncpg.Pool:
        healthy_slaves = [s for s in self._slave_hosts if s.is_healthy and s.pool]

        if not healthy_slaves:
            logger.warning("No healthy slave pools available, falling back to master")
            return self._get_master_pool()
        
        # Round-robin selection
        selected_slave = healthy_slaves[self._slave_round_robin_index % len(healthy_slaves)]
        self._slave_round_robin_index = (self._slave_round_robin_index + 1) % len(healthy_slaves)

        logger.debug(f"Using slave pool (RR): {selected_slave.host}")
        return selected_slave.pool

    def get_hosts_info(self) -> Dict[str, any]:
        return {
            "master": self._master_host.host if self._master_host else None,
            "slaves": [s.host for s in self._slave_hosts],
            "total_hosts": len(self._hosts),
            "healthy_hosts": len([h for h in self._hosts if h.is_healthy])
        }
