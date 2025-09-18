Production run
```
gunicorn app:create_app -w $(nproc) -k uvicorn.workers.UvicornWorker
```