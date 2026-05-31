# Question 11: Tool Routing and Function Calling

**Question:** A stakeholder wants an LLM application that can search the web, query an internal database, and send an email. How do you design the tool-calling/function-calling architecture to route these intents reliably and safely?

**Answer:**

### 1. Question Explanation
Alright, this is a senior-level architecture question. The interviewer is not just asking if you know what function calling is—they want to see if you've thought about *safety* and *reliability* when an LLM has the power to take real-world actions like sending emails. A red flag is if you only talk about defining functions and ignore the risks. They want to hear about how you guard against the model calling the wrong tool, calling tools with bad arguments, or—worst of all—sending emails it shouldn't. Think about guardrails, confirmations, and schema validation on your tool inputs.

### 2. Concept Explanation
Function calling (also called tool use) is the mechanism that transforms an LLM from a text generator into an *agent that can interact with the real world*. Understanding how it works under the hood will help you build it reliably.

**How it works mechanically:** You define a set of tools in JSON schema format—each tool has a name, a description, and a parameters schema. You pass these tool definitions to the LLM alongside the user's message. The LLM doesn't execute the tools—it simply *decides* which tool to call and what arguments to pass, and returns that decision as a structured JSON object. Your application code reads that decision and actually executes the function. Then you pass the result back to the LLM so it can continue reasoning.

This means the LLM is the *router*, not the *executor*. You are always in control of what actually runs.

**Why this matters for safety:** The moment you give an LLM the ability to trigger a "send_email" or "make_payment" function, you have a system that can cause irreversible real-world effects based on a language model's output. This is not something you want to run on autopilot.

The key design decision is classifying your tools into two categories:
- **Read-only / reversible actions** (web search, database read, weather lookup): Safe to execute automatically. The worst that happens is a wasted API call.
- **Write / irreversible actions** (send email, post to social media, make payment, delete record): These must have a **Human-in-the-Loop (HITL)** gate. Pause execution, show the user exactly what the agent is about to do, and require explicit confirmation before anything runs.

**Argument validation:** Before executing any tool call, validate the arguments the LLM returned against your tool's parameter schema. LLMs occasionally hallucinate argument names or pass the wrong types. A quick validation step catches this before it becomes a runtime error or a security issue.

**Loop prevention:** Agents using tools can enter infinite loops if a tool call fails and the model keeps retrying. Always set a maximum number of tool call iterations (e.g., 10 steps) and fail gracefully if the limit is hit.

### 3. Real-World Example
A sales team AI assistant can search the web for competitor pricing, query an internal CRM database for customer history, and send follow-up emails. The architecture registers three tools. For web search and DB queries, the tool calls execute automatically. But for the "send_email" tool, a confirmation modal is shown to the sales rep before anything is dispatched. All calls are logged to an audit trail for compliance.

### 4. This is how I would answer this
"I'd define each capability as a function with a strict JSON schema and register them with the LLM's tool-calling API. For routing, the model decides which tool to call based on the user's intent—I don't need to hardcode any routing logic. But the key design decision is around safety: for read-only actions like web search or database queries, I'd execute them automatically. For anything irreversible like sending an email, I'd always insert a human-in-the-loop confirmation step. I'd also validate all tool arguments against the schema before execution and log every tool call for auditability."
