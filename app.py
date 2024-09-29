from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from routes import user_routes, Blog

app = FastAPI()

app.include_router(user_routes.api_router, prefix="/user", tags=["User"])
app.include_router(Blog.api_router, prefix="/blogs", tags=["Blog"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )