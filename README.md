# Multi-Agent Collaborative System for Automated Code Generation

**Course**: COMP7103C - Assignment

**Project**: Code Agent Building

**Student**: YANG Chen, ZENG Hua

## Overview

This project implements a multi-agent system that autonomously generates complete software projects from natural language requirements. The system demonstrates advanced agent coordination, LLM integration, external API usage, and collaborative problem-solving capabilities.

## System Architecture

### Agent Roles

The system consists of three specialized agents coordinated by a central orchestrator:

1. **Planning Agent**
   - Analyzes project requirements
   - Designs system architecture
   - Decomposes requirements into executable tasks
   - Creates structured task lists with dependencies

2. **Code Generation Agent**
   - Implements features using function calling
   - Utilizes multiple tools (file operations, arXiv API, web search)
   - Generates production-ready code
   - Fetches real data from external sources

3. **Evaluation Agent**
   - Reviews code quality and completeness
   - Validates functionality
   - Provides structured feedback
   - Assigns quality scores

### Multi-Agent Orchestrator

- Coordinates communication between agents
- Manages task execution flow
- Maintains shared state and project context
- Handles iterative refinement

### Tool Integration

The system integrates four categories of tools:

1. **File System Tools**: Create, read, write, and manage files
2. **arXiv API Tools**: Fetch real academic papers with authentic metadata
3. **Web Search Tools**: Search the web using multiple providers (Brave, Serper, DuckDuckGo)
4. **LLM Clients**: Support for DeepSeek, OpenAI, and Claude APIs

## Key Features

### 1. Function Calling Implementation

Agents use OpenAI-compatible function calling to execute tools:

```python
{
  "type": "function",
  "function": {
    "name": "search_arxiv_papers",
    "description": "Search for papers from arXiv by category",
    "parameters": {
      "type": "object",
      "properties": {
        "category": {"type": "string", "enum": ["cs.AI", "cs.CV", ...]},
        "max_results": {"type": "integer"}
      }
    }
  }
}
```

### 2. External Knowledge Integration

The system integrates real-world data sources:

- **arXiv API**: Fetches authentic academic papers with real IDs, authors, and PDF links
- **Web Search**: Retrieves current information from the internet
- **Structured Data**: Processes XML/JSON responses into usable formats

### 3. Multi-Provider LLM Support

Supports multiple LLM providers with unified interface:
- DeepSeek (cost-effective)
- OpenAI GPT-4/3.5
- Anthropic Claude 3.5

### 4. Shared State Management

All agents access:
- Project plan and architecture
- Completed files and task status
- Conversation history for context

## Installation and Setup

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt

# For real arXiv data (optional)
pip install arxiv
```

### Configuration

Set your LLM API key:

```bash
# DeepSeek (recommended)
export DEEPSEEK_API_KEY="your-api-key"

# OpenAI (alternative)
export OPENAI_API_KEY="your-api-key"

# Claude (alternative)
export ANTHROPIC_API_KEY="your-api-key"
```

## Usage

### Basic Execution

```bash
# Run with default test case (arXiv CS Daily)
python main.py

# Use specific LLM provider
python main.py --provider openai

# Test system architecture without API
python main.py --mock
```

### Fetching Real arXiv Data

```bash
# Method 1: Using arxiv library (recommended)
pip install arxiv
python scripts/fetch_real_papers.py

# Method 2: Direct API access
PYTHONPATH=. python scripts/fetch_arxiv_papers.py

# Method 3: One-click script
bash get_real_data.sh
```

### Viewing Generated Website

```bash
cd outputs
python -m http.server 8000
# Visit http://localhost:8000
```

## Project Structure

```
arxiv-agent-system/
├── agents/
│   ├── base_agent.py           # Base agent class + Planning Agent
│   ├── code_agent.py           # Code Generation Agent
│   └── evaluation_agent.py     # Evaluation Agent
├── orchestrator/
│   └── multi_agent_orchestrator.py  # Agent coordination
├── tools/
│   ├── file_tools.py           # File operations
│   ├── arxiv_tools.py          # arXiv API integration
│   ├── web_search_tools.py     # Web search (Brave/Serper/DuckDuckGo)
│   └── llm_client.py           # LLM provider wrapper
├── prompts/
│   └── system_prompts.py       # Agent system prompts
├── config/
│   └── config.py               # System configuration
├── scripts/
│   ├── fetch_arxiv_papers.py   # Fetch real papers (API)
│   └── fetch_real_papers.py    # Fetch real papers (arxiv library)
├── outputs/                     # Generated website files
├── logs/                        # Execution logs
├── main.py                      # Main entry point
├── test_system.py              # System tests
└── README.md                    # This file
```

## Test Case: arXiv CS Daily Website

The system generates a complete academic paper tracking website:

### Generated Components

1. **Homepage** (`index.html`)
   - Hero section with project description
   - Category cards for CS subfields
   - Navigation menu

2. **Category Pages** (`category.html`)
   - Papers filtered by category (cs.AI, cs.CV, cs.LG, etc.)
   - Date-based filtering
   - Paper metadata display

3. **Paper Detail Pages** (`paper.html`)
   - Complete paper information
   - Author affiliations
   - Abstract and keywords
   - Links to PDF and arXiv page

4. **Styling** (`css/style.css`)
   - Responsive design
   - Professional appearance
   - Accessible color scheme

5. **Functionality** (`js/script.js`)
   - Dynamic content loading
   - Category filtering
   - Date-based sorting

6. **Data** (`data/papers.json`)
   - Real papers from arXiv API
   - Authentic IDs, authors, and metadata
   - Working PDF links

### Data Authenticity

Papers fetched from arXiv contain:
- Real paper IDs (e.g., `2412.11798v1`)
- Authentic author names and affiliations
- Actual abstracts and publication dates
- Functional PDF links to arXiv.org

## Agent Communication Protocol

### Message Flow

```
1. User provides requirement
   ↓
2. Planning Agent creates structured plan
   ↓
3. Orchestrator distributes tasks
   ↓
4. Code Generation Agent executes tasks
   - Uses file tools to create files
   - Calls arXiv API for real data
   - Uses web search when needed
   ↓
5. Evaluation Agent reviews output
   ↓
6. Orchestrator decides: complete or refine
```

### Shared Context

All agents access:
- Project requirements
- Current plan and architecture
- List of completed files
- Task execution history
- Previous agent responses

## Technical Implementation

### Function Calling Example

```python
# Agent generates function call
{
  "tool_calls": [{
    "function": {
      "name": "search_arxiv_papers",
      "arguments": {
        "category": "cs.AI",
        "max_results": 6
      }
    }
  }]
}

# System executes and returns
{
  "status": "success",
  "papers": [
    {
      "id": "2412.11798v1",
      "title": "Particulate: Feed-Forward 3D Object Articulation",
      "authors": ["Ruining Li", "Yuxin Yao", ...],
      "pdf_url": "https://arxiv.org/pdf/2412.11798v1.pdf"
    }
  ]
}
```

### Error Handling

- Automatic retry on API failures
- Fallback to alternative providers
- Graceful degradation (mock data if APIs unavailable)
- Detailed error logging

## System Evaluation

### Quantitative Metrics

- **Code Completeness**: All required files generated (6/6)
- **Functionality**: Working navigation, filtering, and data display
- **Data Quality**: Real papers with authentic metadata (30+ papers)
- **Evaluation Score**: 88/100 (by Evaluation Agent)

### Qualitative Assessment

- Clean, professional UI design
- Responsive layout
- Proper error handling
- Extensible architecture

## Course Requirements Fulfillment

| Requirement | Implementation | Status |
|------------|----------------|--------|
| Multi-Agent System | 3 specialized agents + orchestrator | ✅ |
| Agent Roles | Planning, Code Generation, Evaluation | ✅ |
| Task Decomposition | Structured plan with dependencies | ✅ |
| LLM Integration | DeepSeek/OpenAI/Claude support | ✅ |
| Function Calling | OpenAI-format tool definitions | ✅ |
| Tool Kit | File + arXiv + Web Search tools | ✅ |
| External Knowledge | Real data from arXiv API | ✅ |
| Communication Protocol | Shared state + message passing | ✅ |
| Test Case | arXiv CS Daily website | ✅ |
| Documentation | Comprehensive README | ✅ |

## Testing

### System Tests

```bash
# Run unit tests
python test_system.py
```

Expected output:
```
✓ All imports successful
✓ File tools working
✓ Mock LLM client working
✓ Agents initialized correctly
✓ Generated files exist

5/5 tests PASSED ✅
```

### Integration Tests

Test with real APIs:
```bash
# Test arXiv API
PYTHONPATH=. python tools/arxiv_tools.py

# Test Web Search
PYTHONPATH=. python tools/web_search_tools.py
```

## Limitations and Future Work

### Current Limitations
- arXiv API has rate limits (3 seconds between requests)
- Web search requires API keys for best performance
- Generated code requires manual deployment

### Potential Enhancements
- Add more agent types (Testing Agent, Documentation Agent)
- Implement more sophisticated task scheduling
- Add support for more data sources
- Implement automatic deployment

## Logging

Detailed logs are saved to `logs/agent_system_TIMESTAMP.log`:

```
[2024-12-15 10:00:00] [Orchestrator] Starting multi-agent system
[2024-12-15 10:00:01] [PlanningAgent] Analyzing requirement...
[2024-12-15 10:00:05] [CodeGenerationAgent] Calling tool: create_file
[2024-12-15 10:00:06] [CodeGenerationAgent] Calling tool: search_arxiv_papers
[2024-12-15 10:00:10] [Orchestrator] Task completed: index.html
[2024-12-15 10:05:00] [EvaluationAgent] Score: 88/100
```

## References

- OpenAI Function Calling API: https://platform.openai.com/docs/guides/function-calling
- arXiv API Documentation: https://info.arxiv.org/help/api/
- AutoGen Framework: Multi-agent patterns
- LangChain: Agent tooling patterns

---

**Note**: This system demonstrates practical multi-agent collaboration for automated software development. All components are designed for educational purposes as part of the COMP7103C course requirements.
