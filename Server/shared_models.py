import torch
from sentence_transformers import CrossEncoder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

reranker = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2-v2', device="cpu")
reranker.model.half()

