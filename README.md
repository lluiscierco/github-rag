# RAG-Based Codebase Q&A System - Backend

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

This repository contains the backend service for a Retrieval-Augmented Generation (RAG) application.  
It enables ingestion of any public GitHub repository, processes its code files into a searchable vector store, and provides natural language Q&A capabilities over the codebase.

The backend is built with **FastAPI**, delivering a robust, asynchronous, and scalable API for frontend consumption.

---

## ✨ Features

- **GitHub Repository Ingestion:** Ingest code from any public GitHub repository via a simple API call.
- **Configurable Data Processing:** Customize file filtering (by extension), text splitting strategy, chunk size, and chunk overlap.
- **Vectorization and Storage:** Automatically chunk source code, create vector embeddings, and store them in a Pinecone vector database.
- **RAG Q&A Pipeline:** Query the ingested codebase using a Large Language Model (LLM) enhanced with retrieved contextual embeddings.
- **Asynchronous API:** High performance and concurrency with FastAPI.
- **CORS Enabled:** Allows frontend requests smoothly.

---

## 🛠️ Technology Stack

- **Framework:** FastAPI  
- **LLM Orchestration:** LangChain  
- **LLM:** Google Gemini (via `GOOGLE_API_KEY`)  
- **Embedding Model:** Hugging Face Hub model (via `HUGGINGFACE_KEY`)  
- **Vector Database:** Pinecone  
- **Server:** Uvicorn ASGI server

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+  
- Package manager (pip)  
- API keys for GitHub, Hugging Face, Pinecone, and Google

### 2. Installation & Setup

```bash
git clone https://github.com/lluiscierco/github-rag.git
cd github-rag
```
Create and activate a virtual environment:

```bash
# Unix/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```
Install dependencies:

```bash
pip install -r requirements.txt
```
Set up environment variables:

```bash
cp .env.example .env
```
Edit .env with your credentials:

```env
# GitHub API key (for higher rate limits)
GITHUB_KEY="ghp_..."

# Hugging Face API key (for embedding models)
HUGGINGFACE_KEY="hf_..."

# Pinecone API key and index name
PC_KEY="your-pinecone-api-key"
PC_INDEX="your-pinecone-index-name"

# Google API key for Gemini LLM
GOOGLE_API_KEY="your-google-api-key"
```
### 3. Running the Server
Start the FastAPI server with Uvicorn:

```bash
uvicorn app.main:app --reload
Server URL: http://127.0.0.1:8000
```
Hot-reloading enabled for development

Interactive API docs: http://127.0.0.1:8000/docs

## 📚 API Endpoints
### Health Check
- Endpoint: /

- Method: GET

- Description: Verify server is running

Success Response:

```json
{
  "message": "RAG Backend is running. Use /ingest-github-repo or /query-rag."
}
```
### Ingest GitHub Repository
- Endpoint: /ingest_github_repo/

- Method: POST

- Description: Clone a GitHub repo, process files, and upload embeddings

Request Body Example:

```json
{
  "repo_name": "langchain-ai/langchain",
  "branch": "master",
  "filter_file_extension": [".py", ".md"],
  "chunk_size": 1000,
  "chunk_overlap": 100,
  "splitter": "RecursiveCharacterTextSplitter"
}
```
Success Response:

```json
{
  "message": "Ingestion successful. 1542 chunks uploaded to the vector store",
  "chunk_length": 1542
}
```
Error Responses:

- 400 Bad Request — Invalid input parameters

- 500 Internal Server Error — Failure during ingestion

### Query the RAG Pipeline
- Endpoint: /query-rag/

- Method: POST

- Description: Query the ingested codebase with natural language

- Request Body Example:

```json
{
  "question": "What is the purpose of the LCEL Runnables?"
}
```
Success Response:

```json
{
  "message": "RAG answering successful.",
  "Answer": "LCEL Runnables are the core components of the LangChain Expression Language..."
}
```
Error Responses:

- 400 Bad Request — Invalid question input

- 500 Internal Server Error — Failure generating an answer

Feel free to contribute or report issues!

Made with 💙 by Lluis Cierco
