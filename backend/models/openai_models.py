from pydantic import BaseModel

class OpenAIRequest(BaseModel):
    message: str
    action: str