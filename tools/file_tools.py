"""
File system tools for agents to interact with the local filesystem
"""
import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class FileTools:
    """Collection of file system operations for agents"""
    
    def __init__(self, base_dir: str = None):
        """
        Initialize FileTools
        
        Args:
            base_dir: Base directory for file operations (defaults to outputs/)
        """
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
    
    def create_file(self, path: str, content: str = "") -> Dict[str, Any]:
        """
        Create a new file with optional content
        
        Args:
            path: Relative path to the file
            content: Initial content for the file
            
        Returns:
            Dict with status and message
        """
        try:
            full_path = os.path.join(self.base_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "status": "success",
                "message": f"File created: {path}",
                "path": full_path
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create file: {str(e)}"
            }
    
    def write_to_file(self, path: str, content: str, mode: str = 'w') -> Dict[str, Any]:
        """
        Write content to a file
        
        Args:
            path: Relative path to the file
            content: Content to write
            mode: Write mode ('w' for overwrite, 'a' for append)
            
        Returns:
            Dict with status and message
        """
        try:
            full_path = os.path.join(self.base_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            return {
                "status": "success",
                "message": f"Content written to: {path}",
                "path": full_path
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to write to file: {str(e)}"
            }
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read content from a file
        
        Args:
            path: Relative path to the file
            
        Returns:
            Dict with status, message, and content
        """
        try:
            full_path = os.path.join(self.base_dir, path)
            
            if not os.path.exists(full_path):
                return {
                    "status": "error",
                    "message": f"File not found: {path}",
                    "content": None
                }
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "status": "success",
                "message": f"File read: {path}",
                "content": content
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to read file: {str(e)}",
                "content": None
            }
    
    def list_directory(self, path: str = "") -> Dict[str, Any]:
        """
        List contents of a directory
        
        Args:
            path: Relative path to the directory (empty for base_dir)
            
        Returns:
            Dict with status, message, and list of files/directories
        """
        try:
            full_path = os.path.join(self.base_dir, path)
            
            if not os.path.exists(full_path):
                return {
                    "status": "error",
                    "message": f"Directory not found: {path}",
                    "contents": []
                }
            
            contents = []
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                contents.append({
                    "name": item,
                    "type": "directory" if os.path.isdir(item_path) else "file",
                    "path": os.path.join(path, item)
                })
            
            return {
                "status": "success",
                "message": f"Directory listed: {path or 'root'}",
                "contents": contents
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to list directory: {str(e)}",
                "contents": []
            }
    
    def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Delete a file
        
        Args:
            path: Relative path to the file
            
        Returns:
            Dict with status and message
        """
        try:
            full_path = os.path.join(self.base_dir, path)
            
            if not os.path.exists(full_path):
                return {
                    "status": "error",
                    "message": f"File not found: {path}"
                }
            
            os.remove(full_path)
            
            return {
                "status": "success",
                "message": f"File deleted: {path}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete file: {str(e)}"
            }
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions in OpenAI function calling format
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_file",
                    "description": "Create a new file with optional content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to the file (e.g., 'index.html', 'css/style.css')"
                            },
                            "content": {
                                "type": "string",
                                "description": "Initial content for the file"
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_to_file",
                    "description": "Write or append content to an existing file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to the file"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write to the file"
                            },
                            "mode": {
                                "type": "string",
                                "enum": ["w", "a"],
                                "description": "Write mode: 'w' for overwrite, 'a' for append"
                            }
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read content from a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to the file"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List contents of a directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to the directory (empty for root)"
                            }
                        }
                    }
                }
            }
        ]
