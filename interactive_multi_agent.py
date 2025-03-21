import os
import asyncio
import json
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, WebSearchTool

# Load environment variables from .env file (if present)
load_dotenv()

# Set up OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in a .env file or export it.")

# Web search function tool (for demo purposes)
@function_tool
def search_web(query: str) -> str:
    """
    Search the web for information on a query.
    This is a simplified implementation - in a production environment, 
    you would use a proper search API.
    """
    try:
        # Using DuckDuckGo's simple API for demonstration
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url)
        data = response.json()
        
        # Extract relevant information
        result = f"Search results for: {query}\n\n"
        
        # Add abstract if available
        if data.get("Abstract"):
            result += f"Abstract: {data['Abstract']}\n\n"
        
        # Add related topics
        if data.get("RelatedTopics"):
            result += "Related information:\n"
            for i, topic in enumerate(data["RelatedTopics"][:5], 1):  # Limit to first 5 topics
                if isinstance(topic, dict) and "Text" in topic:
                    result += f"{i}. {topic['Text']}\n"
        
        return result
    except Exception as e:
        return f"Error searching the web: {str(e)}"

# Translation function tool
@function_tool
def translate_to_french(text: str) -> str:
    """
    Translate the given text to French.
    This is implemented within the agent itself using its language capabilities.
    """
    return "This function will be used to indicate the French agent should translate this text."

# Create the specialized agents
french_agent = Agent(
    name="French Translation Agent",
    instructions=(
        "You are a specialized French translation agent. Your primary responsibility is to:\n"
        "1. Accurately translate text between English and French while preserving tone and meaning\n"
        "2. Answer questions about French language, grammar, or culture\n"
        "3. Help users understand French idioms and expressions\n"
        "4. Always respond in a helpful, accurate manner\n\n"
        "When translating, make sure to preserve the tone, formality level, and cultural nuances."
    )
)

web_search_agent = Agent(
    name="Web Search Agent",
    instructions=(
        "You are a specialized web search agent. Your primary responsibility is to:\n"
        "1. Find accurate, up-to-date information from the web based on user queries\n"
        "2. Summarize search results in a clear, concise manner\n"
        "3. Provide factual, objective information without bias\n"
        "4. Always cite your sources when providing information\n\n"
        "Make sure to conduct thorough searches and verify information when possible."
    ),
    tools=[search_web, WebSearchTool()]
)

# Create the triage agent to handle routing between agents
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a triage agent responsible for routing user requests to the appropriate specialized agent.\n\n"
        "You have access to the following agents:\n"
        "1. FRENCH TRANSLATION AGENT: For translating text to/from French or answering questions about French language and culture\n"
        "2. WEB SEARCH AGENT: For finding factual information and current events on the web\n\n"
        "Your job is to:\n"
        "1. Analyze the user's request\n"
        "2. Determine which specialized agent is best suited to handle it\n"
        "3. Hand off the request to the appropriate agent\n"
        "4. If the request doesn't clearly fit either agent, use your best judgment\n"
        "5. For general questions not requiring specialized knowledge, you may answer directly\n\n"
        "Always prioritize giving the user the best experience by routing to the most appropriate agent."
    ),
    handoffs=[french_agent, web_search_agent]
)

async def process_user_input(user_input):
    """Process a single user input and return the agent's response"""
    result = await Runner.run(triage_agent, input=user_input)
    return result.final_output

async def interactive_session():
    """Run an interactive session with the agent system"""
    print("=" * 50)
    print("Multi-Agent System Interactive Session")
    print("=" * 50)
    print("This system has three agents:")
    print("1. Triage Agent - Routes your request to the appropriate agent")
    print("2. Web Search Agent - Searches the web for information")
    print("3. French Translation Agent - Handles French translations and language questions")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 50)
    
    while True:
        user_input = input("\nWhat would you like help with? ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Thank you for using the Multi-Agent System. Goodbye!")
            break
            
        print("\nProcessing your request...")
        try:
            response = await process_user_input(user_input)
            print("\nAgent Response:")
            print(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(interactive_session()) 