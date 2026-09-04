from fastapi import APIRouter
from controllers.Upload import searchController
from fastapi import UploadFile , File  , Form , Cookie
from typing import Optional , List

router = APIRouter()
@router.post("/upload")
async def func(filesparameter : List[UploadFile] = File(...) , question: Optional[str]  = Form(None), session_id: Optional[str]   = Cookie(None)): #  "Get files from the incoming multipart/form-data request as uploaded files."
 return await searchController(filesparameter , question , session_id)
# when req comes then only call this function

# as its a decorator either we need to pass the reqeasut instance or parse and send to the ocntorlle ror we can just use norml cotnrolle rclallign then the controller itslef hadkes eveyrhtig





# we can do it liek this also
# router.add_api_route("/profile" ,profile )
# Yes! Exactly right. 🎯

# If your controller itself is written to accept request: Request directly:

# python
# async def profile(request: Request):
#     form = await request.form()
#     files = form.getlist("filesparameter")
#     text = form.get("text")
#     # ... rest of your logic
# Then you can register it directly, no wrapper needed:

# python
# router.add_api_route("/profile", profile, methods=["POST"])