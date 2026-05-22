# Question 25: Caching LLM Responses

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

### 4. This is how I would answer this
“I’d start with exact-match caching for identical requests because it’s simple and reliable. For broader query reuse, I’d add semantic caching with embeddings so paraphrased questions can hit the cache too, but only after we validate that the reused response is still appropriate for the new query.”