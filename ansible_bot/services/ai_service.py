"""
AI Service

Handles integration with OpenAI for enhanced module recommendations.
"""

from typing import List, Tuple, Optional
from openai import OpenAI

from ..config import Config


class AIService:
    """Manages AI-powered module recommendations"""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.client: Optional[OpenAI] = None

        if self.enabled:
            api_key = Config.get_api_key()
            if not api_key:
                print("\nWarning: OPENAI_API_KEY not set. AI responses disabled.")
                self.enabled = False
            else:
                self.client = OpenAI(api_key=api_key)

    def format_results(self, query: str, results: List[Tuple[str, str, float]]) -> str:
        """
        Format search results with AI enhancement

        Args:
            query: Original search query
            results: Search results as (name, description, score) tuples

        Returns:
            Formatted string with AI recommendations
        """
        if not self.enabled or not self.client:
            return self._format_simple(results)

        results_text = "\n".join(
            [
                f"{i + 1}. {name} (score: {score:.1f})\n   {desc}"
                for i, (name, desc, score) in enumerate(results)
            ]
        )

        prompt = f"""User query: "{query}"

Found modules:
{results_text}

Provide a concise response (2-3 sentences) explaining which modules best match the user's need and why. Then list the top 3 modules with their full names."""

        try:
            response = self.client.chat.completions.create(
                model=Config.AI_MODEL,
                max_tokens=Config.AI_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"AI error: {e}")
            return self._format_simple(results)

    def _format_simple(self, results: List[Tuple[str, str, float]]) -> str:
        """Fallback formatting without AI"""
        output = []
        for i, (name, desc, score) in enumerate(
            results[: Config.SEARCH_RESULTS_DISPLAY], 1
        ):
            output.append(f"{i}. {name}")
            output.append(f"   {desc}")
            output.append(f"   Match score: {score:.1f}%\n")
        return "\n".join(output)

    def is_enabled(self) -> bool:
        """Check if AI service is enabled and ready"""
        return self.enabled and self.client is not None

    def get_recommendations(
        self, query: str, results: List[Tuple[str, str, float]]
    ) -> str:
        """
        Get AI-powered recommendations for the search results.

        Args:
            query: Original search query
            results: Search results as (name, description, score) tuples

        Returns:
            AI-generated recommendation text
        """
        return self.format_results(query, results)
