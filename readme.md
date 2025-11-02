Production run
```
poetry run gunicorn ai_crm.api:create_app -w 1 -k uvicorn.workers.UvicornWorker
```

Migrations
```
bash scripts/migrate.sh
```