# AskPDF — Chat With Your Documents

A full-stack RAG (Retrieval-Augmented Generation) application that lets you upload PDF documents and ask natural-language questions about their content. Answers are generated strictly from the uploaded documents, with a two-stage retrieval pipeline for improved accuracy.

## Features

- 📄 Upload one or more PDF documents
- 💬 Ask questions in natural language and get grounded, context-based answers
- 🔍 Two-stage retrieval: fast vector similarity search followed by cross-encoder reranking for higher relevance
- 🚫 Refuses to hallucinate — if the answer isn't in the document, it says so explicitly
- ⚡ Built on Groq for fast LLM inference

## Tech Stack

**Backend**
- FastAPI — async Python web framework
- LangChain — document loading, chunking, and retrieval orchestration
- ChromaDB — vector database for storing document embeddings (persisted to disk)
- HuggingFace `sentence-transformers` — embedding model (`all-MiniLM-L6-v2`) and cross-encoder reranker (`ms-marco-MiniLM-L-6-v2`)
- Groq (`openai/gpt-oss-120b`) — LLM for answer generation
- PyMuPDF — PDF text extraction

**Frontend**
- React + Vite

## How It Works

1. **Upload** — PDFs are uploaded, saved temporarily, and parsed with PyMuPDF to extract text.
2. **Chunking** — Extracted text is split into overlapping chunks (~500 characters each) for granular retrieval.
3. **Embedding & Storage** — Each chunk is embedded into a vector and stored in a persistent Chroma vector database.
4. **Retrieval (Stage 1)** — When a question is asked, it's embedded and compared against all stored chunks via cosine similarity to fetch the top 25 candidates.
5. **Reranking (Stage 2)** — A cross-encoder model rescores each (question, chunk) pair for precise relevance, and the top 5 are selected.
6. **Answer Generation** — The top chunks are passed as context to the LLM, which is prompted to answer strictly from that context or state that the document doesn't contain enough information.

## Getting Started

### Backend

```bash
cd Server
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

Create a `.env` file inside `Server/`:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run the server:
```bash
uvicorn app:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd Client/AskPdf
npm install
npm run dev
```

## API

**POST `/search`**

`multipart/form-data`
| Field | Type | Required |
|---|---|---|
| `filesparameter` | file(s) | Yes |
| `text` | string | No — omit to just index documents |

- Files only → indexes the document(s), returns a confirmation message
- Files + question → indexes (if new) and returns an answer grounded in the document



## Roadmap

- [ ] Persistent per-user document sessions
- [ ] OCR support for scanned documents
- [ ] Hybrid search (keyword + semantic)
- [ ] Retrieval evaluation pipeline

## License

MIT



what is this  document about
what is  the price of the ticket
"What is the procedure if the flight is cancelled?