"""
Embedding Service

Handles generation and caching of OpenAI embeddings for Ansible modules.
Provides semantic search capabilities using vector similarity.
"""

import json
import hashlib
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
from openai import OpenAI

from ..config import Config


class EmbeddingService:
    """Manages embeddings for semantic module search"""

    EMBEDDINGS_FILE = Path.home() / ".config" / "ascout" / "module_embeddings.pkl"
    CACHE_VERSION = "1.0"  # Bump when format changes

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.client: Optional[OpenAI] = None
        self.embeddings: Dict[str, List[float]] = {}
        self.modules: Dict[str, str] = {}

        if self.enabled:
            api_key = Config.get_api_key()
            if api_key:
                self.client = OpenAI(api_key=api_key)

    def generate_embeddings(self, modules: Dict[str, str]) -> bool:
        """
        Generate embeddings for all modules.
        Returns True if successful, False otherwise.
        """
        if not self.client:
            return False

        self.modules = modules

        try:
            # Prepare texts for embedding
            # Combine module name + description for better semantic understanding
            texts = []
            module_names = []

            for name, description in modules.items():
                # Create rich text for embedding
                text = f"{name}: {description}"
                texts.append(text)
                module_names.append(name)

            print(f"Generating embeddings for {len(texts)} modules...")
            print("This may take 30-60 seconds on first run...")

            # Generate embeddings in batches (OpenAI allows up to 2048 per batch)
            batch_size = 100
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]
                response = self.client.embeddings.create(
                    model="text-embedding-3-small", input=batch
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
                print(
                    f"  Processed {min(i + batch_size, len(texts))}/{len(texts)} modules..."
                )

            # Store embeddings
            self.embeddings = {
                name: emb for name, emb in zip(module_names, all_embeddings)
            }

            # Cache to disk
            self._save_cache()

            print(f"✓ Embeddings generated and cached successfully!")
            return True

        except Exception as e:
            print(f"Error generating embeddings: {e}")
            self.enabled = False
            return False

    def load_cached_embeddings(self, modules: Dict[str, str]) -> bool:
        """
        Load cached embeddings if they exist and are valid.
        Returns True if loaded successfully, False if regeneration needed.
        """
        if not self.EMBEDDINGS_FILE.exists():
            return False

        try:
            with open(self.EMBEDDINGS_FILE, "rb") as f:
                cache = pickle.load(f)

            # Validate cache
            cached_version = cache.get("version", "0")
            cached_modules_hash = cache.get("modules_hash", "")
            current_modules_hash = self._hash_modules(modules)

            if cached_version != self.CACHE_VERSION:
                print("Cache version mismatch, regenerating embeddings...")
                return False

            if cached_modules_hash != current_modules_hash:
                print("Module list changed, regenerating embeddings...")
                return False

            self.embeddings = cache["embeddings"]
            self.modules = modules

            print(f"✓ Loaded {len(self.embeddings)} cached embeddings")
            return True

        except Exception as e:
            print(f"Error loading embeddings cache: {e}")
            return False

    def _save_cache(self) -> None:
        """Save embeddings to disk cache"""
        try:
            self.EMBEDDINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

            cache = {
                "version": self.CACHE_VERSION,
                "modules_hash": self._hash_modules(self.modules),
                "embeddings": self.embeddings,
            }

            with open(self.EMBEDDINGS_FILE, "wb") as f:
                pickle.dump(cache, f)

        except Exception as e:
            print(f"Warning: Could not save embeddings cache: {e}")

    def _hash_modules(self, modules: Dict[str, str]) -> str:
        """Create a hash of the module list for cache validation"""
        content = json.dumps(modules, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def semantic_search(
        self, query: str, limit: int = 10
    ) -> List[Tuple[str, str, float]]:
        """
        Search modules using semantic similarity.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of (module_name, description, similarity_score) tuples
        """
        if not self.enabled or not self.client or not self.embeddings:
            return []

        try:
            # Generate embedding for query
            response = self.client.embeddings.create(
                model="text-embedding-3-small", input=[query]
            )
            query_embedding = np.array(response.data[0].embedding)

            # Calculate cosine similarity with all modules
            similarities = []
            for name, embedding in self.embeddings.items():
                module_embedding = np.array(embedding)
                similarity = self._cosine_similarity(query_embedding, module_embedding)
                similarities.append((name, similarity))

            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Format results
            results = []
            for name, score in similarities[:limit]:
                description = self.modules.get(name, "")
                # Normalize score to 0-100 range for consistency with fuzzy search
                normalized_score = (score + 1) / 2 * 100  # Cosine similarity is -1 to 1
                results.append((name, description, normalized_score))

            return results

        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def is_ready(self) -> bool:
        """Check if embeddings are loaded and ready"""
        return self.enabled and len(self.embeddings) > 0

    def get_stats(self) -> Dict:
        """Get statistics about the embedding service"""
        return {
            "enabled": self.enabled,
            "cached_embeddings": len(self.embeddings),
            "cache_file": str(self.EMBEDDINGS_FILE),
            "cache_exists": self.EMBEDDINGS_FILE.exists(),
        }
