from fastapi import APIRouter, Body
from services.fsq_services import fsq_search
from models.openai_models import OpenAIRequest
from services.openai_services import text_to_json

router = APIRouter(tags=["fsq"])

@router.post("/execute")
async def search(data: OpenAIRequest = Body(...)):
    prompt = await text_to_json(data.message)
    return await fsq_search(data.action, prompt)