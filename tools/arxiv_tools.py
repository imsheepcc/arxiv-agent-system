"""
arXiv API Tools - Fetch real papers from arXiv
"""
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from datetime import datetime, timedelta


class ArxivTools:
    """Tools for fetching papers from arXiv API"""
    
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        
    def search_papers(self, category: str = "cs.AI", max_results: int = 10, 
                     days_back: int = 7) -> Dict[str, Any]:
        """
        Search for recent papers in a specific category
        
        Args:
            category: arXiv category (e.g., 'cs.AI', 'cs.CV')
            max_results: Maximum number of results to return
            days_back: How many days back to search
            
        Returns:
            Dict with status and list of papers
        """
        try:
            # Build query
            params = {
                'search_query': f'cat:{category}',
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            # Add proper headers to avoid 403
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Make request
            import time
            time.sleep(0.5)  # Be nice to arXiv servers
            
            response = requests.get(self.base_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse XML response
            papers = self._parse_arxiv_response(response.text)
            
            return {
                "status": "success",
                "category": category,
                "count": len(papers),
                "papers": papers
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to fetch papers: {str(e)}",
                "papers": []
            }
    
    def fetch_multiple_categories(self, categories: List[str], 
                                  papers_per_category: int = 5) -> Dict[str, Any]:
        """
        Fetch papers from multiple categories
        
        Args:
            categories: List of category codes
            papers_per_category: Number of papers per category
            
        Returns:
            Dict with all papers organized by category
        """
        all_papers = []
        category_counts = {}
        
        for category in categories:
            result = self.search_papers(category, papers_per_category)
            
            if result["status"] == "success":
                all_papers.extend(result["papers"])
                category_counts[category] = len(result["papers"])
        
        return {
            "status": "success",
            "total_papers": len(all_papers),
            "categories": category_counts,
            "papers": all_papers
        }
    
    def _parse_arxiv_response(self, xml_text: str) -> List[Dict[str, Any]]:
        """Parse arXiv API XML response"""
        
        papers = []
        
        try:
            # Parse XML
            root = ET.fromstring(xml_text)
            
            # Define namespace
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            # Extract entries
            for entry in root.findall('atom:entry', ns):
                try:
                    # Extract basic info
                    paper_id = entry.find('atom:id', ns).text.split('/abs/')[-1]
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                    summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                    
                    # Extract authors
                    authors = []
                    author_affiliations = []
                    for author in entry.findall('atom:author', ns):
                        name = author.find('atom:name', ns).text
                        authors.append(name)
                        
                        # Try to get affiliation
                        affiliation = author.find('arxiv:affiliation', ns)
                        if affiliation is not None:
                            author_affiliations.append(affiliation.text)
                    
                    # If no affiliations found, add generic ones
                    if not author_affiliations:
                        author_affiliations = ["Unknown Institution"]
                    
                    # Extract published date
                    published = entry.find('atom:published', ns).text
                    published_date = published.split('T')[0]  # Get YYYY-MM-DD
                    
                    # Extract category
                    primary_category = entry.find('arxiv:primary_category', ns)
                    if primary_category is not None:
                        category = primary_category.get('term')
                    else:
                        # Fallback to first category
                        category_elem = entry.find('atom:category', ns)
                        category = category_elem.get('term') if category_elem is not None else 'cs.AI'
                    
                    # Build URLs
                    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
                    arxiv_url = f"https://arxiv.org/abs/{paper_id}"
                    
                    paper = {
                        "id": paper_id,
                        "title": title,
                        "authors": authors[:5],  # Limit to first 5 authors
                        "affiliations": list(set(author_affiliations))[:3],  # Unique, max 3
                        "abstract": summary[:500] + "..." if len(summary) > 500 else summary,
                        "category": category,
                        "submitted": published_date,
                        "pdf_url": pdf_url,
                        "arxiv_url": arxiv_url
                    }
                    
                    papers.append(paper)
                    
                except Exception as e:
                    print(f"Error parsing paper entry: {e}")
                    continue
            
        except Exception as e:
            print(f"Error parsing XML: {e}")
        
        return papers
    
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
                    "name": "search_arxiv_papers",
                    "description": "Search for recent papers from arXiv in a specific category",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "arXiv category code (e.g., 'cs.AI', 'cs.CV', 'cs.LG')",
                                "enum": ["cs.AI", "cs.CV", "cs.LG", "cs.CL", "cs.RO", "cs.CR", 
                                        "cs.AR", "cs.CC", "cs.DS", "cs.NE"]
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of papers to fetch (1-20)",
                                "minimum": 1,
                                "maximum": 20
                            }
                        },
                        "required": ["category"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_multiple_categories",
                    "description": "Fetch papers from multiple arXiv categories at once",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "categories": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of arXiv category codes"
                            },
                            "papers_per_category": {
                                "type": "integer",
                                "description": "Number of papers per category (1-10)",
                                "minimum": 1,
                                "maximum": 10
                            }
                        },
                        "required": ["categories"]
                    }
                }
            }
        ]


# Convenience function for quick testing
def test_arxiv_tools():
    """Test the arXiv tools"""
    tools = ArxivTools()
    
    print("Testing arXiv API...")
    result = tools.search_papers("cs.AI", max_results=3)
    
    if result["status"] == "success":
        print(f"✓ Successfully fetched {result['count']} papers from {result['category']}")
        for i, paper in enumerate(result["papers"], 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {', '.join(paper['authors'])}")
            print(f"   arXiv: {paper['id']}")
    else:
        print(f"✗ Error: {result['message']}")


if __name__ == "__main__":
    test_arxiv_tools()
