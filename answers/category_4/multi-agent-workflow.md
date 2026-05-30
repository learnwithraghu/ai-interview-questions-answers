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

### 4. This is how I would answer this
“I would separate the flow into a researcher agent that gathers and structures evidence, and a writer agent that consumes that evidence to draft the report. I’d use a workflow engine or graph framework to keep shared state in a central memory object and route the next step explicitly, so each agent stays focused and we can trace the full end-to-end process.”