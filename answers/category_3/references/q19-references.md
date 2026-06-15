# References: Graceful Degradation When Retrieval Fails

Curated resources for deeper study on vector database high availability, circuit breaker patterns, fallback retrieval, and resilient AI architectures.

---

## Official Documentation

- [Pinecone — High Availability & Replicas](https://docs.pinecone.io/guides/indexes/understanding-indexes) — Serverless multi-AZ by default; pod tier supports configurable read replicas for failover.
- [Weaviate — Replication Architecture](https://weaviate.io/developers/weaviate/configuration/replication) — Multi-node clustering with configurable replication factors and automatic query re-routing on node failure.
- [Qdrant — Distributed Mode](https://qdrant.tech/documentation/guides/distributed_deployment/) — Replication factors and write consistency levels (one/quorum/all) borrowed from distributed database design.

## Provider & Cloud Docs

- [Elasticsearch — kNN Vector Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html) — Dense vector search via the kNN plugin, enabling Elasticsearch as both keyword and approximate semantic search fallback.
- [OpenSearch — k-NN Plugin](https://opensearch.org/docs/latest/search-plugins/knn/index/) — AWS-managed alternative supporting both exact and approximate nearest neighbor search alongside BM25.
- [Redis — Vector Similarity Search](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/) — Redis Stack's vector search capabilities for caching frequently-queried embeddings and chunks.

## Blog Posts & Articles

- [Martin Fowler — Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html) — Foundational article on the circuit breaker pattern: monitor dependency health, automatically "open" the circuit on failure, and route to fallbacks.
- [Microsoft — Resilience Patterns for Cloud Applications](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) — Azure architecture guide covering circuit breaker, retry, and fallback patterns for cloud-native apps.
- [Hybrid Search: Combining BM25 and Vector Search](https://weaviate.io/blog/hybrid-search-explained) — Weaviate's explanation of hybrid retrieval and why running both BM25 and vector search improves resilience and quality.
- [Building Resilient RAG Pipelines](https://www.pinecone.io/learn/retrieval-augmented-generation/) — Pinecone's learning guide on building production-grade RAG with redundancy and monitoring.

## Research Papers

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis et al. (2020). The original RAG paper from Facebook AI, establishing the retrieve-then-generate paradigm.
- [Hybrid Retrieval with Dense and Sparse Representations](https://arxiv.org/abs/2104.07186) — Luan et al. (2021). Shows that combining dense vector retrieval with sparse keyword retrieval (BM25) outperforms either alone.

## Framework Documentation

- [LangChain — Fallback Retriever Pattern](https://python.langchain.com/docs/how_to/fallbacks/) — Configure primary and fallback retrievers in a priority chain with automatic exception-based failover.
- [LlamaIndex — Retriever Modules](https://docs.llamaindex.ai/en/stable/module_guides/querying/retriever/) — Composable retriever architecture supporting vector, keyword, and hybrid retrieval with custom routing.
- [Resilience4j — Circuit Breaker for Java/Kotlin](https://resilience4j.readme.io/docs/circuitbreaker) — Popular circuit breaker library with configurable thresholds, useful as a reference implementation for Python equivalents.
