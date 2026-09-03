from fastapi.responses import JSONResponse
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from sentence_transformers import CrossEncoder
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b" , temperature=0)

embeddings = HuggingFaceEmbeddings(model_name= "sentence-transformers/all-MiniLM-L6-v2")
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')


async def Ask(question , session_id):
    try:

        vectorDB = Chroma(embedding_function=embeddings , collection_name="pdf_documents" , persist_directory="./chroma_storage")

        retriever = vectorDB.as_retriever(search_kwargs={"k" : 25 , "filter" : {"session_id" : session_id}})
        if question:
            returnedAnswer = retriever.invoke(question)   # similarity search

            if not returnedAnswer:
                return JSONResponse(status_code=400 , content={"message" : "No relevant information found in the document."})
#             returned ans will look like this:- # ReturnedAnswer = [
# #     Document(...),   # chunk 1
# #     Document(...),   # chunk 2]
        
        # round 2 rerank

        pairs = []
        for chunk in returnedAnswer:
            pairs.append((question , chunk.page_content))
        scores = reranker.predict(pairs)   # scores = [0.2, 0.9, 0.5, ...]

        reranked = sorted(zip(returnedAnswer , scores) , key=lambda x: x[1] , reverse=True)

        topchunks = []
        for tuplee , score in reranked[:5]:
                topchunks.append(tuplee)


        seperation = []
        for topdocument in topchunks:
                    seperation.append(topdocument.page_content)

                    context = "\n\n".join(seperation)

        prompt = f"""
                    You are a precise, factual assistant that answers questions strictly
                    based on the provided document context. You never use outside knowledge,
                    even if you know the answer.
                    
                    Rules:
                    
                    1. Answer ONLY using information explicitly stated in the context below.
                    
                    2. If the context does not contain enough information to answer,
                    respond exactly with:
                    "The document doesn't contain enough information to answer this question."
                    
                    3. Do not guess, infer beyond what's written, or add information not present
                    in the context.
                    
                    4. Keep your answer clear and concise — no unnecessary preamble like
                    "Based on the context provided."
                    
                    5. If helpful, quote or closely reference the specific part of the chunk
                    that supports your answer.
                    
                    context:
                    {context}
                    
                    Question:
                    {question}

                    """
        response = llm.invoke(prompt)
        return JSONResponse(status_code=200 , content={"answer" : response.content})

                     

    except Exception as error:
        return JSONResponse(status_code=500 , content={"message" : "Internal server error"})
