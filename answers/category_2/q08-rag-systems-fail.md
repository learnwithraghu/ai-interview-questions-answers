# Question 8: RAG Systems Fail Independently

**Question:** In a RAG system, why should retrieval and generation be treated as two separate systems that can fail independently?

**Answer:**

### 1. Question Explanation
Alright, this is a subtle but very important RAG architecture question. The interviewer is checking whether you understand RAG as a pipeline, not as one magic "ask documents" feature. A red flag is blaming every bad answer on the LLM or immediately tweaking the prompt. In production, you need to know whether the retriever failed to supply evidence or the generator failed to use evidence that was already there. That separation is what makes RAG debuggable.

### 2. Concept Explanation
The clean mental model is this: **RAG is two systems glued together.** The retriever finds candidate evidence. The generator reads that evidence and writes the answer. Those two stages depend on each other, but they do not fail in the same way.

**Retrieval failure** means the right information never reached the model. Maybe the chunking split the answer across documents. Maybe the embedding model did not capture the user's vocabulary. Maybe the similarity threshold was too strict. In this case, the LLM is not really the problem. It cannot answer from evidence it never received.

**Generation failure** means the right information was retrieved, but the model did not use it correctly. Maybe the prompt is too restrictive. Maybe the context is too long and got truncated. Maybe the chunks are formatted poorly, so the model misses the relevant sentence. Here, retrieval did its job, but generation failed.

This separation matters because it stops random debugging. If retrieval is broken, prompt changes are a distraction. You should inspect chunks, improve chunking, tune embeddings, add metadata filters, or use re-ranking. If generation is broken, changing the vector database is a distraction. You should fix prompt instructions, context formatting, citation requirements, or model choice.

The production habit is to log the boundary between the two systems: the exact query, retrieved chunks, scores, metadata, and final prompt sent to the model. Once you can see that boundary, you can tell which side failed instead of guessing.

### 3. Real-World Example
Imagine a support bot for a SaaS product. A user asks about refund eligibility. The bot gives the wrong answer. If the retrieved chunks only contain billing setup docs, retrieval failed. If the retrieved chunks contain the refund policy but the model ignores the "within 14 days" clause, generation failed. The fix depends entirely on which side broke.

### 4. This is how I would answer this
"I treat RAG as two systems: retrieval finds the evidence, and generation turns that evidence into an answer. They can fail independently. If the right chunks are missing, that's a retrieval problem. If the right chunks are present but the model still answers badly, that's a generation problem. Separating those two failure modes helps me debug systematically instead of randomly changing prompts or vector settings."
