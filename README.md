# Twpm

A simple workflow builder that takes the complexity out of building dynamic workflows.

## Motivation

Twpm (twelve pm) is a simple workflow engine inspired by n8n, but now using all the benefits that Python offers. Build workflows where you control everything, and they can grow organically.

The project was born from building several WhatsApp automation workflows. Each solution was unique, highly coupled, and had significant code duplication. Twpm solves this by providing a framework to create workflows that are fast to build, scalable, and highly decoupled.

## Quick Start

Get started with Twpm in just a few lines of code:

```python
import asyncio
from twpm.core import Chain, Orchestrator
from twpm.core.container import Container, ServiceScope
from twpm.core.primitives import DisplayMessageNode, QuestionNode, SummaryNode
from twpm.core.depedencies import Output

workflow = (
    Chain()
    .add(DisplayMessageNode("Welcome!", key="welcome"))
    .add(QuestionNode("What's your name?", key="name"))
    .add(QuestionNode("What's your email?", key="email"))
    .add(SummaryNode(
        title="Thank you!",
        fields=[("Name", "name"), ("Email", "email")],
        key="summary"
    ))
    .build()
)

class ConsoleOutput:
    async def send_text(self, text: str):
        print(text, end=" ")

async def main():
    container = Container()
    container.registry(Output, lambda: ConsoleOutput(), ServiceScope.SINGLETON)
    orchestrator = Orchestrator(container)
    
    orchestrator.start(workflow)
    await orchestrator.process()

asyncio.run(main())
```

That's it! Twpm handles the rest!

## Installation

### Using uv

```sh
uv add twpm
```

### Using pip

```sh
pip install twpm
```

## Features

- **Simple API**: Build workflows using an intuitive builder pattern or simple function calls
- **Async Support**: Built on Python's asyncio for efficient async workflows
- **Dependency Injection**: Lightweight IoC container for clean dependency management
- **Built-in Primitives**: Ready-to-use nodes for common patterns:
  - `DisplayMessageNode`: Display messages to users
  - `QuestionNode`: Prompt for user input
  - `PoolNode`: Multiple choice questions
  - `QuizNode`: Quiz questions with correct answers
  - `ConditionalNode`: Dynamic branching based on conditions
  - `ProgressNode`: Show progress through workflow steps
  - `SummaryNode`: Display collected data summaries
  - `TaskNode`: Execute custom async tasks
- **Type Safety**: Full type hints for better IDE support and error detection
- **Extensible**: Easy to create custom nodes for your specific needs

## Examples

Check out the [examples directory](examples/):

- **CLI Example** (`examples/cli/main.py`): A complete interactive CLI workflow demonstrating:
  - User input collection
  - Progress tracking
  - Data summarization
  - Quiz workflow with conditional routing based on results

Run the example:

```sh
git clone https://github.com/jacksonvieiracs/twpm
cd twpm
```

```sh
uv run python3 examples/cli/main.py
```

Try the quiz workflow:

```sh
uv run python3 examples/cli/main.py --quiz
```

## Architecture

### Fundamentals

![Base](docs/linked-list.png)

Approximately 40% of the codebase is a doubly-linked list implementation. Why use a linked list specifically? It guarantees a level of decoupling between components. Each node can define how the next node is processed, with the orchestrator intervening only when necessary. A node a stateful unit that stores state and contains the full logic. The magic happens when combining linked list fundamentals with an orchestrator that manages routing logic to advance, stop, or await.

![Conditional example](docs/conditional-example.png)

This example demonstrates the benefits of using a linked list data structure for controlling flow behavior. You can create a "condition node" that acts as a router to the next node in your flow based on a computed dynamic condition for example, based on the previous node's result.

### Components

![Base components](docs/core-components.png)

#### Node

A Node is a stateful unit of execution. Each node can define guards, execute custom logic, and dynamically choose the next node. Nodes form a double-linked structure (`prev`/`next`) enabling flexible routing based on runtime conditions.

#### Chain

A Chain is a double-linked list of nodes. It simplifies constructing pipelines by automatically connecting nodes and providing structural operations.

#### Orchestrator

The Orchestrator coordinates node execution. It decides which node should run next and whether to continue, await input, or stop, based on node results.

#### Cursor

The Cursor performs operations on the chain knowing only the "current node." It safely manages list mutations (insertion, replacement, deletion) without breaking the chain.

#### Container

The Container is a lightweight IoC system for injecting dependencies into nodes. It registers services, resolves them when needed, and manages lifecycles, without adding business logic.

## License

MIT
