from fastapi import APIRouter

from app.api.v1.endpoints import batches
from app.api.v1.endpoints.endpoints_activity import router as activity_router
from app.api.v1.endpoints.endpoints_course import router as course_router
from app.api.v1.endpoints.endpoints_program import router as program_router
from app.api.v1.endpoints.endpoints_school import router as school_router
from app.api.v1.endpoints import endpoints_user, endpoints_student, endpoints_advisor, endpoints_jury
from app.core.responses import JSendRoute

api_router = APIRouter(route_class=JSendRoute)
# existing batches router
api_router.include_router(
    batches.router,
    prefix="/batches",
    tags=["batches"]
)

# activity endpoints
api_router.include_router(activity_router)

# course endpoints
api_router.include_router(course_router)

# program endpoints
api_router.include_router(program_router)

# school endpoints
api_router.include_router(school_router)

# user endpoints
api_router.include_router(endpoints_user.router)

# student endpoints
api_router.include_router(endpoints_student.router)

# advisor endpoints
api_router.include_router(endpoints_advisor.router)

# jury endpoints
api_router.include_router(endpoints_jury.router)
