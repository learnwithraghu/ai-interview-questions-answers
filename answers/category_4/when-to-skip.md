# Question 20: GenAI Orchestration Frameworks

**Question:** Explain the role of GenAI orchestration frameworks like LangChain or LlamaIndex. In what scenarios might you choose not to use them and write custom code instead?

**Answer:**

### 1. Question Explanation
Here the interviewer is probing whether you can differentiate between using a framework and building a tailored solution. They want to see that you understand how orchestration tools simplify common flows while also recognizing when they become too heavyweight or inflexible. A bad answer is one that blindly advocates for frameworks without any nuance.

### 2. Concept Explanation
GenAI orchestration frameworks like **LangChain** and **LlamaIndex** provide reusable building blocks for common tasks such as prompt management, chaining LLM calls, data retrieval, and memory. They are essentially opinionated scaffolding layers that let teams assemble agents, RAG pipelines, and tool-call workflows more quickly. The value comes from standardized components, integrated connectors for embeddings and vector stores, and utilities for caching, retries, and prompt templates.

However, these frameworks are not always the right choice. If you are building a very simple pipeline, or if your use case demands a highly optimized, minimal-latency path, the overhead of a full orchestration library can be unnecessary. Similarly, if your product has bespoke data flows or strict security rules, a custom implementation gives you tighter control and smaller attack surface.

So the decision is usually:
* Use a framework when you want to move fast, reduce boilerplate, and rely on battle-tested primitives.
* Avoid it when you need maximal performance, minimal dependency surface area, or when the framework’s abstraction leaks too much complexity.

### 3. Real-World Example
A SaaS team building a document Q&A feature might choose **LlamaIndex** because it offers built-in document loaders, retrievers, and query-chain patterns. On the other hand, a real-time conversational agent embedded in a regulated healthcare app might skip the framework and use a custom pipeline with direct API calls to the model, a bespoke cache layer, and tightly controlled prompt injection defenses.

### 4. This is how I would answer this
“I treat LangChain and LlamaIndex as useful accelerators when I need fast RAG or agent flows, because they give me common patterns out of the box. But if the use case is latency-sensitive, security-critical, or very custom, I’ll often write a smaller custom implementation instead of taking on the framework’s complexity.”