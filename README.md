# Multi-Agent System using OpenAI Agents SDK

This project demonstrates a multi-agent system built with the OpenAI Agents SDK. The system consists of three specialized agents working together to handle different types of user requests.

## Agents

1. **Triage Agent**: Routes user requests to the appropriate specialized agent based on the content of the request.
2. **Web Search Agent**: Searches the web for factual information and current events.
3. **French Translation Agent**: Handles French language translation tasks and answers questions about French language or culture.

## Features

- Automated routing of requests to the most appropriate agent
- Web search capabilities using built-in functions
- French translation functionality
- Interactive command-line interface for testing
- Easy extensibility for adding more specialized agents

## Requirements

- Python 3.9+
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   
   Option 1: Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   
   Option 2: Export the API key as an environment variable:
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Running the basic agent script

To run the basic agent script with a single query:

```
python multi_agent_app.py
```

### Running the interactive version

For an interactive session where you can ask multiple questions:

```
python interactive_multi_agent.py
```

## Example Queries

- **For the Web Search Agent**: "What is the latest news about artificial intelligence?"
- **For the French Translation Agent**: "Translate 'Hello, how are you doing today?' to French"
- **For General Information**: "Who developed the OpenAI Agents SDK?"

## Project Structure

- `multi_agent_app.py`: Main script with a single query functionality
- `interactive_multi_agent.py`: Interactive version allowing multiple queries
- `requirements.txt`: List of dependencies
- `README.md`: This documentation file

## Extending the System

To add a new specialized agent:

1. Create a new agent with specific instructions and tools
2. Add the new agent to the triage agent's handoffs list
3. Update the triage agent's instructions to include information about the new agent

## Resources

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
