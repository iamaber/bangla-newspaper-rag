from fastapi import FastAPI
from pydantic import BaseModel
from core.rag_service import BanglaRAG

app = FastAPI()
rag = BanglaRAG()

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

@app.post("/query")
async def handle_query(req: QueryRequest):
    results = rag.query(req.question, req.top_k)
    
    # Get full article details from MySQL
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    for result in results:
        cursor.execute(
            "SELECT * FROM articles WHERE id = %s",
            (int(result['id']),)
        )
        article = cursor.fetchone()
        result['full_article'] = article
    
    conn.close()
    
    return {
        "query": req.question,
        "results": results
    }