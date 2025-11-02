import asyncio
import contextlib

from ai_crm.pkg import context
from ai_crm.pkg.configuration import context_vars
from ai_crm.pkg.logger import logger as logger_lib

logger = logger_lib.get_logger(__name__)


def _get_task_hash() -> int:
    task = asyncio.current_task()
    return hash(task)


def _get_psql_pool_context():
    psql_singleton_dict = context_vars.psql_pool_singleton.get({})
    task_id = _get_task_hash()

    conn, read_only_mode = psql_singleton_dict.get(task_id, (None, None))
    logger.debug(f"task_id={task_id}, conn={conn}")

    return conn, read_only_mode


def _set_psql_pool_context(conn, read_only_mode):
    psql_singleton_dict = context_vars.psql_pool_singleton.get({})
    task_id = _get_task_hash()

    psql_singleton_dict[task_id] = (conn, read_only_mode)
    context_vars.psql_pool_singleton.set(psql_singleton_dict)


@contextlib.asynccontextmanager
async def get_connection(context: context.AnyContext, read_only=False):
    current_conn, read_only_mode = _get_psql_pool_context()

    if current_conn:
        logger.info("using existing connection")
        yield current_conn
    else:
        logger.info(
            "creating a new RO connection"
            if read_only
            else "creating a new connection"
        )
        pool = context.postgresql.get_pool(read_only)

        async with pool.acquire() as new_connection:
            try:
                transaction = new_connection.transaction()
                await transaction.start()
                # Save the conn and connection mode to use in nesting
                _set_psql_pool_context(new_connection, read_only)
                yield new_connection
                await transaction.commit()
            except Exception as error:
                logger.warning(
                    f"an error occured: {error}, rolling back transaction {transaction}"
                )
                await transaction.rollback()
                raise error
            finally:
                _set_psql_pool_context(None, None)
