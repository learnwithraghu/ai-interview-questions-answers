# Question 24: OpenAI Function Calling for REST APIs

**Question:** Walk me through exactly how you would use OpenAI's Function Calling API to allow an LLM to interact with an external REST API (like checking the weather).

**Answer:**

### 1. Question Explanation
The interviewer wants to know whether you understand the practical mechanics of function calling, not just the theory. They are testing if you can design a safe, structured integration that turns model output into concrete API actions. A weak response is one that describes the API in abstract terms without walking through the actual request/response flow.

### 2. Concept Explanation
OpenAI’s Function Calling API lets you define a set of functions with names, parameters, and schemas. The model is then asked to choose whether to call one of those functions and to generate a JSON payload that matches the schema. This is powerful because it lets the model plan and execute actions without us needing to parse free-form text.

The flow is typically:
1. Define the external function schema, including required parameters and types.
2. Send the user message plus the function definitions to the model.
3. The model returns a response indicating a function call, with arguments in JSON.
4. Your application executes the external REST API using those arguments.
5. Return the API response to the model if you want it to generate a natural-language answer for the user.

For a weather check, you might define a function like `get_weather(city, date)` and let the model fill in the values. The model does not actually call the REST service itself; it tells your app what to invoke. That means you can validate the arguments, enforce permission rules, and keep the actual API keys secret.

### 3. Real-World Example
For a travel assistant, I would expose a function called `fetch_weather_forecast` with parameters `location` and `date`. When the user asks “Will it rain in Seattle tomorrow?”, the model returns a function call with `location=Seattle` and `date=2025-06-15`. My backend then calls the weather API, receives the forecast JSON, and optionally sends that result back to the model so it can compose a human-friendly reply.

### 4. How Other Providers Implement This Pattern

**Anthropic Tool Use**
Anthropic's equivalent is called “tool use” rather than “function calling,” but the mechanics are nearly identical. You define tools with a `name`, `description`, and `input_schema` (JSON Schema). The model returns a `tool_use` content block with the tool name and generated inputs. Your application executes the tool and returns the result in a `tool_result` content block on the next turn. One notable difference: Anthropic supports parallel tool calls — the model can request multiple tools simultaneously in a single response, which reduces round-trips for complex tasks (e.g., fetch weather AND check calendar at the same time).

**Google Gemini Function Calling**
Gemini's function calling follows the same declare-call-return pattern. Gemini supports a `mode` parameter on function calling: `AUTO` (model decides whether to call a function), `ANY` (model must call at least one function), or `NONE` (model must not call functions). This explicit mode control is useful when you need to guarantee tool invocation for routing workflows. Gemini 1.5 Pro also supports parallel function calls natively.

**JSON Mode (model-agnostic fallback)**
Before structured function calling existed, teams used “JSON mode” — instructing the model via system prompt to always return a specific JSON schema. Most providers now offer a formal `response_format: { type: “json_object” }` parameter. JSON mode doesn't give the model a catalogue of available tools to choose from; it just constrains output format. Useful for simpler structured extraction tasks where you don't need tool selection logic, but less safe for multi-tool routing because the model can hallucinate field names.

**LangChain Tool Abstraction**
LangChain wraps provider-specific function calling behind a unified `Tool` class. You define tools as Python functions with a docstring (the docstring becomes the tool description sent to the model), and LangChain handles serialising the schema for whichever provider you're using (OpenAI, Anthropic, Gemini). This makes it easy to swap providers without rewriting tool definitions. The downside: LangChain's abstraction adds a layer that can obscure errors and makes debugging harder.

**OpenAI Strict Mode**
OpenAI introduced `strict: true` for function definitions, which constrains the model to only output arguments that exactly conform to the provided JSON schema (no additional properties, no missing required fields). This eliminates a class of argument hallucination attacks and malformed outputs. When strict mode is on, the schema is compiled into the model's constrained decoding at inference time. The requirement: your schema must be fully defined with no `additionalProperties: true` anywhere in the tree.

| Provider | Term Used | Parallel Calls | Strict Schema | Unique Feature |
|---|---|---|---|---|
| OpenAI | Function Calling | Yes | Yes (strict mode) | Strict mode for argument safety |
| Anthropic | Tool Use | Yes | Via JSON Schema | Parallel tool use natively supported |
| Google Gemini | Function Calling | Yes | No | `ANY` / `NONE` mode control |
| LangChain | Tool (abstraction) | Depends on backend | Depends on backend | Provider-agnostic tool definitions |
| JSON mode (any provider) | Structured output | N/A | Partial | No tool catalogue, output format only |

The core invariant across all implementations: **the model never calls the tool itself**. It proposes a call; your application validates and executes it. That separation is what keeps API keys secret and gives you the ability to apply argument validation, permission checks, and HITL gates before anything runs.

### 5. This is how I would answer this
“I would define the REST integration as a typed function schema, send that definition to OpenAI alongside the user query, and let the model choose to invoke the function. My backend would validate the generated arguments, call the external weather API, and then either return the raw data or let the model summarize it for the user.”