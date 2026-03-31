# CodeSage — Ingestion + Parsing + Embeddings (API Only)

CodeSage is a modular backend that ingests a source-code repository, parses it into structured code units (functions/classes/modules), and generates **function-level embeddings** for semantic search and downstream RAG. [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

This repository currently implements:

*   ✅ **Repository Ingestion Layer** (clone/pull repo, scan files) [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   ✅ **Parsing Layer** (Python AST → structured units) [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   ✅ **Code Representation & Embedding Layer** (function-level representation + embeddings) [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   ✅ **Persistence** (SQLite by default; configurable DB URL) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   ✅ **FastAPI endpoints** to ingest, browse, embed, and delete/purge data [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Table of Contents

*   \#architecture-overview
*   \#requirements
*   \#install--run
*   \#demo-script-presentation-ready
*   \#python-ast-parsing-what-it-extracts--how-to-demo
*   \#embeddings
*   \#api-reference-endpoints
*   \#configuration
*   \#data--storage
*   \#project-structure
*   \#roadmap

***

## Architecture Overview

### Current data flow

1.  **Ingest** repo URL → clone/pull to local storage [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
2.  **Walk files** → detect language (currently focuses on Python parsing) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
3.  **Parse Python** → extract code units (module/class/function) + metadata + snippet [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
4.  **Represent** each unit as stable text format (type/qualname/signature/file/docstring/code) [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
5.  **Embed** representations → store vectors in DB as float32 blobs [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Design choice: function-level embeddings

Primary embedding granularity is **function-level** for better semantic precision and retrieval quality, aligned to the system design. [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Requirements

*   Python **3.10+** (recommended: 3.11/3.12 for best ML dependency compatibility) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   Git installed (for cloning repositories via GitPython) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

Optional (for Transformer embeddings):

*   `torch`
*   `transformers` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Install & Run

### 1) Create and activate a virtual environment

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install the package (editable)

```bash
pip install -U pip
pip install -e .
```

This installs the backend dependencies and makes the `codesage` package importable by Uvicorn. [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### 3) (Optional) Enable Transformer embedding support

```bash
pip install -e ".[embeddings]"
```

If Transformer dependencies are not available/compatible in your environment, the system can still embed using a deterministic fallback embedder. [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### 4) Run the API

```bash
uvicorn codesage.api.main:app --reload
```

Open Swagger UI:

*   <http://127.0.0.1:8000/docs> [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Demo Script (Presentation Ready)

This is a **clean, reliable live demo flow** you can follow on stage. It’s designed to show:

1.  ingestion, 2) parsing outputs, 3) embeddings, 4) delete/purge.

### Demo Setup (before presenting)

*   Have the API running:

```bash
uvicorn codesage.api.main:app --reload
```

*   Open Swagger UI:
    *   `http://127.0.0.1:8000/docs` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

### Demo Part 1 — Ingest a repo (60–90 seconds)

**Talking point:**  
“First, we ingest a real repository. The system clones/pulls it locally, walks files, detects language, and parses Python into structured units.” [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

**Command:**

```bash
curl -X POST http://127.0.0.1:8000/ingest/repo \
  -H "Content-Type: application/json" \
  -d "{\"repo_url\":\"https://github.com/pallets/flask.git\"}"
```

**Expected response:**

```json
{ "repo_id": "<repo_id>" }
```

Copy the `repo_id` for the next steps. [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

### Demo Part 2 — Show what the parser produced (2–3 minutes)

**Talking point:**  
“The ingestion layer outputs structured code units — functions, classes, and module docs — with file paths and line ranges. This is the clean contract that downstream embeddings and retrieval depend on.” [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

1.  List repos:

```bash
curl http://127.0.0.1:8000/repos
```

2.  List Python files:

```bash
curl "http://127.0.0.1:8000/repos/<repo_id>/files?language=python&limit=20"
```

3.  List extracted functions (show function-level granularity):

```bash
curl "http://127.0.0.1:8000/repos/<repo_id>/units?type=function&limit=10"
```

4.  Pick a `unit_id` from the response and fetch the full snippet:

```bash
curl "http://127.0.0.1:8000/units/<unit_id>"
```

**What to highlight on screen:**

*   `unit_type` (function/class/module)
*   `qualname` and `signature`
*   `start_line` / `end_line`
*   `docstring`
*   `code` snippet

This proves parsing created **structured + queryable** code units. [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

### Demo Part 3 — Generate embeddings (2 minutes)

**Talking point:**  
“Now we convert each code unit into a stable representation string and generate embeddings at function-level granularity, stored in the database for retrieval.” [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

**Option A: Transformer embeddings (recommended if available)**

```bash
curl -X POST "http://127.0.0.1:8000/embed/repos/<repo_id>" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"microsoft/codebert-base\",\"batch_size\":8,\"force\":false}"
```

**Option B: Fallback embeddings (no ML dependencies)**

```bash
curl -X POST "http://127.0.0.1:8000/embed/repos/<repo_id>" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"hash-embedder-384\",\"batch_size\":32,\"force\":false}"
```

Then show stats:

```bash
curl "http://127.0.0.1:8000/repos/<repo_id>/embeddings?model=microsoft/codebert-base"
```

And show one unit’s embedding preview:

```bash
curl "http://127.0.0.1:8000/units/<unit_id>/embedding?model=microsoft/codebert-base"
```

**What to highlight:**

*   Count of embeddings
*   Embedding dimension (`dim`)
*   `vector_preview` (first few values)
*   `content_hash` (ties embeddings to exact code version)

This demonstrates a complete ingestion → parsing → embedding pipeline. [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

### Demo Part 4 — Delete / Purge (30–60 seconds)

**Talking point:**  
“Ingestion is reversible — we can delete one repo’s metadata and optionally its cloned folder, or purge everything for clean re-runs.” [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

Delete one repo:

```bash
curl -X DELETE "http://127.0.0.1:8000/repos/<repo_id>?delete_clone=true"
```

Purge all:

```bash
curl -X DELETE "http://127.0.0.1:8000/repos?delete_clones=true"
```

 [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Python AST Parsing (What It Extracts + How to Demo)

This section lists **exact parsing capabilities** and the best way to **show each capability** live.

### What the Python AST parser extracts

For each Python file, the parser can extract:

1.  **Module-level docstring** (stored as a `module` unit) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
2.  **Top-level functions** (`def f(...)`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
3.  **Async functions** (`async def f(...)`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
4.  **Classes** (`class C:`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
5.  **Methods inside classes** (as `function` units with qualified names) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
6.  **Nested functions** (functions defined inside other functions; qualified name reflects nesting) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
7.  **Qualified name (`qualname`)** reflecting nesting scope (e.g., `ClassName.method`, `outer.inner`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
8.  **Best-effort signature formatting** (function name + argument list) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
9.  **Line ranges** (`start_line`, `end_line`) for precise citation and UI highlighting [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
10. **Docstrings** for module/functions/classes (if present) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
11. **Raw code snippet** exactly for that unit (used for embedding and later citations) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

> Output contract: each parsed unit has metadata + a stable snippet for downstream embedding/retrieval/RAG. [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

### How to demonstrate parsing features in the UI / API

#### 1) Show all unit types (module/class/function)

```bash
curl "http://127.0.0.1:8000/repos/<repo_id>/units?limit=50"
```

Then filter by type:

```bash
curl "http://127.0.0.1:8000/repos/<repo_id>/units?type=module&limit=20"
curl "http://127.0.0.1:8000/repos/<repo_id>/units?type=class&limit=20"
curl "http://127.0.0.1:8000/repos/<repo_id>/units?type=function&limit=20"
```

 [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

**What to say:**  
“Here we can see the parser emits structured units by type, which makes indexing and retrieval consistent.” [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

#### 2) Show `qualname` (class methods & nesting)

List functions and look at `qualname` values:

```bash
curl "http://127.0.0.1:8000/repos/<repo_id>/units?type=function&limit=50"
```

 [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

**What to point out:**

*   `qualname` like `SomeClass.method_name`
*   nested patterns like `outer.inner`

This proves the parser captures **structure**, not just text. [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify), [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate)

***

#### 3) Show docstring extraction

Pick a `unit_id` that has a docstring and fetch full details:

```bash
curl "http://127.0.0.1:8000/units/<unit_id>"
```

Then highlight:

*   `"docstring": "..."`

This is important because docstrings boost both explanation quality and embedding relevance. [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

#### 4) Show precise line ranges

Using the same `GET /units/<unit_id>` response, highlight:

*   `start_line`
*   `end_line`

**What to say:**  
“These line ranges are what enable citations later — we can point the user to exact file + line spans.” [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

#### 5) Show the extracted code snippet matches the source

In the unit response:

*   `code` contains the exact snippet for that unit

**What to say:**  
“This is the canonical snippet that gets embedded and later retrieved for RAG answers.” [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

#### 6) Show search/filtering behavior (great quick win)

Use substring query:

```bash
curl "http://127.0.0.1:8000/repos/<repo_id>/units?type=function&q=route&limit=20"
```

This demonstrates unit-level querying and sets you up for retrieval features later. [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify), [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate)

***

## Embeddings

### Representation format

Each `CodeUnit` is converted into a stable embedding string that includes:

*   `TYPE`, `QUALNAME`, `SIGNATURE`
*   `FILE` (optional)
*   `DOCSTRING` (if present)
*   `CODE` snippet [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate), [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Embedders

*   **Transformer embedder** (optional): uses HuggingFace models when available [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   **Fallback embedder**: deterministic vectors for end-to-end pipeline without model downloads [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Idempotency

Embeddings are stored with `(unit_id, model, content_hash)` uniqueness so unchanged code is not redundantly re-embedded. [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## API Reference (Endpoints)

### Ingestion

*   `POST /ingest/repo`  
    Body: `{ "repo_url": "https://..." }` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `POST /ingest/local`  
    Body: `{ "local_path": "/path/to/folder" }` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Browse

*   `GET /repos` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `GET /repos/{repo_id}` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `GET /repos/{repo_id}/files?language=python&limit=200` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `GET /repos/{repo_id}/units?type=function&q=search&limit=200` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `GET /units/{unit_id}` (includes full code snippet) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Embeddings

*   `POST /embed/repos/{repo_id}` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `GET /repos/{repo_id}/embeddings?model=...` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `GET /units/{unit_id}/embedding?model=...` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Delete / Purge

*   `DELETE /repos/{repo_id}?delete_clone=true|false` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `DELETE /repos?delete_clones=true|false` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Configuration

Environment variables (prefix: `CODESAGE_`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Storage / DB

*   `CODESAGE_DB_URL` (default: `sqlite:///./codesage.db`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `CODESAGE_DATA_DIR` (default: `./.data`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Embeddings

*   `CODESAGE_EMBEDDING_MODEL` (default: `microsoft/codebert-base`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `CODESAGE_EMBEDDING_MAX_LENGTH` (default: `256`) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

Example:

```bash
export CODESAGE_DB_URL="sqlite:///./my_codesage.db"
export CODESAGE_DATA_DIR="./my_data"
export CODESAGE_EMBEDDING_MODEL="microsoft/codebert-base"
export CODESAGE_EMBEDDING_MAX_LENGTH=256
```

 [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Data & Storage

### Default locations

*   SQLite DB: `./codesage.db` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   Cloned repos: `./.data/repos/<repo_id>/` [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

### Core tables

*   `repos` — repo identity + local clone path [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `files` — file inventory (path, language, size) [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `code_units` — parsed functions/classes/modules with metadata + snippet [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)
*   `code_unit_embeddings` — embedding vectors (float32 blob) + model + hash [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Project Structure

    codesage/
      api/
        main.py
        routes.py
        schemas.py
      core/
        config.py
        logging.py
      db/
        session.py
        models.py
        init_db.py
      ingestion/
        git_client.py
        file_walker.py
        language.py
      parsing/
        python_ast.py
        registry.py
      embeddings/
        representation.py
        hf_embedder.py
        hash_embedder.py
        registry.py
      pipeline/
        ingest_parse.py
        embed_repo.py
        delete_repo.py
    tests/

 [\[stackoverflow.com\]](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

***

## Roadmap

Next planned layers:

*   Multi-language parsing with Tree-sitter [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate)
*   Hybrid retrieval (BM25 + vector search) + reranking [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate)
*   RAG generation with grounded citations (file + line refs) [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate)
*   UI & visualization (snippet highlighting + graphs) [\[stackoverflow.com\]](https://stackoverflow.com/questions/30405867/how-can-i-get-python-requests-to-trust-a-self-signed-ssl-certificate)