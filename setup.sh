#!/bin/bash

# 自动设置脚本 - arxiv-agent-system
# 这个脚本会验证和修复项目结构

echo "======================================================================"
echo "  arxiv-agent-system 自动设置脚本"
echo "======================================================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "❌ 错误: 请在 arxiv-agent-system 目录下运行此脚本"
    echo "   当前目录: $(pwd)"
    echo "   请使用: cd arxiv-agent-system && bash setup.sh"
    exit 1
fi

echo "✓ 在正确的目录中"
echo ""

# 创建必需的目录
echo "检查目录结构..."
mkdir -p agents orchestrator tools prompts config scripts outputs/data outputs/css outputs/js logs

# 创建 __init__.py 文件
touch agents/__init__.py
touch orchestrator/__init__.py
touch tools/__init__.py
touch prompts/__init__.py
touch config/__init__.py

echo "✓ 目录结构已创建"
echo ""

# 检查必需文件
echo "检查必需文件..."
required_files=(
    "agents/base_agent.py"
    "agents/code_agent.py"
    "agents/evaluation_agent.py"
    "orchestrator/multi_agent_orchestrator.py"
    "tools/file_tools.py"
    "tools/llm_client.py"
    "tools/enhanced_mock_client.py"
    "tools/arxiv_tools.py"
    "tools/web_search_tools.py"
    "prompts/system_prompts.py"
    "config/config.py"
    "scripts/fetch_arxiv_papers.py"
    "main.py"
    "test_system.py"
    "requirements.txt"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "❌ 缺少以下文件:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "请确保所有文件都已下载到正确位置"
    exit 1
else
    echo "✓ 所有必需文件都存在 (${#required_files[@]}/18)"
fi
echo ""

# 检查 Python
echo "检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装"
    exit 1
fi
python_version=$(python3 --version)
echo "✓ $python_version"
echo ""

# 安装依赖
echo "安装 Python 依赖..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt -q
    echo "✓ 依赖已安装"
else
    echo "❌ requirements.txt 不存在"
    exit 1
fi
echo ""

# 测试导入
echo "测试模块导入..."
python3 << 'PYEOF'
import sys
sys.path.insert(0, '.')

try:
    from agents.base_agent import PlanningAgent
    from agents.code_agent import CodeGenerationAgent
    from agents.evaluation_agent import EvaluationAgent
    from orchestrator.multi_agent_orchestrator import MultiAgentOrchestrator
    from tools.file_tools import FileTools
    from tools.arxiv_tools import ArxivTools
    from tools.web_search_tools import WebSearchTools
    print("✓ 所有模块导入成功")
    exit(0)
except Exception as e:
    print(f"❌ 模块导入失败: {e}")
    exit(1)
PYEOF

if [ $? -ne 0 ]; then
    exit 1
fi
echo ""

# 运行测试
echo "运行系统测试..."
python3 test_system.py
echo ""

# 创建启动脚本
echo "创建启动脚本..."

# Mac/Linux 启动脚本
cat > run.sh << 'RUNEOF'
#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 main.py "$@"
RUNEOF
chmod +x run.sh
echo "✓ 创建 run.sh (Mac/Linux)"

# Windows 启动脚本
cat > run.bat << 'BATEOF'
@echo off
set PYTHONPATH=%PYTHONPATH%;%cd%
python main.py %*
BATEOF
echo "✓ 创建 run.bat (Windows)"
echo ""

echo "======================================================================"
echo "  ✅ 设置完成！"
echo "======================================================================"
echo ""
echo "快速开始:"
echo ""
echo "  1. 测试 arXiv API:"
echo "     ./run.sh tools/arxiv_tools.py"
echo "     或: PYTHONPATH=. python3 tools/arxiv_tools.py"
echo ""
echo "  2. 测试 Web Search:"
echo "     ./run.sh tools/web_search_tools.py"
echo "     或: PYTHONPATH=. python3 tools/web_search_tools.py"
echo ""
echo "  3. 获取真实 arXiv 数据:"
echo "     PYTHONPATH=. python3 scripts/fetch_arxiv_papers.py"
echo ""
echo "  4. 运行多智能体系统:"
echo "     ./run.sh --mock"
echo "     或: python3 main.py --mock"
echo ""
echo "  5. 查看生成的网站:"
echo "     cd outputs && python3 -m http.server 8000"
echo "     然后访问 http://localhost:8000"
echo ""
echo "======================================================================"
