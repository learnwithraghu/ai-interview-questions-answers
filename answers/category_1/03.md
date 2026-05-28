# Question 3: Input Tokens Versus Output Tokens

**Question:** What is the difference between input tokens and output tokens in LLM APIs?

**Answer:**

### 1. Question Explanation
Alright, this one sounds simple, but it's a quick way for interviewers to see if you actually understand how LLM APIs **bill you and enforce limits**. They're not looking for a dictionary definition—they want to know you can explain what counts as input versus output on a real API call, why both matter for cost, and why both eat into the context window. A red flag is treating tokens like words, or saying "input is the prompt, output is the reply" without mentioning that chat history, system prompts, and retrieved RAG chunks all count as input too.

### 2. Concept Explanation
Before an LLM can process anything, raw text is converted into **tokens**—subword units from the model's vocabulary. APIs don't charge by characters or words; they charge and meter everything in tokens.

**Input tokens** are every token you **send to the model** in a single API request. That includes the system prompt, all prior user and assistant messages in the conversation, any RAG context you inject, tool definitions, and the current user message. If it goes into the request payload, it is input. When you see `prompt_tokens` in an API response, that's the input token count.

**Output tokens** are every token the model **generates back** to you—the completion. When you see `completion_tokens` in the response, that's the output count. If you're streaming, tokens arrive one at a time, but they're still counted the same way at the end.

The two are priced **separately** on almost every provider. Output tokens are typically more expensive per token than input tokens, because generation requires more compute than reading context. So a chatty model that writes 2,000-token essays costs more than one that gives terse 50-token answers—even if the input is identical.

Both input and output tokens also count toward the model's **context window limit**. A model with a 128K window doesn't mean 128K words—it means the combined total of input + output in that request must stay under the cap. This is why long chat histories cause timeouts and failures: your input tokens grow every turn, leaving less room for the model to respond.

A common misconception is that only the latest user message counts as input. In a stateless chat API, **you resend the entire message history every time**, so input tokens compound with every turn. Another misconception is ignoring output token limits—many APIs let you set `max_tokens` to cap generation, which is essential for controlling cost and preventing runaway responses.

### 3. Real-World Example
You're running a customer support bot on Claude. Each request sends an 800-token system prompt, 12,000 tokens of chat history, 2,000 tokens of retrieved policy docs, and a 100-token user question—that's **14,900 input tokens**. The model replies with a 400-token answer (**400 output tokens**). At typical pricing where output costs more per token than input, that 400-token reply might cost as much as several thousand input tokens. If you don't monitor both numbers in your observability dashboard, you'll wonder why your bill spiked when "the prompts didn't change"—the model just started generating longer responses.

### 4. This is how I would answer this
"Input tokens are everything you send to the model in the request—system prompt, chat history, RAG context, and the user's message. Output tokens are what the model generates back. In my experience, both count toward the context window limit, but APIs price them separately, and output is usually more expensive per token. That's why I always track `prompt_tokens` and `completion_tokens` in production and set a `max_tokens` cap so a single runaway response doesn't blow the budget."
