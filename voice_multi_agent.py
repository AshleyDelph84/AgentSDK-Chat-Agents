import os
import asyncio
import json
import requests
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, WebSearchTool
from agents.voice import SingleAgentVoiceWorkflow, VoicePipeline, VoicePipelineConfig, AudioInput
from agents.tracing import trace

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
        "When translating, make sure to preserve the tone, formality level, and cultural nuances.\n\n"
        "Since you are communicating via voice, keep your responses concise and easy to understand when spoken."
    ),
    model="gpt-4o-mini"
)

web_search_agent = Agent(
    name="Web Search Agent",
    instructions=(
        "You are a specialized web search agent. Your primary responsibility is to:\n"
        "1. Find accurate, up-to-date information from the web based on user queries\n"
        "2. Summarize search results in a clear, concise manner\n"
        "3. Provide factual, objective information without bias\n"
        "4. Always cite your sources when providing information\n\n"
        "Make sure to conduct thorough searches and verify information when possible.\n\n"
        "Since you are communicating via voice, keep your responses concise and easy to understand when spoken."
    ),
    tools=[search_web, WebSearchTool()],
    model="gpt-4o-mini"
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
        "Always prioritize giving the user the best experience by routing to the most appropriate agent.\n\n"
        "Since you are communicating via voice, keep your responses concise and conversational. Introduce yourself when first speaking."
    ),
    handoffs=[french_agent, web_search_agent],
    model="gpt-4o-mini" # Using a more capable model for voice interactions
)

async def run_voice_session():
    """Run a voice session with the multi-agent system"""
    print("=" * 50)
    print("Voice Multi-Agent System")
    print("=" * 50)
    print("Setting up voice pipeline with three specialized agents:")
    print("1. Triage Agent - Routes your request to the appropriate agent")
    print("2. Web Search Agent - Searches the web for information")
    print("3. French Translation Agent - Handles French translations and language questions")
    print("Testing with 3 seconds of silence audio as input...")
    print("=" * 50)
    
    # Create a voice workflow using our triage agent
    workflow = SingleAgentVoiceWorkflow(triage_agent)
    
    # Configure the voice pipeline with tracing enabled
    config = VoicePipelineConfig(
        workflow_name="MultiAgentVoice",
        trace_include_sensitive_audio_data=True  # Set to False in production for privacy
    )
    
    # Create the voice pipeline
    pipeline = VoicePipeline(
        workflow=workflow,
        config=config
    )
    
    try:
        # For simplicity, create 3 seconds of silence as audio input
        # This matches the official example in the documentation
        samplerate = 24000  # Hz
        buffer = np.zeros(samplerate * 3, dtype=np.int16)
        audio_input = AudioInput(buffer=buffer)
        
        print("Processing audio input...")
        
        # Setup audio output stream
        player = sd.OutputStream(samplerate=samplerate, channels=1, dtype=np.int16)
        player.start()
        
        # Run the pipeline with the audio input
        result = await pipeline.run(audio_input)
        
        # Process and play the response
        print("Agent is responding...")
        async for event in result.stream():
            if event.type == "voice_stream_event_audio":
                # Play the audio response
                player.write(event.data)
            elif event.type == "voice_stream_event_lifecycle":
                # Print lifecycle event information
                print(f"Lifecycle event: {event}")
                # The correct attribute is 'event', not 'name' or 'event_name'
                if event.event == "turn_ended":
                    print("Agent finished speaking.")
                elif event.event == "turn_started":
                    print("Agent started speaking.")
                elif event.event == "session_ended":
                    print("Session ended.")
            elif event.type == "voice_stream_event_error":
                print(f"Error: {event.error}")
        
        player.stop()
        print("\nVoice interaction completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

async def interactive_voice_session():
    """Run an interactive voice session with continuous microphone input"""
    print("=" * 50)
    print("Interactive Voice Multi-Agent System")
    print("=" * 50)
    print("Setting up interactive voice pipeline with three specialized agents:")
    print("1. Triage Agent - Routes your request to the appropriate agent")
    print("2. Web Search Agent - Searches the web for information")
    print("3. French Translation Agent - Handles French translations and language questions")
    print("Speak into your microphone when prompted. Press Ctrl+C to exit.")
    print("=" * 50)
    
    # Create a voice workflow using our triage agent
    workflow = SingleAgentVoiceWorkflow(triage_agent)
    
    # Configure the voice pipeline with tracing enabled
    config = VoicePipelineConfig(
        workflow_name="InteractiveMultiAgentVoice",
        trace_include_sensitive_audio_data=True  # Set to False in production for privacy
    )
    
    # Create the voice pipeline
    pipeline = VoicePipeline(
        workflow=workflow,
        config=config
    )
    
    # Setup audio parameters
    samplerate = 24000  # Hz
    duration = 5  # seconds
    
    try:
        while True:
            print("\nListening (speak for 5 seconds)...")
            
            # Record audio from microphone
            audio_input_np = sd.rec(int(samplerate * duration), samplerate=samplerate, 
                                  channels=1, dtype=np.int16)
            sd.wait()  # Wait until recording is finished
            
            print("Processing your speech...")
            
            # Create audio input from numpy array
            audio_input = AudioInput(buffer=audio_input_np.flatten())
            
            # Setup audio output stream
            player = sd.OutputStream(samplerate=samplerate, channels=1, dtype=np.int16)
            player.start()
            
            # Run the pipeline with the audio input
            result = await pipeline.run(audio_input)
            
            # Process and play the response
            print("Agent is responding...")
            async for event in result.stream():
                if event.type == "voice_stream_event_audio":
                    # Play the audio response
                    player.write(event.data)
                elif event.type == "voice_stream_event_lifecycle":
                    # Print lifecycle event information
                    print(f"Lifecycle event: {event}")
                    # The correct attribute is 'event', not 'name' or 'event_name'
                    if event.event == "turn_ended":
                        print("Agent finished speaking.")
                    elif event.event == "turn_started":
                        print("Agent started speaking.")
                    elif event.event == "session_ended":
                        print("Session ended.")
                elif event.type == "voice_stream_event_error":
                    print(f"Error: {event.error}")
            
            player.stop()
            print("\nReady for next question. Press Ctrl+C to exit.")
            
    except KeyboardInterrupt:
        print("\nExiting voice agent session. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # First run the simple test with silence input
    print("Running voice test with silence input...")
    asyncio.run(run_voice_session())
    
    # Then run the interactive session
    print("\n\nStarting interactive voice session...")
    asyncio.run(interactive_voice_session()) 