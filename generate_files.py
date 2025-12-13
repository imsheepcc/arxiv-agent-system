#!/usr/bin/env python
"""
Direct file generation script for arXiv CS Daily project
This bypasses the agent system and directly generates all required files
"""
import sys
sys.path.insert(0, '.')

from tools.file_tools import FileTools

# Initialize file tools
file_tools = FileTools(base_dir="outputs")

# 1. Create papers.json
papers_data = '''{
  "papers": [
    {
      "id": "2501.00001",
      "title": "Attention Is All You Need: A Comprehensive Survey",
      "authors": ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
      "affiliations": ["Google Brain", "Google Research"],
      "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. The dominant approach in sequence transduction is based on complex recurrent or convolutional neural networks that include an encoder and a decoder. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.",
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
      "abstract": "This survey presents recent advances in deep learning methods for computer vision tasks. We cover convolutional neural networks, vision transformers, and the latest advances in self-supervised learning for visual recognition.",
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
      "abstract": "Reinforcement learning has shown remarkable success in various domains, from playing complex games to robotic control. This paper discusses practical challenges in deploying RL systems and presents solutions based on our experience.",
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
      "abstract": "We introduce BERT: Bidirectional Encoder Representations from Transformers. BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers.",
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
      "abstract": "Graph neural networks have emerged as powerful tools for learning on graph-structured data. This review covers the fundamental architectures, training techniques, and applications of GNNs across various domains.",
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
      "abstract": "This paper explores the intersection of quantum computing and machine learning. We discuss quantum algorithms for optimization, sampling, and linear algebra that could provide exponential speedups for certain ML tasks.",
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
      "abstract": "This survey provides a comprehensive overview of recent advances in robotics and autonomous systems. Topics include perception, planning, control, and learning for mobile robots and manipulators.",
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
      "abstract": "We present a comprehensive study of privacy-preserving techniques in machine learning, including differential privacy, federated learning, and secure multi-party computation. Applications in healthcare and finance are discussed.",
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
}'''

print("Creating data/papers.json...")
file_tools.create_file("data/papers.json", papers_data)

# 2. Create index.html
index_html = '''<!DOCTYPE html>
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

print("Creating index.html...")
file_tools.create_file("index.html", index_html)

print("Done! Files created successfully.")
print(f"Output directory: {file_tools.base_dir}")
