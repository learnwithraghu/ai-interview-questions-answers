# Question 25: Multi-Agent Workflow State and Routing

**Question:** You need to build a complex, multi-agent workflow where a "researcher" agent gathers data and a "writer" agent drafts a report. How do you manage state, memory, and routing using frameworks like LangGraph or AutoGen?

**Answer:**

### 1. Question Explanation
This question is designed to see if you can architect a multi-agent system rather than a simple single-agent chatbot. Interviewers want to know whether you understand how to separate concerns, maintain state across agents, and route tasks so each agent can focus on one responsibility. A strong answer shows a clear mental model of agents, memory, and orchestration.

### 2. Concept Explanation
In a multi-agent workflow, each agent is responsible for a distinct role. The **researcher** is responsible for retrieving facts, summarizing sources, and assembling evidence. The **writer** is responsible for taking that evidence and producing a coherent final deliverable. The challenge is to keep state consistent and avoid repeated work.

The architecture usually includes:
* **State management:** Use a shared state store or memory object where agents write and read structured results. This is the single source of truth for the output of each step.
* **Memory:** Store intermediate artifacts like search results, extracted quotes, and outlines. This can be short-lived session memory or persistent memory if the workflow needs to be resumed later.
* **Routing:** Implement a controller that decides which agent runs next. The controller can be explicit code or a higher-level workflow engine. It should also manage fallbacks, retries, and branching logic.

Frameworks like **LangGraph** or **AutoGen** provide abstractions for agent nodes and message passing. They let you define a graph where the researcher node produces research summaries and the writer node consumes those summaries. They also help with serialization, agent prompts, and execution flow so you don't have to manage every state transfer manually.

### 3. Real-World Example
A consulting firm could build a report generation pipeline where the researcher agent queries a document store, scrapes public filings, and builds a bullet-point evidence deck. Then the writer agent uses that deck to write the executive summary. The workflow engine keeps the evidence in a shared memory object so the writer always has the latest, verified facts.

### 4. How Other Frameworks Handle Multi-Agent State and Routing

**LangGraph**
LangGraph (from LangChain) models a multi-agent workflow as a directed graph where nodes are agents or functions and edges are transitions between them. State is a typed Python object (`TypedDict`) that flows through the graph — each node reads from and writes to it. This makes state management explicit and inspectable. Conditional edges let you implement branching logic (e.g., “if the researcher found no results, route back to query reformulation”). LangGraph also supports cycles — the same agent can run multiple times in a loop until a condition is met. Natively integrates with LangSmith for tracing. Best for teams that want fine-grained control over routing and can tolerate LangChain’s abstraction overhead.

**Microsoft AutoGen**
AutoGen frames multi-agent workflows as a conversation between agents. Each agent has a system prompt defining its role and can send messages to other agents or a group chat. The `GroupChatManager` orchestrates turn-taking and routing in a conversation-style loop. State is passed implicitly through the message history — agents share context via what was said, not a structured state object. This is more flexible and natural-language-friendly but harder to debug and less predictable than a graph model. AutoGen 0.4 introduced a major redesign with `AgentChat` and explicit message passing, improving testability.

**CrewAI**
CrewAI uses a “crew + task” metaphor. You define agents with roles (researcher, writer, editor), assign tasks to them, and a `Crew` object orchestrates execution. Tasks can be sequential or parallel. CrewAI handles the orchestration loop, passing each task’s output as context to the next. Much simpler API than LangGraph for linear workflows, but less flexible for complex conditional branching. Popular for getting a multi-agent prototype running quickly.

**Anthropic’s Agent Pattern (Claude-native)**
Anthropic’s own guidance recommends keeping multi-agent systems as simple as possible: prefer direct API calls with explicit tool use over heavy frameworks. For researcher/writer workflows, their recommended pattern is a lightweight orchestrator (a Python function, not a framework) that calls Claude with different system prompts for each role and passes structured outputs between them using tool use / structured JSON. No framework dependency — just the Anthropic SDK and Python dataclasses. The advantage: maximum transparency and debuggability. The trade-off: you write more boilerplate.

**Temporal (workflow orchestration)**
For long-running, durable multi-agent workflows — tasks that might run for minutes or hours, need to survive process restarts, or require human approval mid-flow — teams are increasingly using Temporal alongside their LLM framework. Temporal handles workflow state persistence, retries, and timeouts at the infrastructure level. Each agent step becomes a Temporal “activity.” This is overkill for simple pipelines but essential for enterprise workflows where reliability guarantees matter.

| Framework | State Model | Routing Style | Complexity | Best For |
|---|---|---|---|---|
| LangGraph | Typed graph state object | Explicit conditional edges | Medium | Complex branching, cycles |
| AutoGen | Message history (conversation) | Turn-based group chat | Medium | Conversational agent teams |
| CrewAI | Task output chaining | Sequential / parallel tasks | Low | Quick linear prototypes |
| Anthropic SDK (direct) | Custom Python objects | Explicit orchestrator code | Low–Medium | Transparent, debuggable workflows |
| Temporal + LLM | Durable workflow state | Workflow engine | High | Long-running, resumable pipelines |

The selection heuristic: for a two-agent researcher/writer pipeline, start with CrewAI or direct SDK calls. Migrate to LangGraph when you need conditional branching or cycles. Add Temporal only when workflows need to be durable across hours or days.

### 5. This is how I would answer this
“I would separate the flow into a researcher agent that gathers and structures evidence, and a writer agent that consumes that evidence to draft the report. I’d use a workflow engine or graph framework to keep shared state in a central memory object and route the next step explicitly, so each agent stays focused and we can trace the full end-to-end process.”