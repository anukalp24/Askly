from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import tempfile
import os
from pathlib import Path
from sentence_transformers import CrossEncoder
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
async def searchController(files, text):

    AllDocuments = []
    print(" search - controller running")

    try:

        for file in files:
# each file is an uplaod file obeject
            print(file.filename)
            suffix = Path(file.filename).suffix

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_path = tmp.name

            try:
                loader = PyMuPDFLoader(tmp_path)

                document = loader.load()

                for doc in document:

                    doc.metadata["source_file"] = file.filename

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
        )  # it actually creates chunks and returns an array of chunks

        if not chunks:
            return JSONResponse(status_code=400 , content={"message" : "No extractable text found in the uploaded document(s). The PDF may be scanned/image-based."})

        # A chunk internally contains two main things:

        # python
        # Document(
        #     page_content="...",   # the actual text
        #     metadata={...}       # extra info about where this text came from
        # )

        # sentence transformers creates the embeddings


        vectorDB = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="pdf_documents",
            persist_directory="./chroma_storage"
        )  # stores in vector db

        # vector db stores the original chunks, embeddings and metadata of that chunk

        retriever = vectorDB.as_retriever(
            search_kwargs={"k": 25}
        )  # return 5 most relevant chunks

        # round-1 do similarity search and find the top 25 chunks which is closest to the question vector numbers
        if text:
            ReturnedAnswer = retriever.invoke(text)
# ReturnedAnswer = [
#     Document(...),   # chunk 1
#     Document(...),   # chunk 2
#     Document(...),   # chunk 3
#     ...
#     Document(...)    # chunk 25
# ]

                
          # this line says hey retriever go find the relevant chunks
              # and it will return those chunks
              # it will return stored text known as page_content
              # and metadata

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

            reranked = sorted(zip(ReturnedAnswer , scores) , key=lambda x: x[1] , reverse=True)

            TopChunks  = []
            # here tuple contains (doc1 , 0.6) for ex
            for tuplee , score in reranked[:5]:
             TopChunks.append(tuplee)
            #  and here we are jsut addign the  doc  not the score

            
# ReturnedAnswer = [doc1, doc2, doc3, ...]
# scores =         [0.2, 0.9, 0.5, ...]

# zip(ReturnedAnswer, scores) → [(doc1, 0.2), (doc2, 0.9), (doc3, 0.5), ...]

# reranked = [
#     (doc2, 0.9),   # highest score, now first
#     (doc3, 0.5),
#     (doc1, 0.2),   # lowest score, now last
# ]


            context = "\n\n".join(
                [doc.page_content for doc in TopChunks]
            )

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
{text}
"""

            response = llm.invoke(prompt)
            return JSONResponse(status_code=200, content={"answer": response.content})

        return JSONResponse(status_code=200, content={"message":  "your documents are  processed  successfully , now u can ask questions related to it"})

    except Exception as error:

        print(error)
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error"
            }
        )


# very imp mental mode
#     Way 1 (what your embedding model does — Stage 1):

# Step A: turn question into a number (alone)
# Step B: turn chunk into a number (alone)  
# Step C: compare those two numbers afterward (cosine similarity)

# Here, "comparing" is a distinct, separate step — happens after both are already converted to numbers.

# Way 2 (what the cross-encoder does — Stage 2):

# Step A: feed question + chunk together into the model
# Step B: the model internally reads both, weighs how they relate to each other, and outputs ONE number directly