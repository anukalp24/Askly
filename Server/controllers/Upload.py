from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import tempfile
import os
import uuid
from pathlib import Path
from shared_models import llm, embeddings, reranker



async def searchController(files, text , session_id=None):

    AllDocuments = []

    try:
        if not session_id:
            session_id = str(uuid.uuid4())

        for file in files:

            suffix = Path(file.filename).suffix

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_path = tmp.name
            try:
                loader = PyMuPDFLoader(tmp_path)
                document = loader.load()
                # here document is a list

                for doc in document:

                    doc.metadata["source_file"] = file.filename
                    doc.metadata["session_id"] = session_id

                    for doc in document:
                        doc.metadata["source_file"] = file.filename
                        doc.metadata["session_id"] = session_id
                AllDocuments.extend(document)
            finally:  
                os.unlink(tmp_path)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len
        )  # its just a tool/rules

        chunks = text_splitter.split_documents(
            AllDocuments
        )  

        if not chunks:
            return JSONResponse(status_code=400 , content={"message" : "No extractable text found in the uploaded document(s). The PDF may be scanned/image-based."})

        


        vectorDB = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="pdf_documents",
            persist_directory="./chroma_storage"
        )  # stores in vector db

       
        

        retriever = vectorDB.as_retriever(
            search_kwargs={"k": 25 , "filter" : {"session_id" : session_id}}
        )  # return 5 most relevant chunks

      
        if text:
            ReturnedAnswer = retriever.invoke(text)


            if not ReturnedAnswer: 

                return JSONResponse(
                    status_code=400,
                    content={
                        "message": "No relevant information found in the document"
                    }
                )

            # round 2 rerank these 25 chunks

            pairs = []

            for chunk in ReturnedAnswer:
                pairs.append((text , chunk.page_content))  
            scores = reranker.predict(pairs)

            reranked = sorted(zip(ReturnedAnswer , scores) , key=lambda x: x[1] , reverse=True) # it is jsut sorting it from bigger to smaller
            
            TopChunks  = []
            # here tuple contains (doc1 , 0.6) for ex
            for tuplee , score in reranked[:5]:
             TopChunks.append(tuplee)

        
    


            context = "\n\n".join(
                [doc.page_content for doc in TopChunks]
            )
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
context:
{context}

Question:
{text}
"""

            req = llm.invoke(prompt)

            response = JSONResponse(status_code=200 , content={"session_id" : session_id , "question": text , "answer" : req.content})
            response.set_cookie(key="session_id" , value=session_id ,httponly=True,  secure=True, samesite="none",)
            return response
        
       

        response =  JSONResponse(status_code=400, content={  "session_id" :  session_id  , "message":  "Document processed successfully. You can now ask questions about it."})
        print("it has runned successfully")
        response.set_cookie(key="session_id" , value=session_id ,httponly=True,  secure=True, samesite="none",)
        return response

    except Exception as error:

        print(error)
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error"
            }
        )


