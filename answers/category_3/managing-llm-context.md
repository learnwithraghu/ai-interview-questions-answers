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

### 4. How Other Tools and Frameworks Handle This

**OpenAI Assistants API (Threads)**
OpenAI's managed Threads API handles context management automatically. When you use the Assistants API, conversation history is stored server-side in a "thread" and OpenAI's infrastructure decides what to include in each API call — you never manage the token budget yourself. The model silently truncates older messages when the window fills up. The trade-off: you lose control over *what* gets dropped, and there's no transparency about when truncation happens.

**LangChain Memory**
LangChain has a dedicated `memory` module with several strategies: `ConversationBufferMemory` (keep everything, fail at limit), `ConversationSummaryMemory` (summarise on overflow), `ConversationSummaryBufferMemory` (hybrid — summarise old, keep recent verbatim), and `VectorStoreRetrieverMemory` (store everything, retrieve only relevant turns per query). The framework makes the strategy swappable with a single line change — good for experimenting. The downside: LangChain's memory abstractions have been inconsistent across versions.

**Mem0 (open-source)**
Mem0 is a memory layer specifically designed for AI applications. It extracts structured facts from conversations (names, preferences, decisions, constraints) and stores them in a vector database. On each new turn, it retrieves the top-K most relevant facts by similarity and injects them into the context. This is the "external memory store" approach described in section 2, packaged as a reusable library. It can maintain effectively infinite memory with a constant, small token footprint per request.

**ChatGPT's Memory Feature**
OpenAI's consumer ChatGPT uses a two-layer system: in-session context (standard sliding window) plus a separate "memory" that persists across sessions as a list of saved facts ("User prefers concise answers", "User works at a fintech company"). The model decides what to save, which is convenient but opaque — you can't reliably predict what it will remember or forget. The key insight: persistent facts and ephemeral conversation history are treated as separate concerns, not one growing buffer.

**Claude Code's `/compact` Command**
Claude Code's approach is a manual LLM-summarisation trigger with full user visibility. You run `/compact`, Claude generates a structured summary of the session (decisions made, files edited, open tasks), and that summary replaces the full history. You can inspect the summary before continuing. Unlike the Assistants API's silent truncation, the user controls timing and can verify what was preserved. (See the dedicated `/compact` question for a full breakdown.)

| Tool | Strategy | User Control | Transparency |
|---|---|---|---|
| OpenAI Assistants API | Silent truncation | None | Opaque |
| LangChain Memory | Configurable (buffer / summary / vector) | High | Medium |
| Mem0 | Structured fact extraction + retrieval | Medium | High |
| ChatGPT Memory | Persistent facts + session window | Low | Low |
| Claude Code `/compact` | Manual LLM summarisation | Full | Full |

The key insight across all tools: **context management is a product decision, not just an engineering one**. Silent truncation is convenient but erodes trust. Manual compaction preserves trust but adds friction. The right choice depends on whether your users care about session continuity more than they care about simplicity.

### 5. This is how I would answer this
"The first thing I'd do is add proactive token counting before every API call—if we're approaching the context limit, we trigger compression before the timeout happens. My preferred strategy is conversation summarization: once the history gets too long, I run a fast, cheap model to compress the older messages into a short summary and replace them with that. I'd combine that with a sliding window that always preserves the last 10 messages verbatim so recent context is never lost. For power users who have long sessions with critical facts scattered throughout, I'd also explore extracting key entities into an external memory store."
