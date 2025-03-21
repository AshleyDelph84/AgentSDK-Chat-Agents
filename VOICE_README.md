# Voice Agent System

This extension adds voice capabilities to the multi-agent system, allowing you to interact with agents through speech.

## Setup

1. **Install Required Dependencies**:
   ```
   python setup_voice_agents.py
   ```
   
   This will install all necessary dependencies, including:
   - OpenAI Agents SDK with voice support
   - NumPy for audio processing
   - SoundDevice for microphone input and speaker output

2. **Alternative Manual Setup**:
   If the setup script doesn't work, you can install dependencies manually:
   ```
   pip install -r requirements.txt
   pip install 'openai-agents[voice]>=0.0.6'
   ```

## Usage

To start the voice agent system:

```
python voice_multi_agent.py
```

**How it works**:
1. The system will start listening for 5 seconds when prompted
2. Speak your request clearly into your microphone
3. The system will process your speech, route it to the appropriate agent, and respond audibly

**Available Agents**:
- **Triage Agent**: Routes your request to the appropriate specialized agent
- **Web Search Agent**: Searches the web for information
- **French Translation Agent**: Handles French translations and language questions

## Features

- **Speech-to-Text**: Converts your spoken words into text that agents can process
- **Agent Processing**: Routes your request to the specialized agent best suited for the task
- **Text-to-Speech**: Converts the agent's response back into spoken words
- **Tracing**: Full tracing of the entire voice pipeline for debugging and monitoring

## Troubleshooting

- **No sound input/output**: Ensure your microphone and speakers are properly connected and set as default devices
- **Python errors**: Make sure all dependencies are properly installed
- **OpenAI API errors**: Check that your API key is valid and has sufficient credits

## Extending

You can extend the voice agent system in several ways:
- Add more specialized agents by creating new agents and adding them to the triage agent's handoff list
- Implement better audio input handling with voice activity detection
- Create a more sophisticated UI for the voice interaction

## References

This implementation is based on the [OpenAI Agents SDK Voice Quickstart](https://openai.github.io/openai-agents-python/voice/quickstart/). 