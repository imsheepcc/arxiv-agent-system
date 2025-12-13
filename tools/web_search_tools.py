"""
Web Search Tools - Search the web for information
"""
import requests
from typing import List, Dict, Any
import os


class WebSearchTools:
    """Tools for web search functionality"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize web search tools
        
        Args:
            api_key: API key for search service (Brave, Google, etc.)
        """
        self.api_key = api_key or os.getenv("BRAVE_API_KEY") or os.getenv("SERPER_API_KEY")
        self.provider = self._detect_provider()
        
    def _detect_provider(self) -> str:
        """Detect which search provider to use based on API key"""
        if os.getenv("BRAVE_API_KEY"):
            return "brave"
        elif os.getenv("SERPER_API_KEY"):
            return "serper"
        else:
            return "duckduckgo"  # Free fallback
    
    def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Dict with search results
        """
        if self.provider == "brave":
            return self._brave_search(query, num_results)
        elif self.provider == "serper":
            return self._serper_search(query, num_results)
        else:
            return self._duckduckgo_search(query, num_results)
    
    def _brave_search(self, query: str, num_results: int) -> Dict[str, Any]:
        """Search using Brave Search API"""
        
        if not self.api_key:
            return {
                "status": "error",
                "message": "Brave API key not found. Set BRAVE_API_KEY environment variable.",
                "results": []
            }
        
        try:
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.api_key
            }
            
            params = {
                "q": query,
                "count": num_results
            }
            
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("web", {}).get("results", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", "")
                })
            
            return {
                "status": "success",
                "query": query,
                "count": len(results),
                "results": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Brave search failed: {str(e)}",
                "results": []
            }
    
    def _serper_search(self, query: str, num_results: int) -> Dict[str, Any]:
        """Search using Serper API (Google Search)"""
        
        if not self.api_key:
            return {
                "status": "error",
                "message": "Serper API key not found. Set SERPER_API_KEY environment variable.",
                "results": []
            }
        
        try:
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "num": num_results
            }
            
            response = requests.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("organic", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
            
            return {
                "status": "success",
                "query": query,
                "count": len(results),
                "results": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Serper search failed: {str(e)}",
                "results": []
            }
    
    def _duckduckgo_search(self, query: str, num_results: int) -> Dict[str, Any]:
        """
        Fallback: Simple DuckDuckGo search (no API key needed)
        Note: This is a simplified version for demonstration
        """
        
        try:
            # DuckDuckGo Instant Answer API (limited)
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(
                "https://api.duckduckgo.com/",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Get abstract if available
            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", query),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("Abstract", "")
                })
            
            # Get related topics
            for topic in data.get("RelatedTopics", [])[:num_results-1]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "url": topic.get("FirstURL", ""),
                        "snippet": topic.get("Text", "")
                    })
            
            return {
                "status": "success",
                "query": query,
                "count": len(results),
                "results": results,
                "note": "Using DuckDuckGo (limited results). For better results, set BRAVE_API_KEY or SERPER_API_KEY."
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"DuckDuckGo search failed: {str(e)}",
                "results": []
            }
    
    def fetch_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch content from a URL
        
        Args:
            url: URL to fetch
            
        Returns:
            Dict with page content
        """
        try:
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; ArxivAgentBot/1.0)'
            })
            response.raise_for_status()
            
            # Get text content (simplified - could use BeautifulSoup for better parsing)
            content = response.text[:5000]  # Limit content length
            
            return {
                "status": "success",
                "url": url,
                "content": content,
                "length": len(content)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to fetch URL: {str(e)}",
                "content": ""
            }
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions for LLM function calling
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for information on any topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "num_results": {
                                "type": "integer",
                                "description": "Number of results to return (1-10)",
                                "minimum": 1,
                                "maximum": 10
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_url",
                    "description": "Fetch content from a specific URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to fetch content from"
                            }
                        },
                        "required": ["url"]
                    }
                }
            }
        ]


# Test function
def test_web_search():
    """Test web search tools"""
    tools = WebSearchTools()
    
    print(f"Using provider: {tools.provider}")
    print("\nTesting web search...")
    
    result = tools.search("latest AI research papers", num_results=3)
    
    if result["status"] == "success":
        print(f"✓ Found {result['count']} results for '{result['query']}'")
        for i, res in enumerate(result["results"], 1):
            print(f"\n{i}. {res['title']}")
            print(f"   URL: {res['url']}")
            print(f"   Snippet: {res['snippet'][:100]}...")
    else:
        print(f"✗ Error: {result['message']}")


if __name__ == "__main__":
    test_web_search()
