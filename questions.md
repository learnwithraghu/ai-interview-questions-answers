# GenAI Engineer Interview Questions

Question bank for the AI Engineer Interview Bootcamp.

---

### Section 1: Core GenAI Concepts & Foundations

1. **[Easy]** What is the difference between a system prompt, a user prompt, and an assistant response in modern chat-based LLM APIs?

2. **[Medium]** Explain the concept of few-shot prompting and how it differs from zero-shot prompting. Provide an example of when you would use it.

3. **[Medium]** What is the difference between input tokens and output tokens in LLM APIs?

4. **[Medium]** What is the purpose of `AGENTS.md` in a GitHub repository?

5. **[Hard]** What is ReAct concept in LLM?

6. **[Medium]** In your AI coding experience, what is an example of an LLM hallucination you saw, and why do you think it happened?

---

### Section 2: Real-World Scenario Architecture

7. **[Easy]** You need to extract structured JSON data (like user profiles) from unstructured customer emails. How would you design the prompt and API call to guarantee valid JSON output?

8. **[Medium]** In a RAG system, why should retrieval and generation be treated as two separate systems that can fail independently?

9. **[Medium]** You are an hour into a complex debugging session with Claude Code — many files edited, lots of back-and-forth. Responses are getting less focused and you're approaching the context window limit. How do you keep the session going without losing your work or starting over?

10. **[Medium]** Your application uses an LLM to generate SQL queries from natural language. How do you handle database schema changes and prevent the LLM from hallucinating column names?

11. **[Hard]** A stakeholder wants an LLM application that can search the web, query an internal database, and send an email. How do you design the tool-calling/function-calling architecture to route these intents reliably and safely?

12. **[Hard]** Your RAG application is returning irrelevant context for complex, multi-part user queries. What advanced retrieval strategies (e.g., query expansion, Hyde, cross-encoder re-ranking) would you implement to fix this?

13. **[Hard]** You are evaluating two different LLMs for a summarization task. One is cheaper but potentially less accurate. How do you set up an automated evaluation pipeline (e.g., using LLM-as-a-judge) to quantify the trade-off at scale?

---

### Section 3: Production Incidents & Reliability

14. **[Easy]** Your customer-facing chatbot suddenly starts ignoring its system instructions and answering inappropriate questions. What is likely happening, and how do you stop it immediately?

15. **[Medium]** A production LLM feature starts timing out and failing for 30% of users because the chat history (context window) grew too large. What strategies can you use to compress or manage the context dynamically?

16. **[Medium]** During a product launch, your primary LLM API provider hits a severe rate limit (HTTP 429), causing complete service failure. How do you implement robust fallback mechanisms and load balancing across different models?

17. **[Hard]** A malicious prompt injection attack successfully tricks your AI agent into executing an unauthorized API call using its connected tools. How do you secure the agent's function-calling capabilities and implement a "human-in-the-loop" safeguard?

18. **[Hard]** Users report that your LLM app occasionally hallucinates highly realistic but fake citations and URLs. How do you detect, mitigate, and filter hallucinated facts in a production pipeline before the user sees them?

19. **[Hard]** Your vector database goes down, breaking the semantic search feature of your application. How do you design a highly available GenAI architecture that gracefully degrades when retrieval fails?

---

### Section 4: Modern AI Stack & Tooling

20. **[Easy]** What are the main differences between using a managed LLM API (like OpenAI GPT-4 or Anthropic Claude) versus accessing an open-weight model (like Llama 3) hosted on a cloud provider like Groq or Together AI?

21. **[Easy]** Explain the role of GenAI orchestration frameworks like LangChain or LlamaIndex. In what scenarios might you choose *not* to use them and write custom code instead?

22. **[Medium]** Compare the trade-offs of using a dedicated Vector Database (e.g., Pinecone, Weaviate) versus using vector extensions in a traditional relational database (e.g., `pgvector` in PostgreSQL).

23. **[Medium]** What is the purpose of LLM observability and tracing tools (e.g., Langfuse, Helicone, LangSmith)? What specific metrics are critical to track for a GenAI application?

24. **[Medium]** Walk me through exactly how you would use OpenAI's Function Calling API to allow an LLM to interact with an external REST API (like checking the weather).

25. **[Hard]** You need to build a complex, multi-agent workflow where a "researcher" agent gathers data and a "writer" agent drafts a report. How do you manage state, memory, and routing using frameworks like LangGraph or AutoGen?

26. **[Hard]** How do you handle caching LLM responses to reduce API costs and latency? Explain the architectural difference between exact-match caching and semantic caching.

27. **[Medium]** Where should inference run — browser, edge, server — and why?

28. **[Medium]** In the context of building and testing AI agents, what is the difference between a "tool" and a "harness"?

