#!/bin/bash

# 一键获取真实 arXiv 数据
# 使用方法: bash get_real_data.sh

echo "========================================================================"
echo "  一键获取真实 arXiv 论文数据"
echo "========================================================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python 未安装"
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)
echo "✓ 使用 Python: $PYTHON_CMD"
echo ""

# 安装 arxiv 库
echo "正在安装 arxiv 库..."
$PYTHON_CMD -m pip install arxiv -q

if [ $? -eq 0 ]; then
    echo "✓ arxiv 库已安装"
else
    echo "❌ 安装失败，尝试使用系统 API..."
fi
echo ""

# 运行获取脚本
echo "开始获取真实论文..."
echo ""

if [ -f "scripts/fetch_real_papers.py" ]; then
    $PYTHON_CMD scripts/fetch_real_papers.py
    EXIT_CODE=$?
elif [ -f "scripts/fetch_arxiv_papers.py" ]; then
    echo "⚠️  使用备用脚本..."
    PYTHONPATH=. $PYTHON_CMD scripts/fetch_arxiv_papers.py
    EXIT_CODE=$?
else
    echo "❌ 找不到获取脚本"
    exit 1
fi

echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo "========================================================================"
    echo "  ✅ 成功！"
    echo "========================================================================"
    echo ""
    echo "检查数据："
    
    if [ -f "outputs/data/papers.json" ]; then
        PAPER_COUNT=$($PYTHON_CMD -c "import json; print(len(json.load(open('outputs/data/papers.json'))['papers']))" 2>/dev/null || echo "0")
        echo "  论文数量: $PAPER_COUNT"
        
        if [ "$PAPER_COUNT" -gt "0" ]; then
            echo ""
            echo "示例论文："
            $PYTHON_CMD << 'PYEOF'
import json
data = json.load(open('outputs/data/papers.json'))
if data['papers']:
    paper = data['papers'][0]
    print(f"  标题: {paper['title'][:60]}...")
    print(f"  ID: {paper['id']}")
    print(f"  PDF: {paper['pdf_url']}")
PYEOF
            echo ""
            echo "✅ 所有 PDF 链接都是真实可用的！"
        fi
    fi
    
    echo ""
    echo "下一步："
    echo "  cd outputs"
    echo "  python -m http.server 8000"
    echo "  打开 http://localhost:8000"
else
    echo "========================================================================"
    echo "  ⚠️  获取数据时出现问题"
    echo "========================================================================"
    echo ""
    echo "请尝试："
    echo "  1. 检查网络连接"
    echo "  2. 手动运行: python scripts/fetch_real_papers.py"
    echo "  3. 查看 GET_REAL_DATA_GUIDE.md 获取详细帮助"
fi

echo ""
echo "========================================================================"
