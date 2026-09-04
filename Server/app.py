
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app  = FastAPI()
from routes.Ask import router as ask_router
from routes.Upload import router as upload_router
app.add_middleware(
    CORSMiddleware ,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:8000" , "https://askly-mo5d.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ask_router)
app.include_router(upload_router)