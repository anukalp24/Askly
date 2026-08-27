# from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader, DirectoryLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from pathlib import Path
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv

# load_dotenv()
# llm = ChatGroq(
#     model="openai/gpt-oss-120b",
#     temperature=0
# )
# # LangChain gives you standardized interfaces and utilities for things like:


# st.title("AskMyPDF")
# def pdf(pdf_directory):
#     AllDocuments = []
#     pdf_dir = Path(pdf_directory)
#     #  path converts the plain string pdf directory into a path obejct so u can call glob()
#     # print(type(pdf_dir))
#     # print(pdf_dir)

#     # we need to wrap it in a list cause then only we can see the file names
#     pdf_files = list(pdf_dir.glob("**/*.pdf"))
#     # .glob() is a method that only exists on Path objects thats why we convert the directory into path object
#     # print(pdf_files)  it will return this [
#     # WindowsPath('../data/report.pdf'),
#     # WindowsPath('../data/notes.pdf')
#     # ]

#     try:
#         for pdf_file in pdf_files:
#             print(pdf_file.name)
#             loader = PyMuPDFLoader(str(pdf_file))  # we need to conevrt the apth obj into stricng before sending it to PyMuPDFLoader
#             document = loader.load()

#             for doc in document:
#                 doc.metadata["source_file"] = pdf_file.name 8 

#             AllDocuments.extend(document)

#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100, separators=["\n\n", "\n", ". ", " ", ""], length_function=len)  # its just a tool/rules

#         chunks = text_splitter.split_documents(AllDocuments)  # it actually creates chunks and return a array of chunks

#         #      A chunk internally contains two main things:

#         # python
#         # Document(
#         #     page_content="...",   # the actual text
#         #     metadata={...}         # extra info about where this text came from
#         # )
#         # sentence tranformers creates the embedding        s
#         embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#         vectorDB = Chroma.from_documents(documents=chunks, embedding=embeddings, collection_name="pdf_documents")  # stores in vector db

#         # vector db stores the  original chunks , embeddings and meta data which of that chunk
#         retriever = vectorDB.as_retriever(search_kwargs={"k": 5})  # return three most relevant chunks

#         question = st.text_input("Ask a Question")
#         if question:
#             docs = retriever.invoke(question)    # this line says hey retriever go find the relevant  chunks and it will return those chunks
#                         # # it will return stred text knwos as page content which is original chunk text  and meta data
            

#             if not docs:
#                 st.write("No relevant information found in the document") 

               
#             context = "\n\n".join([doc.page_content for doc in docs])
#             prompt = f"""You are a precise, factual assistant that answers questions strictly based on the provided document context. You never use outside knowledge, even if you know the answer.
    
# # Rules:
# # 1. Answer ONLY using information explicitly stated in the context below.
# # 2. If the context does not contain enough information to answer, respond exactly with: "The document doesn't contain enough information to answer this question."
# # 3. Do not guess, infer beyond what's written, or add information not present in the context.
# # 4. Keep your answer clear and concise — no unnecessary preamble like "Based on the context provided."
# # 5. If helpful, quote or closely reference the specific part of the context that supports your answer.


# # context:{context}
# # Question:{question}
# #         """
#             response = llm.invoke(prompt)
#             st.write(response.content)

#             print(document)
#     except Exception as error:
#         st.error(str(error))
#         print(error)
#         continue
#     # # ex how documents are stored inside a list:-
#     # # Resume = 1 page
#     # # Health = 5 pages
#     # # then after both:
#     # # AllDocuments = 6 Document objects
#     # # see docuemnt is one array which will consit of many docuemnt  as per page

# pdf("data")  # function calling


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app  = FastAPI()

app.add_middleware(
    CORSMiddleware ,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






 