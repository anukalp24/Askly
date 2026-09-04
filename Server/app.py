

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app  = FastAPI()
from Server.routes.Ask import router as ask_router
from Server.routes.Upload import router as upload_router
app.add_middleware(
    CORSMiddleware ,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ask_router)
app.include_router(upload_router)