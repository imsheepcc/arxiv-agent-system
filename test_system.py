#!/usr/bin/env python3
"""
Test script for Multi-Agent Code Generation System
Validates that all components are working correctly
"""
import os
import sys
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from agents.base_agent import BaseAgent, PlanningAgent
        from agents.code_agent import CodeGenerationAgent
        from agents.evaluation_agent import EvaluationAgent
        from orchestrator.multi_agent_orchestrator import MultiAgentOrchestrator
        from tools.file_tools import FileTools
        from tools.llm_client import LLMClient, MockLLMClient
        from tools.enhanced_mock_client import EnhancedMockLLMClient
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_file_tools():
    """Test file tools functionality"""
    print("\nTesting file tools...")
    try:
        from tools.file_tools import FileTools
        
        # Create temporary test directory
        tools = FileTools(base_dir="test_output")
        
        # Test create file
        result = tools.create_file("test.txt", "Hello World")
        assert result["status"] == "success", "File creation failed"
        
        # Test read file
        result = tools.read_file("test.txt")
        assert result["status"] == "success", "File reading failed"
        assert result["content"] == "Hello World", "File content incorrect"
        
        # Test list directory
        result = tools.list_directory("")
        assert result["status"] == "success", "Directory listing failed"
        
        # Cleanup
        import shutil
        shutil.rmtree("test_output")
        
        print("✓ File tools working correctly")
        return True
    except Exception as e:
        print(f"✗ File tools test failed: {e}")
        return False

def test_mock_client():
    """Test enhanced mock client"""
    print("\nTesting mock client...")
    try:
        from tools.enhanced_mock_client import EnhancedMockLLMClient
        
        client = EnhancedMockLLMClient()
        
        # Test planning response
        response = client.chat([
            {"role": "user", "content": "create a project plan"}
        ])
        assert "content" in response, "Response missing content"
        
        print("✓ Mock client working correctly")
        return True
    except Exception as e:
        print(f"✗ Mock client test failed: {e}")
        return False

def test_agents():
    """Test agent initialization"""
    print("\nTesting agents...")
    try:
        from agents.base_agent import PlanningAgent
        from agents.code_agent import CodeGenerationAgent
        from agents.evaluation_agent import EvaluationAgent
        from tools.enhanced_mock_client import EnhancedMockLLMClient
        from tools.file_tools import FileTools
        
        client = EnhancedMockLLMClient()
        tools = FileTools(base_dir="test_output")
        
        # Test planning agent
        planning_agent = PlanningAgent(client)
        assert planning_agent.role == "PlanningAgent"
        
        # Test code agent
        code_agent = CodeGenerationAgent(client, tools)
        assert code_agent.role == "CodeGenerationAgent"
        
        # Test evaluation agent
        eval_agent = EvaluationAgent(client, tools)
        assert eval_agent.role == "EvaluationAgent"
        
        # Cleanup
        import shutil
        if os.path.exists("test_output"):
            shutil.rmtree("test_output")
        
        print("✓ All agents initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Agent test failed: {e}")
        return False

def test_generated_files():
    """Test that website files were generated"""
    print("\nTesting generated website files...")
    
    required_files = [
        "outputs/index.html",
        "outputs/category.html",
        "outputs/paper.html",
        "outputs/css/style.css",
        "outputs/js/script.js",
        "outputs/data/papers.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    
    # Test that papers.json is valid JSON
    try:
        with open("outputs/data/papers.json", "r") as f:
            data = json.load(f)
            assert "papers" in data, "papers.json missing 'papers' key"
            assert "categories" in data, "papers.json missing 'categories' key"
            assert len(data["papers"]) > 0, "No papers in data"
    except Exception as e:
        print(f"✗ papers.json validation failed: {e}")
        return False
    
    print(f"✓ All {len(required_files)} files exist and valid")
    return True

def main():
    """Run all tests"""
    print("="*60)
    print("Multi-Agent System - Test Suite")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("File Tools", test_file_tools),
        ("Mock Client", test_mock_client),
        ("Agents", test_agents),
        ("Generated Files", test_generated_files)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! System is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
