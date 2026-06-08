# Question 15: Context Window Management

**Question:** A production LLM feature starts timing out and failing for 30% of users because the chat history (context window) grew too large. What strategies can you use to compress or manage the context dynamically?

**Answer:**

### 1. Question Explanation
Alright, this is a very real production scaling problem that every team hits eventually. The interviewer is checking if you understand how context windows work as a hard constraint, and whether you've thought about how to manage them gracefully at scale. A red flag is if you say "just use a model with a bigger context window"—that is a bandaid that ignores cost, latency, and the fact that LLMs degrade in quality on very long contexts anyway. They want to hear about proactive strategies like summarization, sliding windows, and message pruning.

### 2. Concept Explanation
First, let's understand *why* this happens. Every LLM API call has a hard limit on the total number of tokens it can process in a single request—this is the context window. For GPT-4o it's 128K tokens, for Claude 3.5 Sonnet it's 200K. But here's what trips teams up: **these limits include everything**—your system prompt, the entire chat history, the RAG context you've injected, and the model's output. In a long-running conversation, the chat history alone can balloon to tens of thousands of tokens, and eventually you hit the wall.

There's another problem people miss: even with models that have 128K+ context windows, **LLM quality degrades on very long contexts**. There's a well-documented phenomenon called the "lost in the middle" problem where models tend to underweight information in the middle of a long context and pay more attention to the beginning and end. So even if you could fit everything in, you probably shouldn't.

Instead of trying multiple fragmented solutions, the industry-standard production strategy is **Hybrid Asynchronous Summarization**. This approach combines token counting, sliding windows, and summarization, but critically runs it outside the user's response path to avoid latency spikes.

#### How Hybrid Asynchronous Summarization Works:
- **Verbatim Sliding Window:** Keep the last 10 messages of the conversation entirely verbatim. This ensures the LLM has crisp, immediate short-term context (it knows exactly what was said in the last few turns).
- **Asynchronous Compaction:** All messages older than the sliding window are sent to a fast, cheap model (like `gpt-4o-mini` or `claude-3-haiku`) to be summarized into a single, cohesive paragraph. This paragraph is prepended to the sliding window as the "Session Summary".
- **Background Execution (The Latency Fix):** Instead of running this token count and summarization synchronously during the user's request—which adds 2–5 seconds of latency—the application triggers this check *asynchronously in the background* right after returning the current response. When the user sends their next message, the pre-compacted context is loaded instantly from the database.

### 3. Real-World Example
A customer support chatbot started failing for long-running sessions—some conversations had 200+ message turns spanning an entire workday. The team implemented a hybrid strategy: they kept the last 10 messages verbatim (sliding window) and used GPT-4o-mini to summarize everything older into a 3-sentence "session summary" that was prepended to every API call. Timeouts dropped from 30% to under 0.5% within a day of the fix.

### 4. Implementation Example: FastAPI Background Tasks
To prevent latency spikes on the user's critical path, we can offload the token counting, summarization, and database updates to a background task. Here is a production-ready implementation pattern in Python using FastAPI's `BackgroundTasks` and `tiktoken`:

```python
import tiktoken
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()
tokenizer = tiktoken.encoding_for_model("gpt-4o")

TOKEN_COMPACTION_THRESHOLD = 80000  # Start compacting at 80k tokens
VERBATIM_MESSAGE_COUNT = 10         # Always keep the last 10 messages untouched

class ChatRequest(BaseModel):
    session_id: str
    user_message: str

async def compact_context_background(session_id: str):
    """
    Background worker that runs asynchronously after the user's response is sent.
    Ensures context is pre-compacted for the NEXT turn.
    """
    # 1. Fetch current conversation history from database
    messages = await db.get_conversation_history(session_id)
    
    # 2. Count current tokens in the history
    total_tokens = sum(len(tokenizer.encode(m["content"])) for m in messages)
    
    # 3. Trigger compaction if we exceed the safety threshold
    if total_tokens > TOKEN_COMPACTION_THRESHOLD:
        # Keep the latest N messages verbatim for short-term flow
        messages_to_keep = messages[-VERBATIM_MESSAGE_COUNT:]
        messages_to_summarize = messages[:-VERBATIM_MESSAGE_COUNT]
        
        # Call a fast, inexpensive model (e.g., gpt-4o-mini) to summarize the older history
        summary_text = await call_fast_llm_summarizer(messages_to_summarize)
        
        # Build the new compacted history format
        compacted_messages = [
            {"role": "system", "content": f"System Summary of early conversation: {summary_text}"}
        ] + messages_to_keep
        
        # 4. Atomically update the session state in the database
        await db.update_conversation_history(session_id, compacted_messages)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    # 1. Fetch pre-compacted history from DB (Instant - no in-flight LLM summarization latency)
    history = await db.get_conversation_history(request.session_id)
    
    # 2. Append the new user query
    current_payload = history + [{"role": "user", "content": request.user_message}]
    
    # 3. Call primary LLM on the critical path
    response = await call_primary_llm(current_payload)
    
    # 4. Persist the user message and model response to the database
    await db.save_message(request.session_id, role="user", content=request.user_message)
    await db.save_message(request.session_id, role="assistant", content=response)
    
    # 5. Schedule context compaction in the background (out of the request-response loop)
    background_tasks.add_task(compact_context_background, request.session_id)
    
    return {"response": response}
```

### 5. How Other Tools and Frameworks Handle This

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
| FastAPI / Celery | Asynchronous background summarization | High | High |

The key insight across all tools: **context management is a product decision, not just an engineering one**. Silent truncation is convenient but erodes trust. Manual compaction preserves trust but adds friction. The right choice depends on whether your users care about session continuity more than they care about simplicity.

### 6. This is how I would answer this
"My go-to solution for context window bloat is **Hybrid Asynchronous Summarization**. 

I would design the system to keep the last 10 messages verbatim for immediate short-term memory, while using a cheap model like `gpt-4o-mini` to summarize older messages into a rolling paragraph. Crucially, to prevent latency spikes on the critical path, I would run this summarization **asynchronously in the background** (using FastAPI's `BackgroundTasks` or a background worker like Celery) after responding to the user. This ensures that when the user sends their next message, the pre-compacted context is already generated and loaded instantly.

*If the interviewer asks about other strategies or trade-offs, I would mention:*
- **A pure sliding window**: Simple to implement but causes the model to completely forget early conversation details.
- **An external memory store (like Mem0 or a vector database)**: Excellent for long-term/cross-session key-fact retrieval, but introduces complexity with database lookups and relevance filtering.
- **Token counting checks**: I'd always keep a basic pre-call token count check (using `tiktoken`) as a safety guardrail to catch anomalies before hitting API limits."
