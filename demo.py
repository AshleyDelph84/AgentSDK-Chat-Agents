import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, WebSearchTool

# Load environment variables from .env file (if present)
load_dotenv()

# Set up OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in a .env file or export it.")

# Import the agents from the multi_agent_app.py file
from multi_agent_app import triage_agent, french_agent, web_search_agent

# Define some test queries for demonstration
TEST_QUERIES = [
    "Translate 'Hello, how are you today?' to French",
    "What are the latest developments in AI technology?",
    "What is the capital city of France?",
    "How do you say 'I love artificial intelligence' in French?",
    "Who is the current CEO of OpenAI?"
]

async def run_demo():
    print("=" * 50)
    print("Multi-Agent System Demo")
    print("=" * 50)
    print("This demo will run through a series of predefined test queries to demonstrate")
    print("how the various agents work together to handle different types of requests.")
    print("=" * 50)
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\nTest Query #{i}: {query}")
        print("-" * 50)
        
        print("Processing...")
        try:
            result = await Runner.run(triage_agent, input=query)
            print("\nAgent Response:")
            print(result.final_output)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        print("=" * 50)
        
        # Add a small delay between queries for better readability
        if i < len(TEST_QUERIES):
            print("Next query in 3 seconds...")
            await asyncio.sleep(3)
    
    print("\nDemo completed. All test queries have been processed.")

if __name__ == "__main__":
    asyncio.run(run_demo()) 