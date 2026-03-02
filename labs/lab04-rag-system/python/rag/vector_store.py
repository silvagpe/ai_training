"""Vector Store implementation using ChromaDB."""
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional
import os
import hashlib


class LightweightHashEmbeddingFunction:
    """Small deterministic embedding function without heavy ML dependencies."""

    def __init__(self, dim: int = 384):
        self.dim = dim

    def __call__(self, input: List[str]) -> List[List[float]]:
        vectors = []
        for text in input:
            vector = [0.0] * self.dim
            tokens = text.lower().split()
            if not tokens:
                vectors.append(vector)
                continue

            for token in tokens:
                digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
                idx = int(digest[:8], 16) % self.dim
                sign = 1.0 if int(digest[8:10], 16) % 2 == 0 else -1.0
                vector[idx] += sign

            norm = sum(v * v for v in vector) ** 0.5
            if norm > 0:
                vector = [v / norm for v in vector]

            vectors.append(vector)
        return vectors


class CodebaseVectorStore:
    """Vector store for code embeddings using ChromaDB."""

    def __init__(
        self,
        collection_name: str = "codebase",
        persist_directory: str = "./chroma_db"
    ):
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Use OpenAI embeddings when key is available.
        # Otherwise fallback to a lightweight local embedding (no heavy ML deps).
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key,
                model_name="text-embedding-3-small"
            )
        else:
            print("OPENAI_API_KEY not set. Using lightweight local hash embeddings.")
            self.embedding_fn = LightweightHashEmbeddingFunction(dim=384)

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """Add documents to the vector store."""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> List[Dict]:
        """Query the vector store."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

        formatted = []
        for i in range(len(results['documents'][0])):
            formatted.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
                'id': results['ids'][0][i]
            })

        return formatted

    def get_stats(self) -> Dict:
        """Get collection statistics."""
        return {
            "count": self.collection.count(),
            "name": self.collection.name
        }

    def clear(self) -> None:
        """Clear all documents from the collection."""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )
