from fastapi import FastAPI

from jobastra_ai.api.errors import register_exception_handlers
from jobastra_ai.api.routes.career import router as career_router
from jobastra_ai.api.routes.health import router as health_router
from jobastra_ai.api.routes.jobs import router as jobs_router
from jobastra_ai.api.routes.knowledge import router as knowledge_router
from jobastra_ai.api.routes.matching import router as matching_router
from jobastra_ai.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)

register_exception_handlers(app)
app.include_router(career_router, prefix="/api")
app.include_router(health_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")
app.include_router(knowledge_router, prefix="/api")
app.include_router(matching_router, prefix="/api")
