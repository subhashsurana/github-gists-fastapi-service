from fastapi import FastAPI
from app.api.routes import router as gists_router
from fastapi_pagination import add_pagination
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
from fastapi import Request

logger = logging.getLogger("uvicorn.error")

app = FastAPI()
app.include_router(gists_router)
add_pagination(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to the GitHub Gits Data fetch API"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"422 Validation error on request to {request.url}: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid input. Please check the username or query parameters."},
    )