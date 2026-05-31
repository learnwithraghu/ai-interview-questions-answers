# Question 28: Tool vs Harness

**Question:** In the context of building and testing AI agents, what is the difference between a "tool" and a "harness"?

**Answer:**

### 1. Question Explanation
Alright, when an interviewer asks you this, what they are really looking for is to see if you understand the architecture of AI agent systems beyond just using high-level orchestration frameworks. They want to check if you distinguish between the model's reasoning/intent and the actual system runtime that executes those intents. The red flag they are watching out for is hand-waving about how "agents run functions" without understanding that the LLM only outputs structured text, and that a separate, secure execution environment must do the heavy lifting of running, sandboxing, and returning the result. They might also be checking if you understand the difference in testing environments—specifically, a single evaluation task versus a full benchmark evaluation harness.

### 2. Concept Explanation
Let's break this down from first principles. When we talk about "tool" and "harness," we are looking at two different levels of abstraction in the AI engineering stack. 

In **agent execution runtimes**, a **tool** is a specific utility or function exposed to the LLM (like `search_web`, `run_sql_query`, or `write_file`). Think of it as a leaf-node capability. The LLM only knows about the tool because we describe it in its system prompt or pass its schema to the API. Crucially, the LLM itself *cannot* execute code or hit API endpoints. It simply outputs structured text (like JSON) specifying the tool it wants to use and the arguments it wants to pass.

The **harness** (often called the *execution harness* or *agent harness*) is the surrounding infrastructure and control loop that runs the agent. It is the active runner. When the LLM outputs a tool-calling request, the harness catches the request, validates the arguments, enforces security boundaries (like running in a gRPC sandbox or Docker container), executes the tool function on the host machine, catches any runtime exceptions or timeouts, and formats the output back to the LLM as a new message. The tool is passive; the harness is the active orchestrator.

In **evaluation frameworks**, we see a similar split. An **evaluation tool** is a specific script or LLM-as-a-judge prompt that tests one single capability (like checking if a generated SQL query is valid). An **evaluation harness** (like EleutherAI's `lm-eval-harness`) is the entire testing rig. It loads the models, handles batching, injects the datasets, runs the individual evaluation scripts, logs the outputs, catches failures, and calculates aggregated metrics.

A great mental model is to think of a **tool** as a wrench, and the **harness** as the engine stand and safety enclosure. The wrench performs a specific operation on a bolt, but it requires the engine stand to hold the engine stable and the safety cage to protect the workshop while the test runs.

### 3. Real-World Example
Suppose you are building a coding agent like Claude Code. 
*   **The Tools:** The agent has access to tools like `view_file` and `run_command`. These tools are simple Python/Go functions that take arguments (like a file path or terminal command) and return strings.
*   **The Harness:** The command-line interface and daemon running on your computer. When the LLM decides to call `run_command` with `"npm run test"`, the harness intercepts this call. It prompts you for permission (creating a human-in-the-loop gate), spawns a sub-shell, sets a execution timeout of 10 seconds, collects stdout/stderr, and sends that text block back into the chat history. If the command crashes, the harness catches the error and reports it to the LLM, preventing the entire agent process from crashing.

### 4. This is how I would answer this
"In my experience, the difference comes down to capability versus container. A tool is a specific function or API we expose to the LLM—like a database reader or a web scraper—so it can choose to interact with the outside world. The model doesn't execute the tool; it just returns the JSON describing its intent to call it. 

The harness is the surrounding execution infrastructure that actually runs the code. It intercepts the model's tool calls, enforces sandboxing, manages timeouts, handles permissions, and catches errors before feeding the result back to the model as an observation. In testing, the same concept applies: an evaluation tool measures one specific task, while an evaluation harness is the full test runner that orchestrates models, datasets, and metrics at scale."
