class BanglaRAG:
    def __init__(self):
        self.vectorizer = Vectorizer()
        self.chroma = ChromaManager()
        
    def index_articles(self):
        """Populate vector database"""
        article_gen = self.vectorizer.get_articles()
        
        for batch in article_gen:
            texts = [f"{art['headline']} {art['article_body'][:500]}" 
                    for art in batch]
            embeddings = self.vectorizer.generate_embeddings(texts)
            
            self.chroma.store_embeddings(
                ids=[str(art['id']) for art in batch],
                embeddings=embeddings.tolist(),
                documents=texts,
                metadata=[{"source": "mysql"} for _ in batch]
            )
    
    def query(self, question, top_k=5):
        """Retrieve relevant articles"""
        query_embedding = self.vectorizer.generate_embeddings([question])[0]
        
        results = self.chroma.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        return self._format_results(results)

    def _format_results(self, chroma_results):
        """Convert Chroma results to usable context"""
        return [{
            'id': chroma_results['ids'][0][i],
            'score': chroma_results['distances'][0][i],
            'text': chroma_results['documents'][0][i],
            'metadata': chroma_results['metadatas'][0][i]
        } for i in range(len(chroma_results['ids'][0]))]