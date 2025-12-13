#!/usr/bin/env python3
"""
使用 arxiv Python 库获取真实论文
这个方法比直接调用API更可靠
"""

import json
import os
from datetime import datetime

try:
    import arxiv
    ARXIV_INSTALLED = True
except ImportError:
    ARXIV_INSTALLED = False
    print("⚠️  arxiv 库未安装")
    print("安装命令: pip install arxiv")
    print("")


def fetch_papers_with_arxiv_library():
    """使用 arxiv 库获取真实论文"""
    
    if not ARXIV_INSTALLED:
        print("请先安装: pip install arxiv")
        return None
    
    print("=" * 80)
    print("使用 arxiv 库获取真实论文...")
    print("=" * 80)
    print("")
    
    # 定义要获取的类别
    categories = [
        ("cs.AI", "Artificial Intelligence", 6),
        ("cs.CV", "Computer Vision", 6),
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
        print(f"正在获取 {cat_code} ({cat_name})...")
        
        try:
            # 搜索该类别的论文
            search = arxiv.Search(
                query=f"cat:{cat_code}",
                max_results=num_papers,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            # 获取结果
            results = list(search.results())
            
            for paper in results:
                # 提取作者信息
                authors = [author.name for author in paper.authors[:5]]
                
                # 提取机构（如果有）
                affiliations = []
                for author in paper.authors[:3]:
                    # arxiv库可能不包含机构信息，使用通用值
                    if hasattr(author, 'affiliation') and author.affiliation:
                        affiliations.append(author.affiliation)
                
                if not affiliations:
                    affiliations = ["Research Institution"]
                
                # 构建论文数据
                paper_data = {
                    "id": paper.entry_id.split('/abs/')[-1],
                    "title": paper.title.replace('\n', ' ').strip(),
                    "authors": authors,
                    "affiliations": list(set(affiliations))[:3],
                    "abstract": paper.summary.replace('\n', ' ').strip()[:500] + "...",
                    "category": cat_code,
                    "submitted": paper.published.strftime("%Y-%m-%d"),
                    "pdf_url": paper.pdf_url,
                    "arxiv_url": paper.entry_id
                }
                
                all_papers.append(paper_data)
            
            category_info[cat_code] = cat_name
            print(f"✓ 获取了 {len(results)} 篇论文")
            
        except Exception as e:
            print(f"✗ 获取 {cat_code} 失败: {e}")
            continue
    
    # 创建完整数据结构
    papers_data = {
        "papers": all_papers,
        "categories": category_info,
        "metadata": {
            "total_papers": len(all_papers),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "source": "arXiv (via arxiv Python library)",
            "note": "Real papers fetched from arXiv.org"
        }
    }
    
    return papers_data


def save_papers(papers_data, output_file="outputs/data/papers.json"):
    """保存论文数据"""
    
    # 创建输出目录
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 保存 JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(papers_data, f, indent=2, ensure_ascii=False)
    
    print("")
    print("=" * 80)
    print("成功！")
    print("=" * 80)
    print(f"总论文数: {papers_data['metadata']['total_papers']}")
    print(f"类别数: {len(papers_data['categories'])}")
    print(f"输出文件: {output_file}")
    print("")
    print("所有论文都是真实的：")
    print("  ✓ 真实的 arXiv ID")
    print("  ✓ 可工作的 PDF 链接")
    print("  ✓ 真实的作者")
    print("  ✓ 真实的摘要")
    print("")
    
    # 显示统计
    print("=" * 80)
    print("论文统计")
    print("=" * 80)
    
    categories_count = {}
    for paper in papers_data["papers"]:
        cat = paper["category"]
        categories_count[cat] = categories_count.get(cat, 0) + 1
    
    for cat, count in sorted(categories_count.items()):
        print(f"{cat}: {count} 篇")
    
    # 显示几个示例
    print("")
    print("=" * 80)
    print("示例论文")
    print("=" * 80)
    for i, paper in enumerate(papers_data["papers"][:3], 1):
        print(f"\n{i}. {paper['title'][:80]}...")
        print(f"   ID: {paper['id']}")
        print(f"   作者: {', '.join(paper['authors'][:3])}")
        print(f"   PDF: {paper['pdf_url']}")


def main():
    """主函数"""
    
    print("")
    print("=" * 80)
    print("arXiv 真实论文获取工具 (使用 arxiv Python 库)")
    print("=" * 80)
    print("")
    
    if not ARXIV_INSTALLED:
        print("第一步：安装 arxiv 库")
        print("")
        print("运行:")
        print("  pip install arxiv")
        print("")
        print("然后重新运行此脚本")
        return 1
    
    print("开始获取论文...")
    print("")
    
    # 获取论文
    papers_data = fetch_papers_with_arxiv_library()
    
    if papers_data is None:
        return 1
    
    if papers_data["metadata"]["total_papers"] == 0:
        print("❌ 没有获取到论文")
        return 1
    
    # 保存数据
    save_papers(papers_data)
    
    print("")
    print("=" * 80)
    print("✅ 完成！现在可以使用真实数据运行网站了")
    print("=" * 80)
    print("")
    print("下一步:")
    print("  cd outputs")
    print("  python -m http.server 8000")
    print("  打开 http://localhost:8000")
    print("")
    
    return 0


if __name__ == "__main__":
    exit(main())
