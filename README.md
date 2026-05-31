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
* **Lecture 11:** Designing Safe LLM Tool Calling
* **Lecture 12:** Advanced RAG Retrieval Strategy Options
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

To understand how tool calling operates under the hood, here is the step-by-step trace of the **4 JSON payloads** exchanged between your application and the LLM API when a user asks: *"What is the temperature in Dubai?"*

### Step 1: Initial Request (App → LLM)
Your application sends the user's prompt alongside the definitions of the tools it supports (written in JSON schema format).

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "What is the temperature in Dubai?"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "Get the current weather for a given location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. Dubai, UAE"
            }
          },
          "required": ["location"]
        }
      }
    }
  ]
}
```

### Step 2: Tool Call Decision (LLM → App)
The LLM identifies that the request requires the `get_current_weather` tool, parses the parameter `"Dubai"`, and returns a request for the application to run the tool. The model **stops generating text** at this point.

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_12345xyz",
            "type": "function",
            "function": {
              "name": "get_current_weather",
              "arguments": "{\"location\": \"Dubai\"}"
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
Your application extracts the arguments, executes the local code (e.g., calling a weather API), receives the result, and feeds the **entire conversation history** plus the new tool output back to the LLM.

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "What is the temperature in Dubai?"
    },
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_12345xyz",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\"location\": \"Dubai\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_12345xyz",
      "content": "{\"temp\": \"42°C\", \"condition\": \"Sunny\"}"
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
        "content": "The current temperature in Dubai is 42°C and it is Sunny."
      },
      "finish_reason": "stop"
    }
  ]
}
```