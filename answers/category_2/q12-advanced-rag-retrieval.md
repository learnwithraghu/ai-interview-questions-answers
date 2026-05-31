# Question 12: Advanced Retrieval Strategies

**Question:** Your RAG application is returning irrelevant context for complex, multi-part user queries. What advanced retrieval strategies (e.g., query expansion, HyDE, cross-encoder re-ranking) would you implement to fix this?

**Answer:**

### 1. Question Explanation
Okay everyone, this is where basic RAG ends and real RAG engineering begins! The interviewer is asking this because they know that a naive single-vector similarity search completely breaks down when users ask complex, multi-part questions. They want to see that you know *why* it breaks—a single query vector can't represent multiple intents at once—and that you have a toolkit of specific strategies to fix it. A red flag is if you can only name one technique. They are looking for you to show depth by explaining query expansion, HyDE, or re-ranking and knowing *when* to apply each one.

### 2. Concept Explanation
To understand why these advanced strategies exist, you first need to appreciate the core limitation of basic RAG: **you're representing the user's entire question as a single vector, and then doing a single nearest-neighbour lookup.** For simple, focused questions this works fine. But the moment a user asks something like "What were the risk factors in Q3 and how do they affect the 2025 guidance?"—you have two distinct information needs packed into one query. A single vector cannot optimally represent both at the same time. You'll get chunks relevant to one intent but miss the other.

Here are the main strategies to fix this, in order of increasing complexity:

**Query Decomposition:** You use the LLM itself to break the complex question into multiple simpler sub-questions before retrieval even starts. Each sub-question gets its own retrieval pass, and then you merge all the retrieved chunks before passing them to the final LLM call. This directly solves the "multiple intents in one query" problem. It's your first and most impactful fix.

**HyDE (Hypothetical Document Embeddings):** This one is clever. Instead of embedding the user's *question*, you first ask the LLM to write a *hypothetical answer* to the question—even if the answer is made up. Then you embed that hypothetical answer and use it for retrieval. Why does this work? Because the embedding of a full, properly written answer is semantically much closer in vector space to the actual document chunks than the embedding of a short, conversational question. You're searching for "answer-shaped" content with "answer-shaped" queries.

**Cross-Encoder Re-ranking:** This is a two-stage retrieval approach. In stage 1, you use fast vector search (bi-encoder) to get the top-50 candidate chunks. These are rough candidates—fast but imprecise. In stage 2, you run a *cross-encoder*—a model that takes the query and a candidate chunk *together* as input and produces a single relevance score. Cross-encoders are much more accurate than bi-encoders at judging relevance, but too slow to run against your entire corpus. So you use the fast bi-encoder to shortlist, then the accurate cross-encoder to re-rank. You pass only the top-5 re-ranked chunks to the LLM.

**Hybrid Search (BM25 + Dense):** Sometimes the best match is an exact keyword match (like a product code, a legal term, or a proper name) that the vector space might not capture perfectly. Hybrid search runs both a keyword search and a vector search in parallel and merges the results using **Reciprocal Rank Fusion (RRF)**—a simple formula that combines rankings from both lists into a single unified ranking. This gives you the best of both worlds.

### 3. Real-World Example
A financial research tool receives complex queries like "What were the risk factors mentioned in the Q3 2024 earnings call, and how do they relate to the guidance given for 2025?" A naive single-query RAG returns irrelevant sections. The fix: decompose into two sub-queries (risk factors in Q3, and 2025 guidance), retrieve top-50 chunks per sub-query, merge, then run a cross-encoder re-ranker to select the top-10 most relevant chunks for the final LLM prompt.

### 4. This is how I would answer this
"A single vector query breaks down for complex questions because one vector can't capture multiple intents. My go-to fix is query decomposition—I break the complex question into simpler sub-queries and retrieve independently for each one. I'd also consider HyDE, where I ask the LLM to generate a hypothetical answer first and use that for retrieval since it's semantically closer to the actual documents. On top of that, I'd add a cross-encoder re-ranker as a second pass to filter down the merged results to only the most relevant chunks before sending them to the LLM. If I'm working with structured enterprise data, I may also use a vector DB over table and column metadata to semantically identify the most relevant parts of the schema, while still using the live database schema as the source of truth."
