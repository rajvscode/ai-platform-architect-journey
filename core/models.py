from pydantic import BaseModel

class LogRequest(BaseModel):
    log: str
    context: list[str] = []

class DocumentRequest(BaseModel):
    text: str