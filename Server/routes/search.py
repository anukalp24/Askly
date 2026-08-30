from fastapi import APIRouter
from controllers.Search import searchController
from fastapi import UploadFile , File  , Form
from typing import Optional , List

router = APIRouter()
@router.post("/search")
async def func(filesparameter : List[UploadFile] = File(...) , text: Optional[str]  = Form(None)): #  "Get files from the incoming multipart/form-data request as uploaded files."
 return await searchController(filesparameter , text)
# when req comes then only call this function

# as its a decorator either we need to pass the reqeasut instance or parse and send to the ocntorlle ror we can just use norml cotnrolle rclallign then the controller itslef hadkes eveyrhtig
