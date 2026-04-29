"""
Semantic Search Service

Provides semantic search capabilities using OpenAI embeddings.
Ctrl+I triggers this for high-quality AI-powered recommendations.
"""

from typing import Dict, List, Tuple

from .embedding_service import EmbeddingService


class SemanticSearchService:
    """Handles semantic search using embeddings"""

    def __init__(self, modules: Dict[str, str], embedding_service: EmbeddingService):
        self.modules = modules
        self.embedding_service = embedding_service

    def search(self, query: str, limit: int = 10) -> List[Tuple[str, str, float]]:
        """
        Perform semantic search using embeddings.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of (module_name, description, similarity_score) tuples
        """
        return self.embedding_service.semantic_search(query, limit)

    def is_ready(self) -> bool:
        """Check if semantic search is ready"""
        return self.embedding_service.is_ready()
