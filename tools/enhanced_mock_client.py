"""
Enhanced Mock LLM Client that generates realistic code for demonstration
"""
import json
from typing import List, Dict, Any


class EnhancedMockLLMClient:
    """Mock LLM client that generates realistic responses for the arXiv project"""
    
    def __init__(self, *args, **kwargs):
        self.call_count = 0
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7,
             max_tokens: int = 4000,
             tools: List[Dict] = None,
             stream: bool = False) -> Dict[str, Any]:
        """Return realistic mock responses based on context"""
        
        self.call_count += 1
        last_message = messages[-1]["content"].lower()
        
        # Planning phase
        if "project plan" in last_message or "analyze the following project" in last_message:
            return self._generate_project_plan()
        
        # Code generation phase
        elif tools is not None:
            return self._generate_code_with_tools(messages, tools)
        
        # Evaluation phase
        elif "evaluate the following" in last_message:
            return self._generate_evaluation()
        
        # Default response
        else:
            return {
                "content": "Task acknowledged and proceeding with implementation.",
                "role": "assistant"
            }
    
    def _generate_project_plan(self) -> Dict[str, Any]:
        """Generate a realistic project plan"""
        
        plan = {
            "project_name": "arXiv CS Daily",
            "technology_stack": ["html5", "css3", "javascript", "json"],
            "file_structure": {
                "index.html": "Homepage with category navigation",
                "category.html": "Category-specific paper listings",
                "paper.html": "Individual paper detail page",
                "css/style.css": "Responsive styling with modern design",
                "js/script.js": "Dynamic functionality and citation generation",
                "data/papers.json": "Sample paper data for demonstration"
            },
            "tasks": [
                {
                    "id": 1,
                    "title": "Create sample paper data",
                    "description": "Create papers.json with realistic arXiv paper samples across multiple CS categories",
                    "file_path": "data/papers.json",
                    "dependencies": [],
                    "priority": "high"
                },
                {
                    "id": 2,
                    "title": "Create homepage",
                    "description": "Build index.html with navigation system for CS categories and link to category pages",
                    "file_path": "index.html",
                    "dependencies": [1],
                    "priority": "high"
                },
                {
                    "id": 3,
                    "title": "Create category page",
                    "description": "Build category.html to display papers filtered by category with links to detail pages",
                    "file_path": "category.html",
                    "dependencies": [1],
                    "priority": "high"
                },
                {
                    "id": 4,
                    "title": "Create paper detail page",
                    "description": "Build paper.html with full metadata, PDF link, and citation generation tools",
                    "file_path": "paper.html",
                    "dependencies": [1],
                    "priority": "high"
                },
                {
                    "id": 5,
                    "title": "Create CSS stylesheet",
                    "description": "Design responsive, modern CSS with clean layout and good UX",
                    "file_path": "css/style.css",
                    "dependencies": [2, 3, 4],
                    "priority": "medium"
                },
                {
                    "id": 6,
                    "title": "Create JavaScript functionality",
                    "description": "Implement data loading, filtering, and citation copy functionality",
                    "file_path": "js/script.js",
                    "dependencies": [2, 3, 4, 5],
                    "priority": "medium"
                }
            ]
        }
        
        return {
            "content": json.dumps(plan, indent=2),
            "role": "assistant"
        }
    
    def _generate_code_with_tools(self, messages: List[Dict[str, str]], 
                                   tools: List[Dict]) -> Dict[str, Any]:
        """Generate code and return with tool calls"""
        
        # Extract what file we're supposed to create from the messages
        last_msg = messages[-1]["content"].lower()
        
        # Determine which file to create based on context
        if "papers.json" in last_msg or "sample paper data" in last_msg or "sample data" in last_msg:
            return self._create_papers_json()
        elif "index.html" in last_msg or "homepage" in last_msg:
            return self._create_index_html()
        elif "category.html" in last_msg or "category page" in last_msg:
            return self._create_category_html()
        elif "paper.html" in last_msg or "paper detail" in last_msg:
            return self._create_paper_html()
        elif "style.css" in last_msg or "css" in last_msg:
            return self._create_style_css()
        elif "script.js" in last_msg or "javascript" in last_msg:
            return self._create_script_js()
        else:
            # Generic response with a simple tool call
            return {
                "content": "Creating the requested file...",
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": f"call_{self.call_count}",
                        "type": "function",
                        "function": {
                            "name": "create_file",
                            "arguments": json.dumps({
                                "path": "README.txt",
                                "content": "Project files generated by Multi-Agent System"
                            })
                        }
                    }
                ]
            }
    
    def _create_papers_json(self) -> Dict[str, Any]:
        """Create sample papers data"""
        
        papers_data = {
            "papers": [
                {
                    "id": "2501.00001",
                    "title": "Attention Is All You Need: A Comprehensive Survey",
                    "authors": ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
                    "affiliations": ["Google Brain", "Google Research"],
                    "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
                    "category": "cs.AI",
                    "submitted": "2025-01-15",
                    "pdf_url": "https://arxiv.org/pdf/2501.00001.pdf",
                    "arxiv_url": "https://arxiv.org/abs/2501.00001"
                },
                {
                    "id": "2501.00002",
                    "title": "Deep Learning for Computer Vision: State of the Art 2025",
                    "authors": ["Yann LeCun", "Geoffrey Hinton", "Yoshua Bengio"],
                    "affiliations": ["Meta AI", "Google DeepMind", "MILA"],
                    "abstract": "This survey presents recent advances in deep learning methods for computer vision tasks...",
                    "category": "cs.CV",
                    "submitted": "2025-01-14",
                    "pdf_url": "https://arxiv.org/pdf/2501.00002.pdf",
                    "arxiv_url": "https://arxiv.org/abs/2501.00002"
                },
                {
                    "id": "2501.00003",
                    "title": "Reinforcement Learning in Practice: Challenges and Solutions",
                    "authors": ["Richard Sutton", "Andrew Barto", "David Silver"],
                    "affiliations": ["University of Alberta", "DeepMind"],
                    "abstract": "Reinforcement learning has shown remarkable success in various domains...",
                    "category": "cs.LG",
                    "submitted": "2025-01-14",
                    "pdf_url": "https://arxiv.org/pdf/2501.00003.pdf",
                    "arxiv_url": "https://arxiv.org/abs/2501.00003"
                },
                {
                    "id": "2501.00004",
                    "title": "Natural Language Processing with Transformers",
                    "authors": ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee"],
                    "affiliations": ["Google AI Language"],
                    "abstract": "We introduce BERT: Bidirectional Encoder Representations from Transformers...",
                    "category": "cs.CL",
                    "submitted": "2025-01-13",
                    "pdf_url": "https://arxiv.org/pdf/2501.00004.pdf",
                    "arxiv_url": "https://arxiv.org/abs/2501.00004"
                },
                {
                    "id": "2501.00005",
                    "title": "Graph Neural Networks: A Review of Methods and Applications",
                    "authors": ["Jure Leskovec", "Joan Bruna", "Thomas Kipf"],
                    "affiliations": ["Stanford University", "NYU", "University of Amsterdam"],
                    "abstract": "Graph neural networks have emerged as powerful tools for learning on graph-structured data...",
                    "category": "cs.LG",
                    "submitted": "2025-01-13",
                    "pdf_url": "https://arxiv.org/pdf/2501.00005.pdf",
                    "arxiv_url": "https://arxiv.org/abs/2501.00005"
                },
                {
                    "id": "2501.00006",
                    "title": "Quantum Computing for Machine Learning: Current State and Future",
                    "authors": ["John Preskill", "Peter Shor", "Scott Aaronson"],
                    "affiliations": ["Caltech", "MIT"],
                    "abstract": "This paper explores the intersection of quantum computing and machine learning...",
                    "category": "cs.LG",
                    "submitted": "2025-01-12",
                    "pdf_url": "https://arxiv.org/pdf/2501.00006.pdf",
                    "arxiv_url": "https://arxiv.org/abs/2501.00006"
                },
                {
                    "id": "2501.00007",
                    "title": "Robotics and Autonomous Systems: A Survey",
                    "authors": ["Sebastian Thrun", "Dieter Fox", "Wolfram Burgard"],
                    "affiliations": ["Stanford University", "University of Washington", "University of Freiburg"],
                    "abstract": "This survey provides a comprehensive overview of recent advances in robotics...",
                    "category": "cs.RO",
                    "submitted": "2025-01-12",
                    "pdf_url": "https://arxiv.org/pdf/2501.00007.pdf",
                    "arxiv_url": "https://arxiv.org/abs/2501.00007"
                },
                {
                    "id": "2501.00008",
                    "title": "Privacy-Preserving Machine Learning: Techniques and Applications",
                    "authors": ["Cynthia Dwork", "Aaron Roth", "Dawn Song"],
                    "affiliations": ["Harvard University", "UC Berkeley"],
                    "abstract": "We present a comprehensive study of privacy-preserving techniques in machine learning...",
                    "category": "cs.CR",
                    "submitted": "2025-01-11",
                    "pdf_url": "https://arxiv.org/pdf/2501.00008.pdf",
                    "arxiv_url": "https://arxiv.org/abs/2501.00008"
                }
            ],
            "categories": {
                "cs.AI": "Artificial Intelligence",
                "cs.CV": "Computer Vision and Pattern Recognition",
                "cs.LG": "Machine Learning",
                "cs.CL": "Computation and Language",
                "cs.RO": "Robotics",
                "cs.CR": "Cryptography and Security",
                "cs.AR": "Hardware Architecture",
                "cs.CC": "Computational Complexity",
                "cs.DS": "Data Structures and Algorithms"
            }
        }
        
        return {
            "content": "Creating sample papers data file...",
            "role": "assistant",
            "tool_calls": [
                {
                    "id": f"call_{self.call_count}",
                    "type": "function",
                    "function": {
                        "name": "create_file",
                        "arguments": json.dumps({
                            "path": "data/papers.json",
                            "content": json.dumps(papers_data, indent=2)
                        })
                    }
                }
            ]
        }
    
    def _create_index_html(self) -> Dict[str, Any]:
        """Create index.html"""
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>arXiv CS Daily</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1 class="logo">arXiv CS Daily</h1>
            <ul class="nav-links">
                <li><a href="index.html" class="active">Home</a></li>
                <li><a href="category.html">All Papers</a></li>
                <li class="dropdown">
                    <a href="#" class="dropbtn">Categories ▼</a>
                    <div class="dropdown-content" id="categoryDropdown"></div>
                </li>
            </ul>
        </div>
    </nav>

    <header class="hero">
        <div class="container">
            <h1 class="hero-title">arXiv CS Daily</h1>
            <p class="hero-subtitle">Track the latest computer science research papers from arXiv.org</p>
            <p class="hero-description">Browse by category or view the most recent submissions across all CS fields.</p>
            <a href="category.html" class="btn btn-primary">View Latest Papers</a>
        </div>
    </header>

    <section class="categories-section">
        <div class="container">
            <h2 class="section-title">Computer Science Categories</h2>
            <p class="section-subtitle">arXiv's Computer Science (cs) archive is organized into the following subject categories:</p>
            
            <div class="categories-grid" id="categoriesGrid">
                <!-- Categories will be dynamically loaded here -->
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 arXiv CS Daily. Data sourced from arXiv.org</p>
            <p>Built with Multi-Agent Code Generation System</p>
        </div>
    </footer>

    <script src="js/script.js"></script>
    <script>
        // Load categories on homepage
        loadCategories();
    </script>
</body>
</html>'''
        
        return {
            "content": "Creating homepage with category navigation...",
            "role": "assistant",
            "tool_calls": [
                {
                    "id": f"call_{self.call_count}",
                    "type": "function",
                    "function": {
                        "name": "create_file",
                        "arguments": json.dumps({
                            "path": "index.html",
                            "content": html_content
                        })
                    }
                }
            ]
        }
    
    def _create_category_html(self) -> Dict[str, Any]:
        """Create category.html"""
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Papers - arXiv CS Daily</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1 class="logo"><a href="index.html">arXiv CS Daily</a></h1>
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="category.html" class="active">All Papers</a></li>
                <li class="dropdown">
                    <a href="#" class="dropbtn">Categories ▼</a>
                    <div class="dropdown-content" id="categoryDropdown"></div>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container main-content">
        <div class="category-header">
            <h1 id="categoryTitle">All Papers</h1>
            <p id="categoryDescription">Showing the latest papers from arXiv in the category</p>
            
            <div class="filters">
                <label for="dateFilter">Publication Date:</label>
                <select id="dateFilter" onchange="filterByDate()">
                    <option value="">All dates</option>
                    <option value="2025-01-15">Jan 15, 2025</option>
                    <option value="2025-01-14">Jan 14, 2025</option>
                    <option value="2025-01-13">Jan 13, 2025</option>
                    <option value="2025-01-12">Jan 12, 2025</option>
                    <option value="2025-01-11">Jan 11, 2025</option>
                </select>
            </div>
        </div>

        <div class="papers-list" id="papersList">
            <!-- Papers will be dynamically loaded here -->
        </div>
    </div>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 arXiv CS Daily. Data sourced from arXiv.org</p>
        </div>
    </footer>

    <script src="js/script.js"></script>
    <script>
        // Load papers when page loads
        const urlParams = new URLSearchParams(window.location.search);
        const category = urlParams.get('category');
        loadPapers(category);
    </script>
</body>
</html>'''
        
        return {
            "content": "Creating category papers listing page...",
            "role": "assistant",
            "tool_calls": [
                {
                    "id": f"call_{self.call_count}",
                    "type": "function",
                    "function": {
                        "name": "create_file",
                        "arguments": json.dumps({
                            "path": "category.html",
                            "content": html_content
                        })
                    }
                }
            ]
        }
    
    def _create_paper_html(self) -> Dict[str, Any]:
        """Create paper.html"""
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paper Details - arXiv CS Daily</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1 class="logo"><a href="index.html">arXiv CS Daily</a></h1>
            <ul class="nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="category.html">All Papers</a></li>
                <li class="dropdown">
                    <a href="#" class="dropbtn">Categories ▼</a>
                    <div class="dropdown-content" id="categoryDropdown"></div>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container main-content">
        <div class="paper-detail" id="paperDetail">
            <!-- Paper details will be dynamically loaded here -->
        </div>

        <div class="citation-section">
            <h2>Citation</h2>
            
            <div class="citation-box">
                <h3>BibTeX</h3>
                <pre id="bibtexCitation" class="citation-content"></pre>
                <button onclick="copyCitation('bibtex')" class="btn btn-secondary">Copy BibTeX</button>
            </div>

            <div class="citation-box">
                <h3>Standard Citation</h3>
                <p id="standardCitation" class="citation-content"></p>
                <button onclick="copyCitation('standard')" class="btn btn-secondary">Copy Citation</button>
            </div>
        </div>
    </div>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 arXiv CS Daily. Data sourced from arXiv.org</p>
        </div>
    </footer>

    <script src="js/script.js"></script>
    <script>
        // Load paper details when page loads
        const urlParams = new URLSearchParams(window.location.search);
        const paperId = urlParams.get('id');
        loadPaperDetails(paperId);
    </script>
</body>
</html>'''
        
        return {
            "content": "Creating paper detail page with citations...",
            "role": "assistant",
            "tool_calls": [
                {
                    "id": f"call_{self.call_count}",
                    "type": "function",
                    "function": {
                        "name": "create_file",
                        "arguments": json.dumps({
                            "path": "paper.html",
                            "content": html_content
                        })
                    }
                }
            ]
        }
    
    def _create_style_css(self) -> Dict[str, Any]:
        """Create style.css"""
        
        css_content = '''/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
.navbar {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
}

.logo a {
    color: white;
    text-decoration: none;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover,
.nav-links a.active {
    color: #3498db;
}

/* Dropdown */
.dropdown {
    position: relative;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: white;
    min-width: 200px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    z-index: 1;
    border-radius: 4px;
    max-height: 400px;
    overflow-y: auto;
}

.dropdown-content a {
    color: #333;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content a:hover {
    background-color: #f1f1f1;
}

.dropdown:hover .dropdown-content {
    display: block;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 0;
    text-align: center;
}

.hero-title {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    opacity: 0.9;
}

.hero-description {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.8;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 12px 30px;
    border-radius: 5px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}

.btn-primary {
    background-color: white;
    color: #667eea;
    font-weight: bold;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.btn-secondary {
    background-color: #3498db;
    color: white;
}

.btn-secondary:hover {
    background-color: #2980b9;
}

/* Categories Section */
.categories-section {
    padding: 4rem 0;
    background-color: white;
}

.section-title {
    font-size: 2rem;
    margin-bottom: 1rem;
    text-align: center;
}

.section-subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 3rem;
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
}

.category-card {
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    border-left: 4px solid #3498db;
    transition: all 0.3s;
}

.category-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.category-card h3 {
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.category-card p {
    color: #666;
    margin-bottom: 1rem;
}

.category-card a {
    color: #3498db;
    text-decoration: none;
    font-weight: bold;
}

/* Papers List */
.main-content {
    padding: 3rem 0;
}

.category-header {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.category-header h1 {
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.filters {
    margin-top: 1rem;
}

.filters select {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.papers-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.paper-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: all 0.3s;
}

.paper-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.paper-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    color: #666;
}

.paper-category {
    background-color: #3498db;
    color: white;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 0.85rem;
}

.paper-title {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.paper-title a {
    color: #2c3e50;
    text-decoration: none;
}

.paper-title a:hover {
    color: #3498db;
}

.paper-authors {
    color: #666;
    margin-bottom: 0.5rem;
}

.paper-abstract {
    color: #555;
    line-height: 1.6;
}

/* Paper Detail */
.paper-detail {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.paper-detail h1 {
    color: #2c3e50;
    margin-bottom: 1rem;
}

.detail-section {
    margin-bottom: 1.5rem;
}

.detail-section h2 {
    color: #2c3e50;
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

.authors-list {
    color: #555;
}

.pdf-link {
    display: inline-block;
    margin-top: 1rem;
}

/* Citation Section */
.citation-section {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.citation-section h2 {
    color: #2c3e50;
    margin-bottom: 1.5rem;
}

.citation-box {
    margin-bottom: 2rem;
}

.citation-box h3 {
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

.citation-content {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 4px;
    border: 1px solid #e9ecef;
    margin-bottom: 0.5rem;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* Footer */
.footer {
    background-color: #2c3e50;
    color: white;
    padding: 2rem 0;
    text-align: center;
    margin-top: 4rem;
}

.footer p {
    margin-bottom: 0.5rem;
    opacity: 0.8;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
    }
    
    .categories-grid {
        grid-template-columns: 1fr;
    }
    
    .nav-links {
        flex-direction: column;
        gap: 1rem;
    }
}'''
        
        return {
            "content": "Creating responsive CSS stylesheet...",
            "role": "assistant",
            "tool_calls": [
                {
                    "id": f"call_{self.call_count}",
                    "type": "function",
                    "function": {
                        "name": "create_file",
                        "arguments": json.dumps({
                            "path": "css/style.css",
                            "content": css_content
                        })
                    }
                }
            ]
        }
    
    def _create_script_js(self) -> Dict[str, Any]:
        """Create script.js"""
        
        js_content = '''// Global data storage
let papersData = null;
let categoriesData = null;

// Load papers data
async function loadData() {
    try {
        const response = await fetch('data/papers.json');
        const data = await response.json();
        papersData = data.papers;
        categoriesData = data.categories;
        return data;
    } catch (error) {
        console.error('Error loading data:', error);
        return null;
    }
}

// Load categories for homepage
async function loadCategories() {
    const data = await loadData();
    if (!data) return;
    
    const grid = document.getElementById('categoriesGrid');
    const dropdown = document.getElementById('categoryDropdown');
    
    if (grid) {
        grid.innerHTML = '';
        for (const [code, name] of Object.entries(data.categories)) {
            const card = document.createElement('div');
            card.className = 'category-card';
            
            const paperCount = data.papers.filter(p => p.category === code).length;
            
            card.innerHTML = `
                <h3>${code}</h3>
                <p>${name}</p>
                <p>${paperCount} paper${paperCount !== 1 ? 's' : ''}</p>
                <a href="category.html?category=${code}">Browse Papers →</a>
            `;
            
            grid.appendChild(card);
        }
    }
    
    if (dropdown) {
        dropdown.innerHTML = '';
        for (const [code, name] of Object.entries(data.categories)) {
            const link = document.createElement('a');
            link.href = `category.html?category=${code}`;
            link.textContent = `${code} - ${name}`;
            dropdown.appendChild(link);
        }
    }
}

// Load papers for category page
async function loadPapers(category = null) {
    const data = await loadData();
    if (!data) return;
    
    const list = document.getElementById('papersList');
    const titleEl = document.getElementById('categoryTitle');
    const descEl = document.getElementById('categoryDescription');
    
    if (!list) return;
    
    // Filter papers by category
    let papers = data.papers;
    if (category) {
        papers = papers.filter(p => p.category === category);
        if (titleEl) titleEl.textContent = `${category} Papers`;
        if (descEl) descEl.textContent = data.categories[category] || '';
    } else {
        if (titleEl) titleEl.textContent = 'All Papers';
        if (descEl) descEl.textContent = 'Showing all recent submissions across CS fields';
    }
    
    // Sort by date (newest first)
    papers.sort((a, b) => new Date(b.submitted) - new Date(a.submitted));
    
    // Display papers
    list.innerHTML = '';
    papers.forEach(paper => {
        const card = createPaperCard(paper);
        list.appendChild(card);
    });
}

// Create paper card element
function createPaperCard(paper) {
    const card = document.createElement('div');
    card.className = 'paper-card';
    
    const date = new Date(paper.submitted).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    card.innerHTML = `
        <div class="paper-meta">
            <span class="paper-category">${paper.category}</span>
            <span>${date}</span>
            <span>arXiv:${paper.id}</span>
        </div>
        <h2 class="paper-title">
            <a href="paper.html?id=${paper.id}">${paper.title}</a>
        </h2>
        <p class="paper-authors">${paper.authors.join(', ')}</p>
        <p class="paper-abstract">${paper.abstract}</p>
    `;
    
    return card;
}

// Filter papers by date
function filterByDate() {
    const dateFilter = document.getElementById('dateFilter');
    const selectedDate = dateFilter.value;
    
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');
    
    const list = document.getElementById('papersList');
    if (!list || !papersData) return;
    
    let papers = papersData;
    
    // Filter by category
    if (category) {
        papers = papers.filter(p => p.category === category);
    }
    
    // Filter by date
    if (selectedDate) {
        papers = papers.filter(p => p.submitted === selectedDate);
    }
    
    // Sort and display
    papers.sort((a, b) => new Date(b.submitted) - new Date(a.submitted));
    
    list.innerHTML = '';
    papers.forEach(paper => {
        const card = createPaperCard(paper);
        list.appendChild(card);
    });
}

// Load paper details
async function loadPaperDetails(paperId) {
    const data = await loadData();
    if (!data) return;
    
    const paper = data.papers.find(p => p.id === paperId);
    if (!paper) {
        document.getElementById('paperDetail').innerHTML = '<p>Paper not found.</p>';
        return;
    }
    
    const detailDiv = document.getElementById('paperDetail');
    
    const date = new Date(paper.submitted).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    detailDiv.innerHTML = `
        <div class="paper-meta">
            <span class="paper-category">${paper.category}</span>
            <span>${date}</span>
            <span>arXiv:${paper.id}</span>
        </div>
        <h1>${paper.title}</h1>
        
        <div class="detail-section">
            <h2>Authors</h2>
            <p class="authors-list">${paper.authors.join(', ')}</p>
            <p style="color: #666; font-size: 0.9rem;">${paper.affiliations.join(', ')}</p>
        </div>
        
        <div class="detail-section">
            <h2>Abstract</h2>
            <p>${paper.abstract}</p>
        </div>
        
        <div class="detail-section">
            <h2>Links</h2>
            <a href="${paper.pdf_url}" class="btn btn-primary pdf-link" target="_blank">View PDF</a>
            <a href="${paper.arxiv_url}" class="btn btn-secondary pdf-link" target="_blank">arXiv Page</a>
        </div>
    `;
    
    // Generate citations
    generateCitations(paper);
}

// Generate citations
function generateCitations(paper) {
    const year = new Date(paper.submitted).getFullYear();
    const authorsLastNames = paper.authors.map(a => a.split(' ').pop());
    
    // BibTeX
    const bibtex = `@article{${authorsLastNames[0].toLowerCase()}${year}${paper.id.split('.')[1]},
  title={${paper.title}},
  author={${paper.authors.join(' and ')}},
  journal={arXiv preprint arXiv:${paper.id}},
  year={${year}}
}`;
    
    document.getElementById('bibtexCitation').textContent = bibtex;
    
    // Standard citation
    const standardCitation = `${paper.authors.join(', ')}. "${paper.title}." arXiv preprint arXiv:${paper.id} (${year}).`;
    
    document.getElementById('standardCitation').textContent = standardCitation;
}

// Copy citation to clipboard
function copyCitation(type) {
    let text = '';
    
    if (type === 'bibtex') {
        text = document.getElementById('bibtexCitation').textContent;
    } else if (type === 'standard') {
        text = document.getElementById('standardCitation').textContent;
    }
    
    navigator.clipboard.writeText(text).then(() => {
        alert('Citation copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Initialize dropdowns on all pages
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
});'''
        
        return {
            "content": "Creating JavaScript functionality...",
            "role": "assistant",
            "tool_calls": [
                {
                    "id": f"call_{self.call_count}",
                    "type": "function",
                    "function": {
                        "name": "create_file",
                        "arguments": json.dumps({
                            "path": "js/script.js",
                            "content": js_content
                        })
                    }
                }
            ]
        }
    
    def _generate_evaluation(self) -> Dict[str, Any]:
        """Generate code evaluation"""
        
        evaluation = {
            "overall_score": 88,
            "passed": True,
            "issues": [
                {
                    "severity": "low",
                    "file": "js/script.js",
                    "description": "Could add error handling for failed fetch requests",
                    "suggestion": "Add try-catch blocks and user-friendly error messages"
                }
            ],
            "strengths": [
                "Clean, semantic HTML structure",
                "Responsive design with mobile support",
                "Well-organized CSS with clear sections",
                "Functional JavaScript with data loading and filtering",
                "Citation generation feature works correctly",
                "Good user experience with intuitive navigation"
            ],
            "recommendations": [
                "Consider adding loading indicators for data fetching",
                "Could implement search functionality",
                "Add pagination for large paper lists"
            ]
        }
        
        return {
            "content": json.dumps(evaluation, indent=2),
            "role": "assistant"
        }
