# Question 11: Tool Calling Flow

**Question:** What does the tool call/function calling flow look like under the hood? Explain the sequence of steps and JSON payloads exchanged between the application and the LLM.

**Answer:**

### 1. Question Explanation
Alright, when an interviewer asks you this, they are digging past high-level wrapper libraries like LangChain or LlamaIndex. They want to check if you understand the actual wire protocol of function calling. A major red flag is if you believe the LLM directly executes code or calls APIs on its own. They want to hear you clearly explain that the LLM is stateless, that it only outputs text instructions (JSON), and that your application code is the active runner that executes the function and updates the chat history. They are checking for foundational engineering literacy.

### 2. Concept Explanation
Under the hood, function calling is a stateless, cooperative cycle between your application and the LLM. The LLM acts purely as a *reasoning engine* and a *router*, while your application handles the *execution*. 

Here is the exact 4-step sequence of events and JSON payloads that occur when a user asks: *"Who is our top spending customer?"*

#### Step 1: Request with Tool Declarations
Your application initiates the conversation. You pass the user's message along with a list of defined tools in JSON schema format. Each tool definition specifies its name, description, and parameter types so the model knows when and how to use it.

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

#### Step 2: Tool Call Decision
The LLM processes the user prompt, determines that it needs data from the database, chooses the `run_sql_query` tool, generates the SQL arguments, and returns a structured request. The model stops generating text here, and the API response sets `finish_reason` to `tool_calls`.

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

#### Step 3: Tool Execution & Result Submission
Your application code intercepts this JSON decision, validates the arguments against the schema, runs the SQL query against your actual database, and receives the result. 

Because LLM APIs are completely stateless, you must resend the **entire chat history**—the user message, the assistant's request to call the tool, and the new tool execution result (using the matching `tool_call_id`).

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

#### Step 4: Final Response Generation
The LLM reads the complete history including the tool's result, uses it to answer the original user query, and returns a natural language response.

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

### 3. Real-World Example
Suppose you are building a weather assistant. The user asks: *"What is the temperature in Dubai?"*
1. The app passes a tool schema `get_current_weather` to the LLM.
2. The LLM generates a tool call payload with the city: `{"location": "Dubai"}`.
3. The app's weather handler calls a live weather API, retrieves `{"temp": "42°C", "condition": "Sunny"}`, and submits it back to the LLM with the tool call ID.
4. The LLM reads this and responds: *"The current temperature in Dubai is 42°C and it is Sunny."*

### 4. This is how I would answer this
"Function calling is a stateless loop between the application and the LLM. First, the application sends the prompt along with the tools' JSON schemas. Second, the model returns a structured JSON payload requesting a tool call and specifying the arguments, pausing its generation. Third, the application parses that payload, runs the function locally, and sends the output back to the LLM, making sure to include the complete conversation history. Finally, the LLM reads that output and generates the natural language response."
