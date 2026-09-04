from fastapi import APIRouter , Form , Cookie
from controllers.ask import Ask
from typing import Optional

router = APIRouter()
@router.post("/ask")
async def ask(question : str = Form(...) , session_id : str = Cookie(...)):
    return await Ask(question , session_id)