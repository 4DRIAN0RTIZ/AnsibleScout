"""
Search Service

Provides fuzzy search functionality for Ansible modules.
"""

from typing import Dict, List, Tuple
from rapidfuzz import fuzz, process


class SearchService:
    """Handles fuzzy search operations on modules"""

    def __init__(self, modules: Dict[str, str]):
        self.modules = modules

    def search(self, query: str, limit: int = 10) -> List[Tuple[str, str, float]]:
        """
        Perform fuzzy search on modules

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of (module_name, description, score) tuples
        """
        search_corpus = {
            name: f"{name} {desc}"
            for name, desc in self.modules.items()
        }

        results = process.extract(
            query,
            search_corpus,
            scorer=fuzz.WRatio,
            limit=limit
        )

        formatted_results = []
        for match_text, score, module_name in results:
            formatted_results.append((
                module_name,
                self.modules[module_name],
                score
            ))

        return formatted_results
