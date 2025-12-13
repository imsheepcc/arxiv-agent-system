"""
Multi-Agent Orchestrator - Coordinates multiple agents to complete software projects
"""
import json
import logging
from typing import Dict, Any, List
from datetime import datetime

from agents.base_agent import PlanningAgent
from agents.code_agent import CodeGenerationAgent
from agents.evaluation_agent import EvaluationAgent
from tools.llm_client import LLMClient
from tools.file_tools import FileTools


class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents to collaboratively complete software development tasks
    """
    
    def __init__(self, llm_client: LLMClient = None, output_dir: str = None, 
                 use_arxiv: bool = True, use_web_search: bool = True):
        """
        Initialize the orchestrator
        
        Args:
            llm_client: LLM client for API calls
            output_dir: Directory for output files
            use_arxiv: Whether to enable arXiv API tools
            use_web_search: Whether to enable web search tools
        """
        # Setup logging
        self.logger = self._setup_logger()
        
        # Initialize LLM client
        self.llm_client = llm_client or LLMClient(provider="deepseek")
        
        # Initialize file tools
        self.file_tools = FileTools(base_dir=output_dir)
        
        # Initialize arXiv tools
        self.arxiv_tools = None
        if use_arxiv:
            try:
                from tools.arxiv_tools import ArxivTools
                self.arxiv_tools = ArxivTools()
                self.logger.info("arXiv API tools enabled")
            except Exception as e:
                self.logger.warning(f"Could not initialize arXiv tools: {e}")
        
        # Initialize web search tools
        self.web_search_tools = None
        if use_web_search:
            try:
                from tools.web_search_tools import WebSearchTools
                self.web_search_tools = WebSearchTools()
                self.logger.info(f"Web search tools enabled (provider: {self.web_search_tools.provider})")
            except Exception as e:
                self.logger.warning(f"Could not initialize web search tools: {e}")
        
        # Initialize agents
        self.planning_agent = PlanningAgent(self.llm_client, self.logger)
        self.code_agent = CodeGenerationAgent(
            self.llm_client, 
            self.file_tools,
            self.arxiv_tools,
            self.web_search_tools,
            self.logger
        )
        self.eval_agent = EvaluationAgent(self.llm_client, self.file_tools, self.logger)
        
        # Shared state
        self.project_plan = None
        self.completed_tasks = []
        self.created_files = []
        self.task_results = {}
        
        self.logger.info("Multi-Agent Orchestrator initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup orchestrator logger"""
        logger = logging.getLogger("Orchestrator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '[%(asctime)s] [%(name)s] %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def run(self, requirement: str, max_iterations: int = 20) -> Dict[str, Any]:
        """
        Execute the complete software development workflow
        
        Args:
            requirement: Project requirement description
            max_iterations: Maximum number of task execution iterations
            
        Returns:
            Dict with execution results
        """
        self.logger.info("="*80)
        self.logger.info("STARTING MULTI-AGENT SOFTWARE DEVELOPMENT")
        self.logger.info("="*80)
        
        start_time = datetime.now()
        
        # Phase 1: Planning
        self.logger.info("\n[PHASE 1] PROJECT PLANNING")
        self.logger.info("-"*80)
        
        planning_result = self.planning_agent.execute(requirement)
        
        if planning_result["status"] != "success":
            self.logger.error("Planning failed!")
            return {
                "status": "error",
                "message": "Planning phase failed",
                "error": planning_result.get("message")
            }
        
        self.project_plan = planning_result["plan"]
        self.logger.info(f"Project: {self.project_plan.get('project_name', 'Unknown')}")
        self.logger.info(f"Tasks planned: {len(self.project_plan.get('tasks', []))}")
        
        # Phase 2: Task Execution
        self.logger.info("\n[PHASE 2] CODE GENERATION")
        self.logger.info("-"*80)
        
        tasks = self.project_plan.get("tasks", [])
        
        if not tasks:
            self.logger.warning("No tasks in project plan!")
            tasks = self._create_default_tasks()
        
        # Sort tasks by priority and dependencies
        sorted_tasks = self._sort_tasks(tasks)
        
        iteration = 0
        for task in sorted_tasks:
            if iteration >= max_iterations:
                self.logger.warning(f"Reached max iterations ({max_iterations})")
                break
            
            iteration += 1
            
            task_id = task.get("id", iteration)
            task_title = task.get("title", f"Task {task_id}")
            
            self.logger.info(f"\n>>> Executing Task {task_id}: {task_title}")
            
            # Check dependencies
            if not self._check_dependencies(task):
                self.logger.warning(f"Dependencies not met for task {task_id}, deferring...")
                # Add back to queue
                sorted_tasks.append(task)
                continue
            
            # Execute code generation
            context = {
                "project_plan": self.project_plan,
                "completed_files": self.created_files,
                "completed_tasks": self.completed_tasks
            }
            
            code_result = self.code_agent.execute(task, context)
            
            if code_result["status"] == "success":
                files = code_result.get("files_created", [])
                self.created_files.extend(files)
                self.completed_tasks.append(task_id)
                self.task_results[task_id] = code_result
                
                self.logger.info(f"✓ Task {task_id} completed - Files: {', '.join(files)}")
            else:
                self.logger.error(f"✗ Task {task_id} failed: {code_result.get('message')}")
                # Continue with other tasks
        
        # Phase 3: Evaluation
        self.logger.info("\n[PHASE 3] CODE EVALUATION")
        self.logger.info("-"*80)
        
        if self.created_files:
            eval_result = self.eval_agent.execute(
                files_to_evaluate=self.created_files,
                requirements=requirement,
                context={"project_plan": self.project_plan}
            )
            
            if eval_result["status"] == "success":
                evaluation = eval_result["evaluation"]
                score = evaluation.get("overall_score", 0)
                passed = evaluation.get("passed", False)
                
                self.logger.info(f"Evaluation Score: {score}/100")
                self.logger.info(f"Status: {'PASSED' if passed else 'NEEDS IMPROVEMENT'}")
                
                if evaluation.get("issues"):
                    self.logger.info(f"Issues found: {len(evaluation['issues'])}")
                    for issue in evaluation["issues"][:3]:  # Show first 3
                        self.logger.info(f"  - [{issue.get('severity', 'unknown')}] {issue.get('description', '')}")
            else:
                self.logger.warning("Evaluation failed")
                evaluation = None
        else:
            self.logger.warning("No files created - skipping evaluation")
            evaluation = None
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.logger.info("\n" + "="*80)
        self.logger.info("EXECUTION SUMMARY")
        self.logger.info("="*80)
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"Tasks completed: {len(self.completed_tasks)}/{len(tasks)}")
        self.logger.info(f"Files created: {len(self.created_files)}")
        self.logger.info(f"Output directory: {self.file_tools.base_dir}")
        
        if self.created_files:
            self.logger.info("\nCreated files:")
            for f in self.created_files:
                self.logger.info(f"  - {f}")
        
        return {
            "status": "success",
            "project_plan": self.project_plan,
            "completed_tasks": self.completed_tasks,
            "created_files": self.created_files,
            "evaluation": evaluation,
            "duration": duration,
            "output_dir": self.file_tools.base_dir
        }
    
    def _sort_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort tasks by priority and dependencies
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            Sorted list of tasks
        """
        # Simple sorting: high priority first, then by task id
        priority_order = {"high": 0, "medium": 1, "low": 2}
        
        return sorted(tasks, key=lambda t: (
            priority_order.get(t.get("priority", "medium"), 1),
            t.get("id", 999)
        ))
    
    def _check_dependencies(self, task: Dict[str, Any]) -> bool:
        """
        Check if task dependencies are met
        
        Args:
            task: Task dictionary
            
        Returns:
            True if all dependencies are completed
        """
        dependencies = task.get("dependencies", [])
        
        if not dependencies:
            return True
        
        for dep_id in dependencies:
            if dep_id not in self.completed_tasks:
                return False
        
        return True
    
    def _create_default_tasks(self) -> List[Dict[str, Any]]:
        """Create default tasks if planning failed"""
        return [
            {
                "id": 1,
                "title": "Create basic HTML structure",
                "description": "Create a basic HTML file",
                "file_path": "index.html",
                "dependencies": [],
                "priority": "high"
            }
        ]
    
    def get_project_summary(self) -> str:
        """
        Get a summary of the project execution
        
        Returns:
            Formatted summary string
        """
        summary = []
        summary.append("="*80)
        summary.append("PROJECT SUMMARY")
        summary.append("="*80)
        
        if self.project_plan:
            summary.append(f"\nProject: {self.project_plan.get('project_name', 'Unknown')}")
            summary.append(f"Technology: {', '.join(self.project_plan.get('technology_stack', []))}")
        
        summary.append(f"\nTasks Completed: {len(self.completed_tasks)}")
        summary.append(f"Files Created: {len(self.created_files)}")
        
        if self.created_files:
            summary.append("\nGenerated Files:")
            for f in self.created_files:
                summary.append(f"  - {f}")
        
        summary.append(f"\nOutput Location: {self.file_tools.base_dir}")
        summary.append("="*80)
        
        return "\n".join(summary)
