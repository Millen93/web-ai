from pydantic import BaseModel


class MessagesModel(BaseModel):
    id: int
    # user_id: int
    # TIMESTAMP: str
    # llm: str
    message: str

    class Config:
        orm_mode = True
