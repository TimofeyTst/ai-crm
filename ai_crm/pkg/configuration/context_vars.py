import contextvars

psql_pool_singleton: contextvars.ContextVar[dict] = contextvars.ContextVar(
    "_context_vars_psql_pool_singleton"
)
read_only: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "_context_vars_read_only"
)
