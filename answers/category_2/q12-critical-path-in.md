# Question 12: Critical Path In AI Pipelines

**Question:** You are building a RAG-based Q&A assistant. Which parts of your system will sit on the critical path, and which parts won't? Are you familiar with the term critical path?

**Answer:**

### 1. Question Explanation
Alright, when the interviewer asks you about the "critical path," they are testing whether you think like a systems engineer or just a framework user. A naive AI developer tends to treat a RAG pipeline as a single, monolithic block of synchronous steps: load history, embed, search, fetch, prompt, call LLM. The interviewer wants to see if you can analyze this sequence, identify where user-perceived latency actually comes from, and apply the concept of the **critical path** to surgically separate query-dependent steps from background tasks. A big red flag is not knowing what a critical path is or failing to see how steps like user profile loading or observability logging can be moved off of it.

### 2. Concept Explanation
The term **critical path** is a fundamental systems engineering concept. In any user-facing application, the critical path is the sequence of dependent operations that must run synchronously between the user submitting a request and receiving a response. Every single millisecond spent on the critical path directly increases user-perceived latency. 

To determine whether a component or step belongs on the critical path, we can apply a simple decision rule:

> **A step must sit on the critical path if and only if it depends on the user's current query text (or the output of a prior step that does). If it does not depend on the query, it should be moved off the critical path.**

Let's classify the typical parts of a RAG-based Q&A assistant using this rule:

#### On the Critical Path (Query-Dependent)
*   **Query Embedding:** You cannot search a vector database until you embed the user's actual question. This must happen synchronously.
*   **Vector Database Search:** The retrieval of relevant document IDs/vectors directly depends on the query embedding.
*   **Document Text Retrieval:** Once you have the matching document IDs, you must fetch the corresponding text chunks from object storage or a database to feed the LLM.
*   **LLM Prompt Assembly:** Constructing the final prompt requires both the query and the retrieved document context.
*   **LLM Generation / Inference:** The model call is the most expensive step and must run synchronously to stream or return the final answer.
*   **Input Guardrails (if blocking):** Any synchronous safety checks on the input query to prevent prompt injection must run before LLM processing.

#### Off the Critical Path (Candidates for Deferral or Parallelization)
*   **User Preferences & Profile Loading:** Knowing the user's preferences, language, or system settings does *not* require the query. This data can be pre-loaded when the user's session starts and cached in memory.
*   **Conversation History Fetching:** While needed for context, the historical chat turns can be pre-fetched or updated in a local cache in the background right after the previous assistant response is sent.
*   **Observability & Logging Traces:** Logging prompt inputs, token counts, and latency metrics to tools like Langfuse or Helicone should never block the user. These should be queued and sent asynchronously via background threads or batch workers.
*   **Post-Generation Analytics & Guardrails:** Running evaluations on response quality or flagging toxic output for moderation (unless you want to block the user) can happen out-of-band.

### 3. Real-World Example
Consider an AI-powered code search tool. When first deployed, the end-to-end response time was 3.8 seconds. A latency trace showed: 1.1 seconds loading the developer's workspace metadata and profile, 0.1 seconds embedding the query, 0.4 seconds searching the codebase index, 0.4 seconds fetching document text, 0.2 seconds prompt building, and 1.6 seconds LLM inference. 

By applying critical path analysis, the team realized the 1.1 seconds spent loading developer workspace metadata was completely independent of the query text. They moved this step off the critical path by pre-loading workspace metadata in the background the moment the developer opened the IDE panel. They also discovered that sending observability traces to their monitoring provider added a blocking 150ms round-trip; they wrapped this call in an asynchronous background worker. After these optimizations, the critical path was reduced solely to query-dependent steps, bringing the response time down to 2.5 seconds—a 34% speedup with zero changes to the LLM or vector database.

### 4. This is how I would answer this
"Yes, I'm familiar with the term. In systems engineering, the critical path is the sequence of synchronous operations that directly determines user-perceived latency. 

When building a RAG-based assistant, I use a simple filter to decide what belongs on the critical path: *does this step depend on the user's query text?* 

Steps like embedding the question, searching the vector database, fetching the matching document content, and calling the LLM are query-dependent, so they must stay on the critical path. However, metadata loading, like fetching the user's profile or preferences, is query-independent and should be pre-loaded and cached when the session opens. Similarly, writing telemetry data, audit logging, and tracing to systems like Langfuse or Helicone should be sent asynchronously off the critical path using a background worker to avoid adding blocking round-trip latency."
