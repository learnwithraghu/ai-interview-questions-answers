# Question 8: Debugging RAG Retrieval

**Question:** You are building a document Q&A bot. Users complain that the bot says "I don't know" even when the answer is clearly in the document. How do you troubleshoot whether the failure is in the retrieval step or the generation step?

**Answer:**

### 1. Question Explanation
Alright, this is a classic RAG debugging scenario and one of the most common issues you'll face in production. The interviewer is checking if you have a systematic debugging mindset—not just guessing. A major red flag is if you say "I'd just tweak the prompt"—that shows you don't understand how to isolate the two independent failure points in a RAG pipeline. They want to see that you know how to test retrieval in isolation, test generation in isolation, and then trace where the chain is breaking. This is all about structured, methodical troubleshooting.

### 2. Concept Explanation
The most important mental model for debugging RAG is this: **a RAG pipeline is two separate systems glued together, and each one can fail independently.** The moment you internalize this, you stop guessing and start isolating.

**The two failure modes are:**

**Failure Mode 1 — Retrieval is broken.** The right chunks containing the answer were never fetched from the vector database. The LLM literally never saw the information it needed. No amount of prompt engineering will fix this because you're trying to get blood from a stone.

How to confirm: **Log your retrieved chunks.** This is the single most important debugging step in RAG. For every failing query, print or store the raw chunks that came back from the vector database and read them. If the answer isn't in those chunks, retrieval is your problem. Common causes include: chunks are too small and context gets split across chunks, the embedding model doesn't capture the domain-specific language, or the similarity threshold is too strict and is cutting off relevant results.

**Failure Mode 2 — Generation is broken.** The right chunks *were* retrieved, but the LLM refused to use them or ignored them. This is surprisingly common.

How to confirm: **Manually inject the correct chunks directly into the prompt, bypassing retrieval entirely.** Copy the chunks you know contain the answer, paste them directly into a test prompt, and send it to the LLM. If the model *still* says "I don't know," your problem is in generation. Common causes: the system prompt has an overly strict refusal instruction ("Only answer if you are 100% certain"), the context is being truncated because it's too long, or the retrieved chunks are formatted in a way the model doesn't parse well.

**Once you've isolated the side that's failing, the fixes become obvious:** for retrieval, improve chunking strategy, switch embedding models, or add re-ranking. For generation, relax the system prompt, fix context formatting, or use a model with a larger context window.

### 3. Real-World Example
A legal firm's document Q&A bot kept saying "I cannot find that information" for questions about specific contract clauses. By logging the retrieved chunks, an engineer discovered the retriever was returning unrelated sections. The fix was switching from fixed-size chunking to semantic chunking and lowering the similarity threshold. After that change, retrieval was accurate and the "I don't know" responses disappeared entirely.

### 4. This is how I would answer this
"I treat RAG as two separate systems that can fail independently. First, I'd log all retrieved chunks for the failing queries to check if the right content is actually being fetched. If the right chunks are there but the model still says 'I don't know', I know it's a generation problem—I'd check if the system prompt is too restrictive or if the context is being truncated. If the wrong chunks are being retrieved, that's a retrieval problem, and I'd look at improving my chunking strategy or adding re-ranking. The key is isolating which side is failing before touching anything."
