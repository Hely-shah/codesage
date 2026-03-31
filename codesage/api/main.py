from fastapi import FastAPI
from codesage.core.logging import configure_logging
from codesage.api.routes import router
from codesage.db.init_db import init_db

configure_logging()
app = FastAPI(title="CodeSage API", version="0.2.1")

@app.on_event("startup")
def _startup():
    init_db()

app.include_router(router)
