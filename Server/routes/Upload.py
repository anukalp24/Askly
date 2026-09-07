from fastapi import APIRouter
from controllers.Upload import searchController
from fastapi import UploadFile , File  , Form , Cookie
from typing import Optional , List

router = APIRouter()
@router.post("/upload")
async def func(filesparameter : List[UploadFile] = File(...) , question: Optional[str]  = Form(None), session_id: Optional[str]   = Cookie(None)): #  "Get files from the incoming multipart/form-data request as uploaded files."
 return await searchController(filesparameter , question , session_id)