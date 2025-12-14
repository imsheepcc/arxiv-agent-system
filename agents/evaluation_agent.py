"""
Code Evaluation Agent implementation
"""
import json
import logging
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from tools.llm_client import LLMClient
from tools.file_tools import FileTools


class EvaluationAgent(BaseAgent):
    """Agent responsible for evaluating code quality and completeness"""
    
    def __init__(self, llm_client: LLMClient, file_tools: FileTools, command_tools=None, logger: logging.Logger = None):
        from prompts.system_prompts import EVALUATION_AGENT_PROMPT
        super().__init__(
            role="EvaluationAgent",
            system_prompt=EVALUATION_AGENT_PROMPT,
            llm_client=llm_client,
            file_tools=file_tools,
            logger=logger
        )
        self.command_tools = command_tools
    
    def execute(self, files_to_evaluate: List[str], 
                requirements: str = None,
                context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate generated code files
        
        Args:
            files_to_evaluate: List of file paths to evaluate
            requirements: Original project requirements
            context: Additional context
            
        Returns:
            Dict with evaluation results
        """
        self.add_thought(f"Evaluating {len(files_to_evaluate)} files")
        
        # Read all files
        file_contents = {}
        for file_path in files_to_evaluate:
            result = self.file_tools.read_file(file_path)
            if result["status"] == "success":
                file_contents[file_path] = result["content"]
            else:
                self.logger.warning(f"Could not read file: {file_path}")
        
        if not file_contents:
            return {
                "status": "error",
                "message": "No files could be read for evaluation"
            }
        
        tests_section = ""
        if self.command_tools:
            try:
                test_results = self.command_tools.run_tests()
                tests_section = "\nAutomated Checks (run_tests output):\n" + json.dumps(test_results, indent=2)
                self.add_thought(f"Automated checks status: {test_results.get('status')}")
            except Exception as e:
                self.logger.warning(f"run_tests failed: {e}")
                tests_section = f"\nAutomated Checks: Failed to execute ({e})"
        
        # Build evaluation prompt
        files_section = "\n\n".join([
            f"File: {path}\n```\n{content}\n```"
            for path, content in file_contents.items()
        ])
        
        requirements_section = ""
        if requirements:
            requirements_section = f"\nOriginal Requirements:\n{requirements}\n"
        
        prompt = f"""Please evaluate the following code files:

{files_section}

{requirements_section}

{tests_section}

Provide a comprehensive evaluation covering:
1. Functionality - Does the code work as intended?
2. Code Quality - Is it clean and well-structured?
3. Best Practices - Does it follow standards?
4. Completeness - Are all requirements met?
5. User Experience - Is the interface usable?

Output your evaluation in the JSON format specified in your system prompt."""
        
        self.add_message("user", prompt)
        
        # Get evaluation from LLM
        messages = self.get_messages()
        response = self.llm_client.chat(messages, temperature=0.3)
        
        if response.get("error"):
            self.logger.error(f"LLM API error: {response['content']}")
            return {"status": "error", "message": response["content"]}
        
        # Parse evaluation
        try:
            content = response["content"]
            
            # Extract JSON from response
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                evaluation = json.loads(json_str)
            else:
                # Create a basic evaluation
                evaluation = self._create_basic_evaluation(content)
            
            self.add_thought(f"Evaluation complete - Score: {evaluation.get('overall_score', 'N/A')}")
            self.logger.info(f"Evaluation completed - Passed: {evaluation.get('passed', False)}")
            
            return {
                "status": "success",
                "evaluation": evaluation
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse evaluation JSON: {e}")
            return {
                "status": "success",
                "evaluation": self._create_basic_evaluation(response["content"])
            }
    
    def _create_basic_evaluation(self, content: str) -> Dict[str, Any]:
        """Create a basic evaluation from text content"""
        
        # Simple heuristic: if response is long and doesn't mention many errors, consider it passed
        has_errors = any(word in content.lower() for word in ["error", "bug", "issue", "problem", "fail"])
        has_positive = any(word in content.lower() for word in ["good", "well", "correct", "properly", "success"])
        
        score = 70 if has_positive else 50
        if has_errors:
            score -= 20
        
        return {
            "overall_score": score,
            "passed": score >= 60,
            "issues": [],
            "strengths": ["Code was generated and reviewed"],
            "recommendations": ["Review the evaluation text for specific feedback"],
            "evaluation_text": content
        }
    
    def quick_check(self, file_path: str) -> bool:
        """
        Quick check if a file exists and is not empty
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file exists and has content
        """
        result = self.file_tools.read_file(file_path)
        
        if result["status"] == "success":
            content = result.get("content", "")
            return len(content.strip()) > 0
        
        return False
