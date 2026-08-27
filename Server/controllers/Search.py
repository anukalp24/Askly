from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


async def searchController(files, text):

    AllDocuments = []

    try:

        for file in files:

            print(file.filename)

            loader = PyMuPDFLoader(
                str(pdf_file)
            )  # we need to convert the path object into string before sending it to PyMuPDFLoader

            document = loader.load()

            for doc in document:

                doc.metadata["source_file"] = files.name

            AllDocuments.extend(document)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len
        )  # its just a tool/rules

        chunks = text_splitter.split_documents(
            AllDocuments
        )  # it actually creates chunks and returns an array of chunks

        # A chunk internally contains two main things:

        # python
        # Document(
        #     page_content="...",   # the actual text
        #     metadata={...}       # extra info about where this text came from
        # )

        # sentence transformers creates the embeddings

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorDB = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="pdf_documents"
        )  # stores in vector db

        # vector db stores the original chunks, embeddings and metadata of that chunk

        retriever = vectorDB.as_retriever(
            search_kwargs={"k": 5}
        )  # return three most relevant chunks

        if text:

            docs = retriever.invoke(
                text
            )  # this line says hey retriever go find the relevant chunks
              # and it will return those chunks
              # it will return stored text known as page_content
              # and metadata

            if not docs:

                return JSONResponse(
                    status_code=400,
                    content={
                        "message": "No relevant information found in the document"
                    }
                )

            context = "\n\n".join(
                [doc.page_content for doc in docs]
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

            print(response.content)

        print(document)

    except Exception as error:

        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error"
            }
        )

        print(error)