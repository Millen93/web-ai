from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn
from chat.router import router_chat as router_chat
from fastapi.responses import HTMLResponse
from auth.auth import auth_backend, fastapi_users, current_user
from auth.schemas import UserCreate, UserRead
from models import User
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
app = FastAPI(
    title="Web AI chat",
    openapi_items={"schemas": {"CallableField": {}}}
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return
    elif exc.status_code == 422:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)



app.include_router(router_chat)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return templates.TemplateResponse("non_auth.html", {"request": request})
    elif exc.status_code == 422:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )




templates = Jinja2Templates(directory="templates")

@app.get("/")
async def web_router(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})





if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
