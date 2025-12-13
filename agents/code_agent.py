"""
Code Generation Agent implementation
"""
import json
import logging
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from tools.llm_client import LLMClient
from tools.file_tools import FileTools


class CodeGenerationAgent(BaseAgent):
    """Agent responsible for generating code based on task specifications"""
    
    def __init__(self, llm_client: LLMClient, file_tools: FileTools, 
                 arxiv_tools=None, web_search_tools=None, logger: logging.Logger = None):
        from prompts.system_prompts import CODE_GENERATION_AGENT_PROMPT
        super().__init__(
            role="CodeGenerationAgent",
            system_prompt=CODE_GENERATION_AGENT_PROMPT,
            llm_client=llm_client,
            file_tools=file_tools,
            logger=logger
        )
        self.arxiv_tools = arxiv_tools
        self.web_search_tools = web_search_tools
    
    def execute(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate code for a specific task
        
        Args:
            task: Task dictionary with description and file_path
            context: Additional context (e.g., project plan, other files)
            
        Returns:
            Dict with status and result
        """
        task_title = task.get("title", "Unknown task")
        task_desc = task.get("description", "")
        file_path = task.get("file_path", "")
        
        self.add_thought(f"Starting task: {task_title}")
        self.logger.info(f"Generating code for: {file_path}")
        
        # Build context for the agent
        context_info = ""
        if context:
            if "project_plan" in context:
                plan = context["project_plan"]
                context_info += f"\nProject: {plan.get('project_name', 'Unknown')}"
                context_info += f"\nTechnology Stack: {', '.join(plan.get('technology_stack', []))}"
            
            if "completed_files" in context:
                context_info += f"\n\nCompleted files: {', '.join(context['completed_files'])}"
        
        # Create the prompt
        prompt = f"""Task: {task_title}

Description:
{task_desc}

Target File: {file_path}

{context_info}

Please implement this task by creating or modifying the specified file. Use the available tools to create the file with complete, production-ready code.

IMPORTANT: You must use the create_file tool to actually create the file. Include all necessary code in the file content."""
        
        self.add_message("user", prompt)
        
        # Get tools for function calling
        tools = self.file_tools.get_tool_definitions()
        
        # Add arXiv tools if available
        if self.arxiv_tools:
            tools.extend(self.arxiv_tools.get_tool_definitions())
        
        # Add web search tools if available
        if self.web_search_tools:
            tools.extend(self.web_search_tools.get_tool_definitions())
        
        # Call LLM with tools
        messages = self.get_messages()
        max_iterations = 5
        iteration = 0
        
        files_created = []
        
        while iteration < max_iterations:
            iteration += 1
            
            response = self.llm_client.chat(messages, temperature=0.4, tools=tools)
            
            if response.get("error"):
                self.logger.error(f"LLM API error: {response['content']}")
                return {"status": "error", "message": response["content"]}
            
            # Add assistant message to history
            self.add_message("assistant", response.get("content", ""))
            
            # Check for tool calls
            if "tool_calls" in response:
                for tool_call in response["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = json.loads(tool_call["function"]["arguments"])
                    
                    self.add_thought(f"Calling tool: {tool_name} with args: {tool_args}")
                    
                    # Execute the tool
                    result = self._execute_tool(tool_name, tool_args)
                    
                    if result["status"] == "success" and tool_name == "create_file":
                        files_created.append(tool_args["path"])
                    
                    # Add tool result to conversation
                    tool_result_message = {
                        "role": "tool",
                        "tool_call_id": tool_call.get("id", ""),
                        "name": tool_name,
                        "content": json.dumps(result)
                    }
                    
                    # For OpenAI-style APIs
                    self.conversation_history.append(tool_result_message)
                    
                    self.logger.info(f"Tool {tool_name} result: {result['message']}")
                
                # Continue the conversation to see if more tools are needed
                continue
            else:
                # No more tool calls, task is complete
                break
        
        if files_created:
            self.add_thought(f"Successfully created files: {files_created}")
            return {
                "status": "success",
                "files_created": files_created,
                "message": f"Task '{task_title}' completed successfully"
            }
        else:
            # If no files were created via tools, try to extract code from response
            return self._fallback_file_creation(task, response.get("content", ""))
    
    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool (file, arXiv, or web search)"""
        
        # File tools
        if tool_name == "create_file":
            return self.file_tools.create_file(args["path"], args.get("content", ""))
        elif tool_name == "write_to_file":
            return self.file_tools.write_to_file(
                args["path"], 
                args.get("content", ""), 
                args.get("mode", "w")
            )
        elif tool_name == "read_file":
            return self.file_tools.read_file(args["path"])
        elif tool_name == "list_directory":
            return self.file_tools.list_directory(args.get("path", ""))
        
        # arXiv tools
        elif tool_name == "search_arxiv_papers" and self.arxiv_tools:
            return self.arxiv_tools.search_papers(
                category=args.get("category", "cs.AI"),
                max_results=args.get("max_results", 10)
            )
        elif tool_name == "fetch_multiple_categories" and self.arxiv_tools:
            return self.arxiv_tools.fetch_multiple_categories(
                categories=args.get("categories", ["cs.AI"]),
                papers_per_category=args.get("papers_per_category", 5)
            )
        
        # Web search tools
        elif tool_name == "web_search" and self.web_search_tools:
            return self.web_search_tools.search(
                query=args.get("query", ""),
                num_results=args.get("num_results", 5)
            )
        elif tool_name == "fetch_url" and self.web_search_tools:
            return self.web_search_tools.fetch_url(args.get("url", ""))
        
        else:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool_name}"
            }
    
    def _fallback_file_creation(self, task: Dict[str, Any], response_content: str) -> Dict[str, Any]:
        """
        Fallback method to create file if tools weren't used
        Extract code from markdown code blocks
        """
        file_path = task.get("file_path", "")
        
        if not file_path:
            return {
                "status": "error",
                "message": "No file path specified in task"
            }
        
        # Try to extract code from markdown code blocks
        code_content = self._extract_code_from_markdown(response_content)
        
        if code_content:
            result = self.file_tools.create_file(file_path, code_content)
            
            if result["status"] == "success":
                self.logger.info(f"Created file using fallback method: {file_path}")
                return {
                    "status": "success",
                    "files_created": [file_path],
                    "message": f"File created: {file_path}"
                }
        
        return {
            "status": "error",
            "message": "Failed to create file - no code found in response"
        }
    
    def _extract_code_from_markdown(self, text: str) -> str:
        """Extract code from markdown code blocks"""
        
        # Look for code blocks
        if "```" in text:
            parts = text.split("```")
            
            # Get the largest code block
            code_blocks = []
            for i in range(1, len(parts), 2):
                block = parts[i]
                # Remove language identifier (e.g., ```html -> html)
                if "\n" in block:
                    block = block.split("\n", 1)[1]
                code_blocks.append(block.strip())
            
            if code_blocks:
                # Return the longest code block
                return max(code_blocks, key=len)
        
        return ""
