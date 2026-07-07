from contextlib import asynccontextmanager
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

_scheduler_runner = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler_runner
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    await init_db()
    _scheduler_runner = WorkflowScheduler()
    await _scheduler_runner.start()
    yield
    logger.info(f"Shutting down {settings.app_name}")
    if _scheduler_runner:
        await _scheduler_runner.stop()
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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
