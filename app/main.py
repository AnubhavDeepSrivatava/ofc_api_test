# from fastapi import FastAPI
# # from my_company_core.logging import setup_logging
# # from my_company_core.middleware import add_standard_middleware
# from app.api.v1.api import api_router
# from app.core.config import settings

# from app.core.db import engine, Base
# from app.models.student import Student
# # Base.metadata.create_all(bind=engine)
# from app.models.school import School
# from app.models.program import Program
# from app.models.course import Course
# from app.models.activity import Activity

# def create_application() -> FastAPI:
#     application = FastAPI(
#         title=settings.PROJECT_NAME,
#         openapi_url=f"{settings.API_V1_STR}/openapi.json"
#     )
    
#     # Standardized setup from your shared library
#     # setup_logging()
#     # add_standard_middleware(application)
    
#     application.include_router(api_router, prefix=settings.API_V1_STR)
#     return application

# app = create_application()
# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    application.include_router(api_router, prefix=settings.API_V1_STR)
    return application

app = create_application()
