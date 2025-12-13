# Multi-Agent Code Generation System

A sophisticated multi-agent collaborative system that autonomously generates complete software projects from natural language descriptions. Built for COMP7103C Course Assignment.

## 🎯 Project Overview

This system implements a multi-agent architecture where specialized AI agents collaborate to:
- **Plan** software projects and decompose requirements into tasks
- **Generate** production-ready code with proper structure
- **Evaluate** code quality and completeness

## 🏗️ Architecture

### Core Components

#### 1. **Agents**
- **Planning Agent**: Analyzes requirements, designs architecture, creates task lists
- **Code Generation Agent**: Implements features using file system tools and LLM function calling
- **Evaluation Agent**: Reviews code quality, validates functionality, provides feedback

#### 2. **Orchestrator**
- **Task Scheduling**: Manages task execution order and dependencies
- **Communication Management**: Coordinates information flow between agents
- **State Management**: Tracks project state and completion status

#### 3. **Tools**
- **File System Tools**: Create, read, write, and manage files
- **LLM Client**: Unified interface for multiple LLM providers (DeepSeek, OpenAI, Claude)
- **arXiv API Tools**: Fetch REAL papers from arXiv (search by category, get authentic metadata)
- **Web Search Tools**: Search the web (Brave, Google Serper, or DuckDuckGo)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd arxiv-agent-system

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Set up your LLM API key (choose one):

```bash
# For DeepSeek (recommended)
export DEEPSEEK_API_KEY="your-api-key-here"

# For OpenAI
export OPENAI_API_KEY="your-api-key-here"

# For Anthropic Claude
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Basic Usage

```bash
# Run the arXiv CS Daily project (default)
python main.py

# Specify custom output directory
python main.py --output-dir my_project

# Use different LLM provider
python main.py --provider openai

# Test without API (mock mode)
python main.py --mock
```

### Advanced Usage

```bash
# Custom project requirement
python main.py --requirement "Build a todo list web app with HTML, CSS, and JavaScript"

# Specify model and provider
python main.py --provider deepseek --model deepseek-chat

# Control iteration limit
python main.py --max-iterations 30
```

## 📁 Project Structure

```
arxiv-agent-system/
├── agents/                 # Agent implementations
│   ├── base_agent.py      # Base agent class and PlanningAgent
│   ├── code_agent.py      # Code generation agent
│   └── evaluation_agent.py # Code evaluation agent
├── orchestrator/          # Multi-agent coordination
│   └── multi_agent_orchestrator.py
├── tools/                 # Agent tools
│   ├── file_tools.py     # File system operations
│   └── llm_client.py     # LLM API wrapper
├── prompts/              # System prompts
│   └── system_prompts.py
├── config/               # Configuration
│   └── config.py
├── outputs/              # Generated code (created at runtime)
├── logs/                 # Execution logs (created at runtime)
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎓 Test Case: arXiv CS Daily Website

The default test case generates a complete "arXiv CS Daily" website with:

### Features
1. **Domain-Specific Navigation**: Browse by CS categories (cs.AI, cs.CV, cs.LG, etc.)
2. **Daily Paper List**: View latest papers with titles, dates, and categories
3. **Paper Detail Pages**: Full metadata, PDF links, and citation generation (BibTeX + standard format)

### Generated Files
- `index.html` - Homepage with category navigation
- `category.html` - Category-specific paper listings
- `paper.html` - Individual paper details
- `css/style.css` - Responsive styling
- `js/script.js` - Dynamic functionality and citation copying
- `data/papers.json` - Sample paper data

### Running the Website

After generation:
```bash
cd outputs
python -m http.server 8000
# Visit http://localhost:8000 in your browser
```

## 🔧 System Design

### Agent Communication Flow

```
User Requirement
      ↓
[Planning Agent]
      ↓ (Task List)
[Orchestrator] ← → [Code Generation Agent] ← → [File Tools]
      ↓
[Evaluation Agent]
      ↓
Complete Project
```

### Key Features

#### 1. Function Calling
Agents use LLM function calling to:
- Create and modify files programmatically
- Read project state
- Execute tools with structured parameters

#### 2. Shared Memory
- **Project Plan**: Accessible to all agents
- **Completed Files**: Track progress across tasks
- **Conversation History**: Maintain context per agent

#### 3. Task Dependency Management
- Automatic dependency resolution
- Priority-based task scheduling
- Iterative refinement capability

## 📊 Logging and Debugging

The system provides detailed logging:

```python
# Logs are saved to logs/agent_system_TIMESTAMP.log
# Console output shows:
# - Agent thoughts and decisions
# - Tool executions
# - Task progress
# - Evaluation results
```

Example log output:
```
[2024-01-15 10:30:15] [PlanningAgent] Thought: Analyzing requirement...
[2024-01-15 10:30:20] [CodeGenerationAgent] Calling tool: create_file
[2024-01-15 10:30:21] [Orchestrator] ✓ Task 1 completed - Files: index.html
```

## 🔌 LLM Provider Support

### Supported Providers
- **DeepSeek** (default): Cost-effective, good performance
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 3.5 Sonnet

### Adding New Providers

Edit `tools/llm_client.py`:
```python
self.model_map = {
    "your_provider": "model-name"
}

self.base_url_map = {
    "your_provider": "https://api.provider.com"
}
```

## 🧪 Testing

### Mock Mode (No API Required)
```bash
python main.py --mock
```

The mock client returns simulated responses, useful for:
- Testing system architecture
- Debugging agent communication
- Demo without API costs

### With Real API
```bash
# Recommended for production use
export DEEPSEEK_API_KEY="your-key"
python main.py
```

## 📈 Performance Considerations

- **API Costs**: Use `--mock` for testing, DeepSeek for cost-effective production
- **Iteration Limits**: Default 20, adjust with `--max-iterations`
- **Model Selection**: Cheaper models for planning, better models for code generation

### Recommended Configuration

**Development:**
```bash
python main.py --mock
```

**Production:**
```bash
python main.py --provider deepseek --max-iterations 15
```

## 🛠️ Extending the System

### Adding New Agents

```python
# agents/custom_agent.py
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def execute(self, task, context=None):
        # Implement custom logic
        pass
```

### Adding New Tools

```python
# tools/custom_tools.py
def my_custom_tool(param1, param2):
    return {"status": "success", "result": ...}
```

### Custom Requirements

```python
# Create your own requirement
custom_req = """
Build a portfolio website with:
- Home page
- Projects gallery
- Contact form
"""

python main.py --requirement "$custom_req"
```

## 📝 Assignment Deliverables

This project provides:

✅ **Git Repository**: Complete source code with modular architecture  
✅ **README.md**: Comprehensive documentation (this file)  
✅ **Functional System**: Generates complete arXiv CS Daily website  
✅ **Logging**: Detailed execution logs for analysis  
✅ **Extensibility**: Easy to add agents, tools, and features  

## 🎯 Learning Outcomes Demonstrated

- ✅ Multi-agent architecture design with specialized roles
- ✅ LLM API integration (DeepSeek, OpenAI, Claude)
- ✅ Function calling implementation for agent tools
- ✅ Advanced agent communication protocols
- ✅ Task decomposition and collaborative execution
- ✅ Code quality evaluation and feedback systems

## 🐛 Troubleshooting

### Common Issues

**"API Error"**
- Check API key is set correctly
- Verify internet connection
- Try `--mock` mode for testing

**"No files created"**
- Check logs for errors
- Verify output directory permissions
- Try with `--max-iterations 30`

**"Planning failed"**
- LLM may have returned invalid JSON
- System uses fallback plan automatically
- Check logs for details

## 📚 References

- LangChain: Agent framework inspiration
- AutoGen: Multi-agent patterns
- OpenAI Function Calling: Tool use patterns

## 👥 Authors

Kasper - COMP7103C Course Assignment

## 📄 License

MIT License - For educational purposes

---

## 💡 Example Execution

```bash
$ python main.py

[2024-01-15 10:00:00] [Orchestrator] INFO: STARTING MULTI-AGENT SOFTWARE DEVELOPMENT
[2024-01-15 10:00:01] [PlanningAgent] INFO: Analyzing requirement...
[2024-01-15 10:00:05] [PlanningAgent] INFO: Plan created successfully: arXiv CS Daily
[2024-01-15 10:00:06] [CodeGenerationAgent] INFO: Generating code for: index.html
[2024-01-15 10:00:12] [Orchestrator] INFO: ✓ Task 1 completed - Files: index.html
...
[2024-01-15 10:05:00] [EvaluationAgent] INFO: Evaluation Score: 85/100
[2024-01-15 10:05:00] [Orchestrator] INFO: PASSED

✓ Project completed successfully!
✓ Generated 6 files
✓ Check output at: /path/to/outputs
```

---

For questions or issues, please check the logs or refer to the course TAs.
