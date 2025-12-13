"""
Main entry point for the Multi-Agent Code Generation System
"""
import os
import sys
import argparse
import logging
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator.multi_agent_orchestrator import MultiAgentOrchestrator
from tools.llm_client import LLMClient, MockLLMClient
from tools.enhanced_mock_client import EnhancedMockLLMClient
from prompts.system_prompts import ARXIV_PROJECT_REQUIREMENT


def setup_logging(log_dir: str = "logs"):
    """Setup logging configuration"""
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"agent_system_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return log_file


def main():
    """Main execution function"""
    
    parser = argparse.ArgumentParser(description="Multi-Agent Code Generation System")
    parser.add_argument(
        "--requirement",
        type=str,
        default=None,
        help="Project requirement (defaults to arXiv project)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Output directory for generated code"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="deepseek",
        choices=["deepseek", "openai", "anthropic", "mock"],
        help="LLM provider to use"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Specific model name (optional)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API key for the LLM provider"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=20,
        help="Maximum task execution iterations"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock LLM client (for testing without API)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("="*80)
    logger.info("MULTI-AGENT CODE GENERATION SYSTEM")
    logger.info("="*80)
    logger.info(f"Log file: {log_file}")
    
    # Get requirement
    requirement = args.requirement or ARXIV_PROJECT_REQUIREMENT
    
    logger.info(f"\nProject Requirement:")
    logger.info("-"*80)
    logger.info(requirement[:200] + "..." if len(requirement) > 200 else requirement)
    logger.info("-"*80)
    
    # Initialize LLM client
    if args.mock or args.provider == "mock":
        logger.info("\nUsing Enhanced Mock LLM Client (generates realistic code)")
        llm_client = EnhancedMockLLMClient()
    else:
        logger.info(f"\nInitializing LLM Client: {args.provider}")
        
        api_key = args.api_key
        if not api_key:
            # Try to get from environment
            env_var = f"{args.provider.upper()}_API_KEY"
            api_key = os.getenv(env_var)
            
            if not api_key:
                logger.warning(f"No API key provided. Set {env_var} environment variable or use --api-key")
                logger.info("Falling back to enhanced mock client...")
                llm_client = EnhancedMockLLMClient()
            else:
                llm_client = LLMClient(
                    provider=args.provider,
                    model=args.model,
                    api_key=api_key
                )
        else:
            llm_client = LLMClient(
                provider=args.provider,
                model=args.model,
                api_key=api_key
            )
    
    # Create output directory
    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Output directory: {output_dir}")
    
    # Initialize orchestrator
    logger.info("\nInitializing Multi-Agent Orchestrator...")
    orchestrator = MultiAgentOrchestrator(
        llm_client=llm_client,
        output_dir=output_dir
    )
    
    # Run the system
    logger.info("\nStarting execution...\n")
    
    try:
        result = orchestrator.run(requirement, max_iterations=args.max_iterations)
        
        # Print summary
        print("\n" + orchestrator.get_project_summary())
        
        if result["status"] == "success":
            print(f"\n✓ Project completed successfully!")
            print(f"✓ Generated {len(result['created_files'])} files")
            print(f"✓ Check output at: {result['output_dir']}")
            
            if result.get("evaluation"):
                eval_data = result["evaluation"]
                print(f"\nEvaluation Score: {eval_data.get('overall_score', 'N/A')}/100")
                print(f"Status: {'PASSED ✓' if eval_data.get('passed') else 'NEEDS IMPROVEMENT'}")
            
            return 0
        else:
            print(f"\n✗ Project failed: {result.get('message', 'Unknown error')}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("\n\nExecution interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"\n\nExecution failed with error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
