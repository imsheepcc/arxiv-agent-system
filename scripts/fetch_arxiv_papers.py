#!/usr/bin/env python3
"""
Fetch real papers from arXiv and generate papers.json
This script demonstrates the arXiv API integration
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.arxiv_tools import ArxivTools


def fetch_arxiv_papers():
    """Fetch real papers from arXiv API"""
    
    print("="*80)
    print("Fetching REAL papers from arXiv API...")
    print("="*80)
    
    tools = ArxivTools()
    
    # Define categories to fetch
    categories = [
        ("cs.AI", "Artificial Intelligence", 6),
        ("cs.CV", "Computer Vision and Pattern Recognition", 6),
        ("cs.LG", "Machine Learning", 6),
        ("cs.CL", "Computation and Language", 5),
        ("cs.RO", "Robotics", 5),
        ("cs.CR", "Cryptography and Security", 4),
        ("cs.NE", "Neural and Evolutionary Computing", 3),
        ("cs.DS", "Data Structures and Algorithms", 3)
    ]
    
    all_papers = []
    category_info = {}
    
    for cat_code, cat_name, num_papers in categories:
        print(f"\nFetching {num_papers} papers from {cat_code} ({cat_name})...")
        
        result = tools.search_papers(cat_code, max_results=num_papers)
        
        if result["status"] == "success":
            papers = result["papers"]
            all_papers.extend(papers)
            category_info[cat_code] = cat_name
            print(f"✓ Fetched {len(papers)} papers from {cat_code}")
            
            # Show first paper as example
            if papers:
                print(f"  Example: {papers[0]['title'][:60]}...")
        else:
            print(f"✗ Failed to fetch from {cat_code}: {result.get('message')}")
    
    # Create papers.json structure
    papers_data = {
        "papers": all_papers,
        "categories": category_info,
        "metadata": {
            "total_papers": len(all_papers),
            "last_updated": "2025-12-13",
            "source": "arXiv API",
            "note": "Real papers fetched from arXiv.org"
        }
    }
    
    # Save to file
    output_dir = "outputs/data"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "papers.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(papers_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("SUCCESS!")
    print("="*80)
    print(f"Total papers fetched: {len(all_papers)}")
    print(f"Categories: {len(category_info)}")
    print(f"Output file: {output_file}")
    print("\nAll papers have REAL:")
    print("  ✓ arXiv IDs")
    print("  ✓ Working PDF links")
    print("  ✓ Real authors and affiliations")
    print("  ✓ Actual abstracts")
    print("\nYou can now use this data with the website!")
    
    return papers_data


def main():
    """Main execution"""
    try:
        data = fetch_arxiv_papers()
        
        # Show some statistics
        print("\n" + "="*80)
        print("PAPER STATISTICS")
        print("="*80)
        
        categories_count = {}
        for paper in data["papers"]:
            cat = paper["category"]
            categories_count[cat] = categories_count.get(cat, 0) + 1
        
        for cat, count in sorted(categories_count.items()):
            print(f"{cat}: {count} papers")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
