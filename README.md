# AI Engineer Interview Bootcamp: Concepts to Production

Welcome to the course repository! This course is designed to take you through the most critical interview questions and scenarios you will face when interviewing for a Generative AI Engineer or LLM Application Developer role. 

Below is the curriculum structure, including the engaging lecture titles that correspond to the interview questions.

---

## 📚 Course Curriculum

### Section 1: Core GenAI Concepts & Foundations
*Building a strong fundamental understanding of how LLMs and AI systems work under the hood.*

* **Lecture 1:** System User and Assistant Prompts
* **Lecture 2:** Few Shot Versus Zero Shot
* **Lecture 3:** Input Tokens Versus Output Tokens
* **Lecture 4:** Purpose Of AGENTS.md In Repos
* **Lecture 5:** What Is the ReAct Framework
* **Lecture 6:** Hallucinations In AI Coding Workflows

### Section 2: Real-World Scenario Architecture
*Tackling practical, system-design challenges commonly seen in enterprise AI applications.*

* **Lecture 7:** Extracting Valid JSON From Emails
* **Lecture 8:** RAG Systems Fail Independently
* **Lecture 9:** Claude Code Compact Feature
* **Lecture 10:** Natural Language To SQL Reliably
* **Lecture 11:** Tool Calling Flow Under Hood
* **Lecture 12:** Critical Path In AI Pipelines
* **Lecture 13:** Automated LLM Evaluation At Scale

### Section 3: Production Incidents & Reliability
*Learning how to handle failures, security threats, and scaling issues when your AI goes live.*

* **Lecture 14:** Stopping Prompt Injection Attack Immediately
* **Lecture 15:** Managing LLM Context Window Limits
* **Lecture 16:** API Rate Limit Fallback Strategies
* **Lecture 17:** Securing AI Agent Function Calling
* **Lecture 18:** Filtering Hallucinated Citations In Production
* **Lecture 19:** Graceful Degradation When Retrieval Fails

### Section 4: Modern AI Stack & Tooling
*Navigating the rapidly evolving ecosystem of frameworks, databases, and deployment platforms.*

* **Lecture 20:** Managed API Versus Open Weight
* **Lecture 21:** When To Skip LangChain Frameworks
* **Lecture 22:** Dedicated Vector DB Versus pgvector
* **Lecture 23:** LLM Observability Tools And Metrics
* **Lecture 24:** Function Calling With External REST
* **Lecture 25:** Multi Agent Workflow State Management
* **Lecture 26:** Exact Match Versus Semantic Caching
* **Lecture 27:** Browser Edge Or Server Inference
* **Lecture 28:** Tool Versus Execution Harness

---

## 🛠️ Tool Calling (Function Calling) JSON Flow Example

To understand how tool calling operates under the hood, here is the step-by-step trace of the **4 JSON payloads** exchanged between your application and the LLM API when a user asks: *"Who is our top spending customer?"*

### Step 1: Initial Request (App → LLM)
Your application sends the user's prompt alongside the definitions of the tools it supports (written in JSON schema format).

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "Who is our top spending customer?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "run_sql_query",
        "description": "Run a read-only SQL query against the user database",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "The SQL query to execute"
            }
          },
          "required": ["query"]
        }
      }
    }
  ]
}
```

### Step 2: Tool Call Decision (LLM → App)
The LLM identifies that the request requires the `run_sql_query` tool, generates the appropriate SQL query arguments, and returns a request for the application to run the tool. The model **stops generating text** at this point.

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_98765abc",
            "type": "function",
            "function": {
              "name": "run_sql_query",
              "arguments": "{\"query\": \"SELECT name FROM users ORDER BY total_spend DESC LIMIT 1;\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

### Step 3: Tool Execution & Result Submission (App → LLM)
Your application extracts the SQL argument, executes the query against your database client, receives the result, and feeds the **entire conversation history** plus the new tool output back to the LLM.

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "Who is our top spending customer?"
    },
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_98765abc",
          "type": "function",
          "function": {
            "name": "run_sql_query",
            "arguments": "{\"query\": \"SELECT name FROM users ORDER BY total_spend DESC LIMIT 1;\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_98765abc",
      "content": "{\"result\": \"Jane Doe\"}"
    }
  ]
}
```

### Step 4: Final Response (LLM → App)
The LLM reads the complete history including the tool's result and produces a final, natural language answer for the user.

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Our top spending customer is Jane Doe."
      },
      "finish_reason": "stop"
    }
  ]
}
```