# Canva Assistant – Agentic RAG System

## Testing the branch changes

## Testing the branch changes 2

## Changes made in the branch 2

## Overview

Canva Assistant is a fully agentic RAG (Retrieval-Augmented Generation) system designed to help users navigate and use the Canva platform through step-by-step, visual-aware guidance. The assistant extracts instructional content from Canva UI walkthroughs (images/screenshots), generates structured markdown with LLMs, stores it in a vector database, and answers user queries with evidence-backed, well-cited guidance.

## AI Frameworks Used

### What We Use:

- **LlamaIndex Parser**  
  Used for parsing and converting PDFs into images and markdown format (`Data/parse.py`).

- **LangChain (Text Splitter Only)**  
  We use LangChain’s `RecursiveCharacterTextSplitter` in `Data/embeddings.py` to chunk the cleaned text into overlapping windows. This preserves semantic coherence across chunks without introducing complexity.

### What We Don’t Use:

We **do not** use LlamaIndex or LangChain for RAG orchestration, agent logic, memory, or retrieval workflows.

### Why We Avoided Full Framework Abstractions:

- ✅ **Full Transparency & Debuggability**  
  Custom Python gives us end-to-end visibility over prompt construction, response streaming, memory updates, and function-calling flows.

- ✅ **Agentic Flexibility**  
  With core logic fully in Python (`backend/core/`), we can fine-tune the control flow of LLM reasoning, retrieval invocation, and response formatting — something frameworks often abstract away or constrain.

- ✅ **Less Overhead**  
  Reduced dependencies, lower cold-start time, and easier deployment, especially on minimal hosting environments like Render or simple containers.

- ✅ **Better Prompt Discipline**  
  Frameworks often bundle defaults or implicit behavior; our approach guarantees strict prompt enforcement through `prompt.py`.

- ✅ **RAG-as-Code Philosophy**  
  We treat RAG not as a black box, but as a programmable pipeline — this philosophy keeps the stack lightweight, auditable, and extensible.

In short, we treat frameworks as utilities, not as architecture. This gives us the best of both worlds: ergonomic tools for preprocessing, and total control for reasoning and retrieval.

## Architecture

### 1. Data Pipeline

**a. Image Extraction & OCR**

- Canva documents (PDFs or images) are converted to images and stored in `Data/images/` and `Data/images2/`.
- gpt 4.1 is used to process `Data/images/`these images to extract text content for each page or section.
- Extracted text is saved as markdown files in `Data/markdowns/`.

**b. Markdown Refinement**

- [`Data/refine.py`](Data/refine.py) (if present) or manual review is used to clean and structure the OCR-extracted markdown into chunk-friendly plain text.

**c. Embedding & Vector Storage**

- [`Data/embeddings.py`](Data/embeddings.py) splits the cleaned OCR text into overlapping chunks.
- Each chunk is embedded using OpenAI's `text-embedding-3-small` model.
- Chunks and embeddings are uploaded to a Supabase vector table (`markdown_docs`).

---

### 2. Backend (API & RAG Logic)

**a. FastAPI Server**

- Entrypoint: [`backend/main.py`](backend/main.py)
- Includes chat and reset endpoints via [`backend/router/chat.py`](backend/router/chat.py).
- Serves the frontend static files from [`backend/frontend/`](backend/frontend/).

**b. Chat Routing**

- `/chat` endpoint streams LLM responses.
- `/reset_chat` resets session memory.

**c. Core Modules**

- **Prompt Engineering:** [`backend/core/prompt.py`](backend/core/prompt.py) defines a strict system prompt to ensure evidence-based, canva related responses.
- **Session Memory:** [`backend/core/memory.py`](backend/core/memory.py) manages per-session chat history, always starting with the system prompt.
- **Agent Loop:** [`backend/core/agent.py`](backend/core/agent.py) handles LLM streaming, OpenAI function-calling, and memory updates.
- **Function Calling:** [`backend/core/specs.py`](backend/core/specs.py) defines the `canva_doc_search` function for retrieval.
- **Function Handler:** [`backend/core/handler.py`](backend/core/handler.py) executes semantic search when the LLM requests it.
- **Semantic Search:** [`backend/utils/query.py`](backend/utils/query.py) computes query embeddings and calls a Supabase RPC to retrieve top-matching chunks.

---

### 3. Frontend

**a. UI**

- Located in [`backend/frontend/`](backend/frontend/)
- Modern chat interface with suggestion chips, markdown rendering, and streaming responses.
- [`backend/frontend/index.html`](backend/frontend/index.html): Main HTML structure.
- [`backend/frontend/style.css`](backend/frontend/style.css): Responsive, modern CSS.
- [`backend/frontend/script.js`](backend/frontend/script.js): Handles chat logic, session management, and streaming updates.

---

## Setup & Run Instructions

### Prerequisites

- Python 3.11+
- Node.js (for frontend, optional)
- Supabase project with `markdown_docs` table and `match_markdown_chunks` RPC
- OpenAI API key
- LlamaParse API key

### 1. Environment Setup

1. Clone the repo.
2. Fill in `.env` with your OpenAI, Supabase, and LlamaParse credentials.

### 2. Data Preparation

1. Place raw PDFs in `Data/rawPdf/`.
2. Run PDF parsing:
   ```sh
   python Data/parse.py
   ```
3. Unrelated or noisy images (e.g., UI logos, repeated backgrounds, etc.), manually move them from `Data/images/` to `Data/images2` to exclude them from further processing.
4. Use the following script to generate detailed step-by-step Markdown instructions from instructional images:
   ```sh
   python Data/refine.py
   ```
5. Generate embeddings and upload the markdowns to Supabase:
   ```sh
   python Data/embeddings.py
   ```

### 3. Backend

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Start the app by running the FastAPI server from the root of the `backend/` directory:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   This serves both the backend API and the frontend UI.
   The static frontend is automatically served from `backend/frontend/`, so there’s no need to run a separate frontend server.

### 4. Frontend

Once running, visit: http://localhost:8000

---

## Architectural Decisions

### Retrieval-Augmented Generation (RAG)

- **Why RAG?**  
  Ensures all answers are grounded in actual documents, preventing hallucinations and ensuring compliance.

- **Chunking & Embedding:**  
  Cleaned, chunked text enables fine-grained retrieval and evidence citation.

- **Supabase Vector Store:**  
  Chosen for easy integration, scalable storage, and fast similarity search via custom RPC.

- **OpenAI Function Calling:**  
  Lets the LLM decide when to retrieve evidence, keeping the system flexible and future-proof.

- **Strict Prompting:**  
  The system prompt in [`backend/core/prompt.py`](backend/core/prompt.py) enforces scope, style, and evidence requirements, minimizing off-topic or speculative responses.

- **Session Memory:**  
  Each chat session is isolated, always starting with the system prompt, ensuring context consistency.

- **Streaming Responses:**  
  Both backend and frontend are designed for streaming, providing a responsive user experience.

- **Frontend Simplicity:**  
  The frontend is static, dependency-light, and uses `marked.js` for markdown rendering, ensuring compatibility and ease of deployment.

---

## Example Conversations

Below are some sample interactions between users and the assistant
<img width="1507" alt="image" src="https://github.com/user-attachments/assets/9d29a006-8788-4514-921e-802e7d20ba0b" />
<img width="1471" alt="image" src="https://github.com/user-attachments/assets/ae36e7e3-bef3-4428-b2d7-e8fefc34bf65" />
<img width="1510" alt="image" src="https://github.com/user-attachments/assets/429eebf6-51a0-4faa-9c3a-edabda6c3cd5" />

These examples demonstrate:

- Precise retrieval of details (e.g. steps, locations of elements)
- Rejecting questions which are not relevant to the use case
- Structured formatting and chunk-aware responses
- Real-time streaming feedback in the frontend with sources of the answers
- Also have memory for individual chats as can be seen in the 3rd image

## File Reference

- **Data Pipeline:**

  - [`Data/parse.py`](Data/parse.py)
  - [`Data/embeddings.py`](Data/embeddings.py)
  - [`Data/images/`](Data/cleaned/images/)
  - [`Data/images2/`](Data/cleaned/images2/)
  - [`Data/markdowns/`](Data/markdowns/)

- **Backend:**

  - [`backend/main.py`](backend/main.py)
  - [`backend/router/chat.py`](backend/router/chat.py)
  - [`backend/core/`](backend/core/)
  - [`backend/utils/query.py`](backend/utils/query.py)

- **Frontend:**
  - [`backend/frontend/index.html`](backend/frontend/index.html)
  - [`backend/frontend/style.css`](backend/frontend/style.css)
  - [`backend/frontend/script.js`](backend/frontend/script.js)

---
