# Question 26: Caching LLM Responses

**Question:** How do you handle caching LLM responses to reduce API costs and latency? Explain the architectural difference between exact-match caching and semantic caching.

**Answer:**

### 1. Question Explanation
This question is aimed at understanding whether you can optimize real production usage of LLMs. Interviewers want to see you distinguish between simple caching strategies and smarter semantic approaches, while also understanding when caching is safe versus when it may return stale or incorrect answers.

### 2. Concept Explanation
Caching LLM responses is one of the most effective ways to reduce cost and improve latency. The simplest form is **exact-match caching**, where you store the complete prompt and its response. If the same prompt appears again, you can return the cached output directly. This is easy to implement and safe, but it only helps when your input is identical.

**Semantic caching** is more advanced. Instead of keying on exact prompt text, you create embeddings for requests and compare them to a cache of prior queries. If a new query is semantically similar to a cached one, you can reuse the existing answer or a partially computed result. This approach can dramatically increase cache hit rates for paraphrased questions and repeated intents.

Architecturally:
* Exact-match caching is typically implemented with a hash of the prompt or request payload and a simple key-value store.
* Semantic caching requires an embedding store, similarity search, and a strategy for deciding when a cached response is close enough to reuse safely.

The trade-off is that semantic caching introduces complexity and the risk of returning an answer that is not perfectly aligned. Therefore, it often works best for stable, low-risk content like FAQs, recommendations, or canned summaries.

### 3. Real-World Example
A knowledge base chatbot might use exact-match caching for repeated user prompts such as “What is your refund policy?” At the same time, it could use semantic caching to recognize closely related variants like “How do I get a refund?” and serve the same precomputed response when the similarity is high enough.

### 4. How Other Tools and Providers Handle This

**Anthropic Prompt Caching**
Anthropic offers server-side prompt caching at the API level. If your system prompt or long context document exceeds 1,024 tokens and you mark it with a `cache_control` breakpoint, Anthropic caches that prefix on their servers for up to 5 minutes. Subsequent requests that share the same prefix get a 90% discount on input token cost and faster time-to-first-token. This is not semantic caching — it’s exact prefix caching for repeated, stable context (system prompts, long documents). It’s the highest-ROI caching technique available because it requires no infrastructure changes, just an extra header.

**OpenAI Automatic Prompt Caching**
OpenAI automatically caches the first 1,024 tokens of a prompt (system + initial messages) at 50% cost discount when the same prefix is reused within an hour. Unlike Anthropic’s opt-in approach, this is fully automatic — you don’t add any headers or flags. The trade-off: you have less visibility into what’s being cached and less control over cache lifetime.

**Portkey Semantic Cache**
Portkey’s managed LLM gateway includes a built-in semantic cache. When a request comes in, Portkey generates an embedding of the prompt and checks it against a cache of prior queries. If the cosine similarity exceeds a configurable threshold, the cached response is returned without calling the model. Hit rates of 20–40% are common for FAQ-heavy chatbots. The advantage over rolling your own: no embedding infrastructure to maintain. The risk: Portkey holds your prompts and responses to power the cache.

**GPTCache (open-source)**
GPTCache is an open-source Python library purpose-built for LLM response caching. Supports both exact-match and semantic caching via pluggable backends (Redis, SQLite, Faiss, Milvus). You configure the similarity function, threshold, and eviction policy. It wraps the OpenAI SDK so existing code needs minimal changes. More flexible than a managed option but requires you to host the cache infrastructure and choose embedding models.

**Redis + custom embedding layer (DIY)**
Many teams build semantic caching by storing embeddings of prior prompts in Redis (using the Redis vector search module) alongside their cached responses. On each request: embed the prompt, query Redis for nearest neighbours above a threshold, return cached response if found. This gives full control but requires maintaining a Redis instance, choosing and hosting an embedding model, and tuning the similarity threshold per use case.

| Approach | Type | Infrastructure | Visibility | Best For |
|---|---|---|---|---|
| Anthropic Prompt Caching | Exact prefix (server-side) | None | Low | Repeated system prompts / long context |
| OpenAI Auto Caching | Exact prefix (server-side) | None | Very low | Automatic savings on stable prompts |
| Portkey Semantic Cache | Semantic (managed) | None | Medium | FAQ chatbots, managed gateway users |
| GPTCache | Exact + semantic (OSS) | Self-hosted | High | Teams wanting OSS control |
| Redis + embeddings (DIY) | Semantic (custom) | Self-hosted | Full | Teams with existing Redis + custom needs |

The layering strategy that maximises savings: apply server-side prompt caching (Anthropic/OpenAI) first — it’s free and requires no code. Add exact-match caching for high-frequency identical requests. Add semantic caching only if exact-match hit rates are low and the query set is paraphrase-heavy.

### 5. This is how I would answer this
“I’d start with exact-match caching for identical requests because it’s simple and reliable. For broader query reuse, I’d add semantic caching with embeddings so paraphrased questions can hit the cache too, but only after we validate that the reused response is still appropriate for the new query.”