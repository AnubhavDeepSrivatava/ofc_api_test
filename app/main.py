
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import logic_exception
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.error_codes import ErrorCodes

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1]
        errors[field] = {
            "code": ErrorCodes.value_required if error["type"] == "missing" else ErrorCodes.invalid_input,
            "message": error["msg"]
        }
    return JSONResponse(status_code=400, content={"status": "fail", "data": errors})

@app.exception_handler(logic_exception)
async def logic_exception_handler(request: Request, exc: logic_exception):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "fail", 
            "data": { "logic": {"code": exc.code, "message": exc.message} }
        }
    )


app.include_router(api_router, prefix=settings.API_V1_STR)

