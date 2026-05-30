# Question 15: Context Window Management

**Question:** A production LLM feature starts timing out and failing for 30% of users because the chat history (context window) grew too large. What strategies can you use to compress or manage the context dynamically?

**Answer:**

### 1. Question Explanation
Alright, this is a very real production scaling problem that every team hits eventually. The interviewer is checking if you understand how context windows work as a hard constraint, and whether you've thought about how to manage them gracefully at scale. A red flag is if you say "just use a model with a bigger context window"—that is a bandaid that ignores cost, latency, and the fact that LLMs degrade in quality on very long contexts anyway. They want to hear about proactive strategies like summarization, sliding windows, and message pruning.

### 2. Concept Explanation
First, let's understand *why* this happens. Every LLM API call has a hard limit on the total number of tokens it can process in a single request—this is the context window. For GPT-4o it's 128K tokens, for Claude 3.5 Sonnet it's 200K. But here's what trips teams up: **these limits include everything**—your system prompt, the entire chat history, the RAG context you've injected, and the model's output. In a long-running conversation, the chat history alone can balloon to tens of thousands of tokens, and eventually you hit the wall.

There's another problem people miss: even with models that have 128K+ context windows, **LLM quality degrades on very long contexts**. There's a well-documented phenomenon called the "lost in the middle" problem where models tend to underweight information in the middle of a long context and pay more attention to the beginning and end. So even if you could fit everything in, you probably shouldn't.

The solution is proactive context management—don't wait for the API to reject your request. Here are the strategies, from simplest to most sophisticated:

**Token Counting Before Every Call:** Use a tokenizer (like tiktoken for OpenAI models) to count the tokens in your payload *before* sending it. If you're at 80% of the limit, trigger compression. This simple check alone prevents most production timeouts.

**Sliding Window:** Keep only the last N messages. It's the simplest approach and works well for stateless tasks, but it has an obvious flaw: if a critical piece of information was mentioned early in the conversation (like the user's name, their account number, or a specific constraint), that's now gone.

**Conversation Summarization (the sweet spot):** When the context exceeds your threshold, run the older messages through a fast, cheap LLM (GPT-4o-mini costs a fraction of GPT-4o) and ask it to produce a 2–3 sentence summary capturing the key facts. Replace all those old messages with this summary. You keep the essential context while dramatically cutting the token count. Combine this with a sliding window for the most recent messages—always keep the last 5–10 messages verbatim so the model has crisp short-term context.

**External Memory Store:** For sophisticated applications, extract key entities and facts from the conversation (user preferences, constraints, important decisions made) and store them in an external key-value store or vector database. At the start of each API call, retrieve only the most relevant stored facts for the current query. This lets you maintain "infinite" memory without ever bloating the context window.

### 3. Real-World Example
A customer support chatbot started failing for long-running sessions—some conversations had 200+ message turns spanning an entire workday. The team implemented a hybrid strategy: they kept the last 10 messages verbatim (sliding window) and used GPT-4o-mini to summarize everything older into a 3-sentence "session summary" that was prepended to every API call. Timeouts dropped from 30% to under 0.5% within a day of the fix.

### 4. This is how I would answer this
"The first thing I'd do is add proactive token counting before every API call—if we're approaching the context limit, we trigger compression before the timeout happens. My preferred strategy is conversation summarization: once the history gets too long, I run a fast, cheap model to compress the older messages into a short summary and replace them with that. I'd combine that with a sliding window that always preserves the last 10 messages verbatim so recent context is never lost. For power users who have long sessions with critical facts scattered throughout, I'd also explore extracting key entities into an external memory store."
