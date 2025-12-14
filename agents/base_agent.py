"""
Base Agent class and specialized agent implementations
"""
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from protocol.message_schema import AgentMessage
from tools.llm_client import LLMClient
from tools.file_tools import FileTools


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, role: str, system_prompt: str, llm_client: LLMClient, 
                 file_tools: FileTools = None, logger: logging.Logger = None):
        """
        Initialize base agent
        
        Args:
            role: Agent role name
            system_prompt: System prompt for the agent
            llm_client: LLM client for API calls
            file_tools: File tools for file operations
            logger: Logger instance
        """
        self.role = role
        self.system_prompt = system_prompt
        self.llm_client = llm_client
        self.file_tools = file_tools or FileTools()
        self.logger = logger or self._setup_logger()
        
        self.conversation_history = []
        self.thoughts = []
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the agent"""
        logger = logging.getLogger(self.role)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'[%(asctime)s] [{self.role}] %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def record_protocol_message(self, message: AgentMessage, role: str = "system"):
        """Record a protocol message (as JSON payload) into conversation history"""
        if not isinstance(message, AgentMessage):
            return
        content = "[PROTOCOL MESSAGE]\n" + message.to_json(pretty=True)
        self.add_message(role, content)
        self.logger.debug(f"Recorded protocol message {message.msg_type.value} ({message.id})")
    
    def add_thought(self, thought: str):
        """Record agent's thought process"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.thoughts.append(f"[{timestamp}] {thought}")
        self.logger.info(f"Thought: {thought}")
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages including system prompt"""
        return [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
    
    def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a task (to be implemented by subclasses)
        
        Args:
            task: Task description
            context: Additional context
            
        Returns:
            Result dictionary
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def reset(self):
        """Reset agent state"""
        self.conversation_history = []
        self.thoughts = []

    def export_memory(self) -> Dict[str, Any]:
        """Export agent memory for persistence"""
        return {
            "conversation_history": list(self.conversation_history),
            "thoughts": list(self.thoughts)
        }

    def load_memory(self, memory: Dict[str, Any]):
        """Load agent memory from persisted state"""
        if not memory:
            return
        self.conversation_history = memory.get("conversation_history", []) or []
        self.thoughts = memory.get("thoughts", []) or []


class PlanningAgent(BaseAgent):
    """Agent responsible for project planning and task decomposition"""
    
    def __init__(self, llm_client: LLMClient, logger: logging.Logger = None):
        from prompts.system_prompts import PLANNING_AGENT_PROMPT
        super().__init__(
            role="PlanningAgent",
            system_prompt=PLANNING_AGENT_PROMPT,
            llm_client=llm_client,
            logger=logger
        )
    
    def execute(self, requirement: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a project plan from requirements
        
        Args:
            requirement: Project requirement description
            context: Additional context
            
        Returns:
            Dict containing project plan with tasks
        """
        self.add_thought(f"Analyzing requirement: {requirement[:100]}...")
        
        # Prepare the prompt
        self.add_message("user", f"""Please analyze the following project requirement and create a detailed project plan:

Requirement:
{requirement}

Provide a comprehensive plan with:
1. Project overview
2. Technology stack
3. File structure
4. Detailed task list with specifications

Output the plan in the JSON format specified in your system prompt.""")
        
        # Get response from LLM
        messages = self.get_messages()
        response = self.llm_client.chat(messages, temperature=0.3)
        
        if response.get("error"):
            self.logger.error(f"LLM API error: {response['content']}")
            return {"status": "error", "message": response["content"]}
        
        # Parse the plan
        try:
            # Extract JSON from response
            content = response["content"]
            
            # Try to find JSON in the response
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                plan = json.loads(json_str)
            else:
                # If no JSON found, create a basic plan
                self.logger.warning("Could not parse JSON from response, creating basic plan")
                plan = self._create_fallback_plan(requirement)
            
            self.add_thought(f"Created plan with {len(plan.get('tasks', []))} tasks")
            self.logger.info(f"Plan created successfully: {plan.get('project_name', 'Unknown')}")
            
            return {
                "status": "success",
                "plan": plan
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse plan JSON: {e}")
            # Return a fallback plan
            return {
                "status": "success",
                "plan": self._create_fallback_plan(requirement)
            }
    
    def _create_fallback_plan(self, requirement: str) -> Dict[str, Any]:
        """Create a basic fallback plan"""
        return {
            "project_name": "arXiv CS Daily",
            "technology_stack": ["html", "css", "javascript"],
            "file_structure": {
                "index.html": "Homepage",
                "category.html": "Category page",
                "paper.html": "Paper detail page",
                "css/style.css": "Styling",
                "js/script.js": "JavaScript",
                "data/papers.json": "Sample data"
            },
            "tasks": [
                {
                    "id": 1,
                    "title": "Create sample data",
                    "description": "Create papers.json with sample arXiv papers",
                    "file_path": "data/papers.json",
                    "dependencies": [],
                    "priority": "high"
                },
                {
                    "id": 2,
                    "title": "Create homepage",
                    "description": "Create index.html with navigation and category links",
                    "file_path": "index.html",
                    "dependencies": [1],
                    "priority": "high"
                },
                {
                    "id": 3,
                    "title": "Create category page",
                    "description": "Create category.html to display papers by category",
                    "file_path": "category.html",
                    "dependencies": [1],
                    "priority": "high"
                },
                {
                    "id": 4,
                    "title": "Create paper detail page",
                    "description": "Create paper.html with full paper details and citations",
                    "file_path": "paper.html",
                    "dependencies": [1],
                    "priority": "high"
                },
                {
                    "id": 5,
                    "title": "Add CSS styling",
                    "description": "Create style.css with responsive design",
                    "file_path": "css/style.css",
                    "dependencies": [2, 3, 4],
                    "priority": "medium"
                },
                {
                    "id": 6,
                    "title": "Add JavaScript functionality",
                    "description": "Create script.js for dynamic features and citations",
                    "file_path": "js/script.js",
                    "dependencies": [2, 3, 4],
                    "priority": "medium"
                }
            ]
        }
