# OpenAI Agents SDK Setup and Usage

This document summarizes the OpenAI Agents SDK, a lightweight framework for building multi-agent workflows, based on information from its [GitHub repository](https://github.com/openai/openai-agents-python/tree/main).

## Core Concepts

The OpenAI Agents SDK revolves around these key concepts:

1.  **Agents:**  These are the fundamental building blocks, representing LLMs configured with specific instructions, tools, guardrails, and handoff capabilities.
2.  **Handoffs:** A mechanism for transferring control between agents, enabling complex multi-agent workflows. It's implemented as a specialized tool call.
3.  **Guardrails:** Configurable safety checks to validate both input to and output from agents, ensuring responsible and reliable behavior.
4.  **Tracing:** Built-in tracking of agent runs, providing insights for debugging, monitoring, and optimizing agent workflows.

## Getting Started

### 1. Setting up your Python Environment

First, create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate
```

### 2. Installing the Agents SDK

Install the SDK using pip:

```bash
pip install openai-agents
```

For voice support, include the `voice` extra:

```bash
pip install 'openai-agents[voice]'
```

## Basic Usage: Hello World Example

Here's a simple "Hello World" example to get started:

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

This code defines an `Agent` with instructions and then uses `Runner.run_sync` to execute it with a given input.

## Handoffs Example

Handoffs allow you to create workflows where agents can transfer tasks to each other. Here's an example with language-based routing:

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)


async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

In this example, `triage_agent` decides whether to handoff to `spanish_agent` or `english_agent` based on the input language.

## Functions/Tools Example

Agents can be equipped with tools (functions) to perform specific actions:

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Here, the `agent` is given the `get_weather` tool, allowing it to respond to weather-related queries.

## Agent Loop and Final Output

The `Runner.run()` method executes an agent loop:

1.  The LLM is called with the agent's configuration and message history.
2.  The LLM responds, potentially with tool calls or a handoff.
3.  If a final output is reached, the loop ends and returns the output.
4.  If a handoff occurs, the agent is switched, and the loop continues with the new agent.
5.  Tool calls are processed, and their responses are fed back into the loop.

The loop continues until a "final output" is determined.  A final output is either:

*   A structured output matching the agent's `output_type` (if defined).
*   A plain text response without tool calls or handoffs (if no `output_type` is defined).

## Tracing

The Agents SDK includes built-in tracing to monitor agent behavior. This tracing is extensible and can be integrated with various external tracing processors.

## Development Setup (For SDK Edits)

If you need to modify the SDK itself:

1.  Ensure you have `uv` installed.
2.  Install dependencies using `make sync`.
3.  Run tests, type checking, and linting with `make tests`, `make mypy`, and `make lint`.

This document provides a starting point for understanding and using the OpenAI Agents SDK. For more in-depth information and advanced features, refer to the [official documentation](https://openai.github.io/openai-agents-python/) and explore the examples in the [GitHub repository](https://github.com/openai/openai-agents-python/tree/main/examples). 