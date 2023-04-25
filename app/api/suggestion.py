import openai
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from config import get_settings
from dependencies.auth import get_current_user_is_verified

suggest_router = APIRouter(
    prefix="/suggestion",
    tags=["suggestion"],
    dependencies=[Depends(get_current_user_is_verified)],
)


settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY


class SuggestionResponse(BaseModel):
    result: str


@suggest_router.get("/", response_model=SuggestionResponse)
async def get_suggestion(prompt: str):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.6,
    )
    result = response.choices[0].text
    return {"result": result.strip()}
