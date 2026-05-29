from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.api.middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware
from backend.db.session import init_db, close_db
from backend.langgraph_engine.execution.scheduler import WorkflowScheduler
from backend.utils.logger import setup_logging, get_logger
from config import settings

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

app.include_router(router, prefix=settings.api_prefix)

_scheduler_runner = None


@app.on_event("startup")
async def startup():
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    await init_db()
    global _scheduler_runner
    _scheduler_runner = WorkflowScheduler()
    await _scheduler_runner.start()


@app.on_event("shutdown")
async def shutdown():
    logger.info(f"Shutting down {settings.app_name}")
    global _scheduler_runner
    if _scheduler_runner:
        await _scheduler_runner.stop()
    await close_db()
