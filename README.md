# Bangla RAG System

This project implements a Bangla RAG (Retrieval Augmented Generation) system using FastAPI, Sentence Transformers, ChromaDB, and MySQL. It allows you to query relevant Bengali articles based on a given question.

## Features

- **Article Indexing**: Populates a vector database (ChromaDB) with embeddings of Bengali articles fetched from a MySQL database.
- **Semantic Search**: Retrieves articles semantically similar to a user's query using sentence embeddings.
- **REST API**: Provides a FastAPI endpoint for querying the RAG system.

## Project Structure

- `fastapi_app.py`: The main FastAPI application that exposes the `/query` endpoint.
- `core/rag_service.py`: Contains the BanglaRAG class, which orchestrates the indexing and querying process.
- `core/vectorizer.py`: Handles fetching articles from MySQL and generating sentence embeddings using sentence-transformers.
- `core/chroma_handler.py`: Manages interactions with ChromaDB for storing and retrieving embeddings.
- `requirements.txt`: Lists the Python dependencies.

## Setup

### Prerequisites

- Python 3.7+
- MySQL database with an `articles` table containing `id`, `headline`, and `article_body` columns.
- `DB_CONFIG` (dictionary) containing your MySQL connection details (e.g., host, user, password, database). This needs to be set up in `core/vectorizer.py` and `fastapi_app.py`.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Configuration

Before running the application, you need to configure your MySQL database connection. Open `core/vectorizer.py` and `fastapi_app.py` and set the `DB_CONFIG` variable with your database credentials.

Example `DB_CONFIG`:

```python
DB_CONFIG = {
    "host": "your_mysql_host",
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "database": "your_mysql_database"
}
```

### Indexing Articles

Before you can query the system, you need to index your articles into the ChromaDB vector store. You can do this by running a script or by calling the `index_articles` method from `BanglaRAG` once.

To manually trigger indexing, you could add a temporary block in `fastapi_app.py` or a separate script:

```python
# In fastapi_app.py or a separate script
from core.rag_service import BanglaRAG

rag = BanglaRAG()
# Run this once to populate the database
# rag.index_articles()
```

## Running the Application

To start the FastAPI application:

```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000
```

The API documentation will be available at `http://0.0.0.0:8000/docs` once the server is running.

## API Endpoint

### POST /query

Retrieves relevant articles based on a natural language question.

**Request Body:**

```json
{
    "question": "Your question in Bengali",
    "top_k": 3
}
```

- `question` (string, required): The question to query against the articles.
- `top_k` (integer, optional): The number of top relevant articles to retrieve. Default is 3.

**Example Request (using curl):**

```bash
curl -X POST "http://localhost:8000/query" \
-H "Content-Type: application/json" \
-d '{"question": "বাংলাদেশের রাজধানী কি?", "top_k": 5}'
```

**Example Response:**

```json
{
    "query": "বাংলাদেশের রাজধানী কি?",
    "results": [
        {
            "id": "123",
            "score": 0.15,
            "text": "ঢাকা বাংলাদেশের রাজধানী। এটি বুড়িগঙ্গা নদীর তীরে অবস্থিত...",
            "metadata": {
                "source": "mysql"
            },
            "full_article": {
                "id": 123,
                "headline": "ঢাকা: বাংলাদেশের রাজধানী",
                "article_body": "ঢাকা বাংলাদেশের রাজধানী এবং বৃহত্তম শহর। এটি একটি মেগাসিটি এবং দক্ষিণ এশিয়ার অন্যতম প্রধান শহর।..."
            }
        }
        // ... more results
    ]
}
```

## Dependencies

- **fastapi**: Web framework for building APIs.
- **uvicorn**: ASGI server for running FastAPI applications.
- **sentence-transformers**: For generating sentence embeddings.
- **chromadb**: Vector database for storing and retrieving embeddings.
- **mysql-connector-python**: MySQL database connector for Python.
- **python-multipart**: For handling form data (dependency of FastAPI).
- **numpy**: Numerical computing library (used by sentence-transformers).