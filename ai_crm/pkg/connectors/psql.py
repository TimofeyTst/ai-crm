import asyncpg
import contextlib

from ai_crm.pkg.configuration import settings
from ai_crm.pkg.logger import logger as logger_lib

logger = logger_lib.get_logger(__name__)

# TODO: mdb connect
@contextlib.asynccontextmanager
async def get_connection(read_only=False):
    dsn = settings.ai_crm_env.POSTGRES.DSN
    currect_conn = None
    # currect_conn, read_only_mode = _get_pg_pool_context()

    if currect_conn:
        yield currect_conn
    else:
        logger.info('creating a new RO connection' if read_only else 'creating a new connection')
        pool = await asyncpg.create_pool(dsn)
        # pool = context.pg.slave_pool if read_only else context.pg.master_pool 

        async with pool.acquire() as new_connection:
            try:
                transaction = new_connection.transaction()
                await transaction.start()
                # Save the conn and connection mode to use in nesting
                # _set_pg_pool_context(new_connection, read_only)
                yield new_connection
            except Exception as error:
                logger.warning(f'an error occured: {error}, rolling back transaction {transaction}')
                await transaction.rollback()
                raise error
            finally:
                pass
                # Finally reset coro state
                # _set_pg_pool_context(None, None)

