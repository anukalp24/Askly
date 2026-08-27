from fastapi import APIRouter
from controllers.Search import searchController
from fastapi import UploadFile , File
router = APIRouter()
from typign import List
@router.post("/search")
def func(filesparameter : List[UploadFile] = File(...)): #  "Get files from the incoming multipart/form-data request as uploaded files."
 return searchController(filesparameter)
# when req comes then only call this function