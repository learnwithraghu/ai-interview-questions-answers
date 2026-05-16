# Question 18: Vector Database Failures

**Question:** Your vector database goes down, breaking the semantic search feature of your application. How do you design a highly available GenAI architecture that gracefully degrades when retrieval fails?

**Answer:**

### 1. Question Explanation
Alright, this is a system design and reliability question. The interviewer wants to know if you treat your vector database as a critical dependency and have planned for its failure. A major red flag is if you have no answer beyond "we'd fix the database"—that tells them you haven't thought about graceful degradation. They are looking for the key concept of "graceful degradation": the idea that when one component fails, the system should continue to function at a reduced capacity rather than going down completely. They want to hear about fallback retrieval strategies and redundancy.

### 2. Concept Explanation
This question is fundamentally about system design and the principle of **graceful degradation**—the idea that when one part of your system fails, the rest should keep working at a reduced level of capability, rather than failing entirely.

Think of it this way: your vector database is a single point of failure. The moment it goes down, if your only response is to return an error to the user, you've built a brittle system. Production-grade architectures plan for this failure from day one.

**Start with redundancy.** Most managed vector database providers (Pinecone, Weaviate Cloud, Qdrant Cloud) offer multi-region deployments and read replicas. A read replica is a copy of your vector data in a separate availability zone or region that handles read queries. Your primary instance handles writes. If the primary goes down, your load balancer routes traffic to the replica automatically. This handles most unplanned outages without any application-level fallback code.

**Add a circuit breaker.** Don't wait for your users to experience 30-second timeouts before you react. Add a health-check endpoint to your vector database connection and wire it into a circuit breaker—a piece of infrastructure logic that monitors the health of a dependency and automatically "opens" (stops routing traffic to it) when it detects failures. A properly configured circuit breaker can detect a vector DB outage within 5 seconds and switch to a fallback before most users even notice something is wrong.

**Design a degradation hierarchy.** When the vector DB is unavailable, what do you fall back to? Think of it as a hierarchy of decreasing quality but increasing availability:

1. **Keyword Search (BM25/Elasticsearch):** Your first fallback. You likely already have your documents indexed somewhere—Elasticsearch, OpenSearch, or even a SQL full-text search. Less semantically aware, but still genuinely useful.
2. **Cached Results (Redis):** Pre-populate a Redis cache with the retrieved chunks for your most common queries. If the vector DB is down, serve these stale cached results. Users querying frequently-asked questions won't notice a thing.
3. **LLM-Only Mode:** If all retrieval fails, route to the LLM with no RAG context, relying purely on its training data. Show a banner: "Document search is temporarily unavailable. Answers may be less specific." This is honest with the user and keeps the product functional.

**User communication matters.** At each degradation level, show the user a clear, non-technical status message so they understand why quality might be reduced. Transparency builds trust; silent degradation erodes it.

### 3. Real-World Example
A document Q&A platform for enterprise clients experienced a 45-minute Pinecone outage. Because they had implemented a circuit breaker that detected the failure within 5 seconds, all traffic was automatically rerouted to an Elasticsearch keyword search fallback. Users saw a banner noting that "AI search is operating in basic mode," but continued to get answers. After the Pinecone cluster recovered, traffic shifted back automatically with zero manual intervention.

### 4. This is how I would answer this
"The key principle is graceful degradation—the app should keep working at reduced capacity, not crash entirely. I'd achieve this with a circuit breaker that detects vector DB failures within seconds and automatically switches to a fallback strategy. My primary fallback would be a keyword search against the same document corpus—less accurate, but functional. I'd also cache results for common queries in Redis so even if both the vector DB and keyword search are struggling, we can serve something. Throughout all of this, I'd show users a clear in-app banner so they know retrieval quality is temporarily reduced."
