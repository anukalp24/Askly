from fastapi.responses import JSONResponse
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_chroma import Chroma
from sentence_transformers import CrossEncoder
from shared_models import llm, embeddings, reranker



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

2. Answer the user's question directly and naturally. Start with a short,
relevant sentence that introduces the answer. Do not start the response
directly with bullet points.

3. Prefer natural paragraphs. Use bullet points only when they clearly
improve readability. For broad questions such as "What's on this page?"
or "What does this document contain?", give a concise overview of the
main subjects instead of immediately listing every individual detail.

4. If the context does not contain enough information to answer, respond
exactly with:
"The document doesn't contain enough information to answer this question."

5. Do not guess, infer beyond what's written, or add information that is
not present in the context.

6. Do NOT use unnecessary preambles such as:
"Based on the context provided..."
"According to the document..."
"The context states..."

7. Do NOT include citation markers, bracketed quotes, or source tags such
as 【...】.

8. NEVER output the characters < or >. If the context contains text inside
angle brackets, rewrite it naturally without the brackets.

9. Do not copy the context word-for-word. Summarize and explain it in your
own words while preserving the information and meaning contained in the
context.
context:
{context}

Question:
{question}
"""
        response = llm.invoke(prompt)
        return JSONResponse(status_code=200 , content={"question" : question, "answer" : response.content})

                     

    except Exception as error:
        return JSONResponse(status_code=500 , content={"message" : "Internal server error"})
