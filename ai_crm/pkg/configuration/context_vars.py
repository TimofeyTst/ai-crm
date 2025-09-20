import typing as tp
import contextvars


psql_pool_singleton: contextvars.ContextVar[tp.Dict] = contextvars.ContextVar('_context_vars_psql_pool_singleton')
read_only: contextvars.ContextVar[bool] = contextvars.ContextVar('_context_vars_read_only')
