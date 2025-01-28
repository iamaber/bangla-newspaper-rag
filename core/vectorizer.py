from sentence_transformers import SentenceTransformer
import mysql.connector
import numpy as np

class Vectorizer:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        
    def generate_embeddings(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)
    
    def get_articles(self, batch_size=100):
        """Fetch articles from MySQL in batches"""
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        offset = 0
        while True:
            cursor.execute(
                "SELECT id, headline, article_body FROM articles LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                break
                
            yield batch
            offset += batch_size
            
        conn.close()