import chromadb
from chromadb.config import Settings

class ChromaManager:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=".chromadb"
        ))
        
        self.collection = self.client.get_or_create_collection(
            name="bangla_articles",
            metadata={"hnsw:space": "cosine"}
        )
    
    def store_embeddings(self, ids, embeddings, documents, metadata):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata
        )