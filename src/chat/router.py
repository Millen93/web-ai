from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter, Request, Depends, File, UploadFile
from chat.llm_model import get_blender_responses as generate_micro
from chat.llm_model import get_zephyr_responses as generate_zephyr
from chat.llm_model import get_coder_responses as generate_coder
from chat.llm_model import get_image_responses as generate_image
from chat.llm_model import get_text_from_image as generate_ocr
from database import async_session_maker, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models import Messages
from chat.schemas import MessagesModel
from sqlalchemy import insert, select
from typing import List, AsyncGenerator, NoReturn
from models import User
from auth.auth import current_user, fastapi_users
from config import AUTH_DB
import os

router_chat = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

def check_docs(llm):
        if os.path.exists('doc.txt'):
            if llm == 'PaddleOCR':
                doc_prompts = {'file': open('doc.txt', 'rb')}
            else:
                doc = open('doc.txt', 'r')
                doc_prompts = doc.read()
                doc.close()
        else:
            doc_prompts = ""
        return doc_prompts



templates = Jinja2Templates(directory="templates")

async def add_messages_to_db(user_id: int, message: str, llm: str):
    if AUTH_DB == 'true':
        async with async_session_maker() as session:
            stmt = insert(Messages).values(
                user_id=user_id,
                message=message,
                llm=llm
            )
            await session.execute(stmt)
            await session.commit()







if AUTH_DB == 'true':
    @router_chat.get("/")
    async def web_router(request: Request, user: User = Depends(current_user)):
        ID = user.id
        return templates.TemplateResponse("chat.html", {"request": request, "USER_ID": ID})
else:
    @router_chat.get("/")
    async def web_router(request: Request):
        ID = "1"
        return templates.TemplateResponse("chat.html", {"request": request, "USER_ID": ID})


@router_chat.post("/upload/")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open('doc.txt', 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the File"}
    finally:
        file.file.close()
    return {"message": f"Successfully uploaded {file.filename}"}


@router_chat.websocket("/ws/{user_id}/{llm}")
async def websocket_endpoint(websocket: WebSocket, llm: str, user_id: int):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            docs = check_docs(llm)
            if llm == "blenderbot-400M-distill":
                async for text in generate_micro(message + docs):
                    await websocket.send_text(text)
                    await add_messages_to_db(user_id, f"USER  prompt: {message + docs}, AI answer: {text}", llm)
            elif llm == "zephyr-7b-beta":
                text = await generate_zephyr(message + docs)
                await websocket.send_text(text)
                await add_messages_to_db(user_id, f"USER  prompt: {message + docs}, AI answer: {text}", llm)
            elif llm == "Everyone-Coder-4x7b-Base-GPTQ":
                text = await generate_coder(message + docs)
                await websocket.send_text(text)
                await add_messages_to_db(user_id, f"USER  prompt: {message + docs}, AI answer: {text}", llm)
            elif llm == "openjourney":
                image_data = await generate_image(message + docs)
                await websocket.send_bytes(image_data)
            elif llm == "PaddleOCR":
                 text = await generate_ocr(docs)
                 await websocket.send_text(text)
            else:
                pass
    except WebSocketDisconnect:
        os.remove('doc.txt')
        pass
