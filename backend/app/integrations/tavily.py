from tavily import TavilyClient
from app.core.config import settings

class TavilyService:
    def __init__(self):
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    async def search(self, query: str, search_depth: str = "basic", max_results: int = 5) -> list:
        """
        Performs a search using Tavily.
        """
        try:
            # Note: The current tavily-python library's search is synchronous
            # We wrap it in an async-friendly way if needed, but for now simple call
            response = self.client.search(query=query, search_depth=search_depth, max_results=max_results)
            return response.get("results", [])
        except Exception as e:
            print(f"Error calling Tavily: {e}")
            return []

    async def get_search_context(self, query: str, search_depth: str = "basic", max_results: int = 5) -> str:
        """
        Gets a search context string for LLM usage.
        """
        try:
            context = self.client.get_search_context(query=query, search_depth=search_depth, max_results=max_results)
            return context
        except Exception as e:
            print(f"Error getting search context: {e}")
            return ""

tavily_service = TavilyService()
