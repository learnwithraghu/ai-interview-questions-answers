# References: Securing AI Agent Function Calling

Curated resources for deeper study on agent security, prompt injection defence, and human-in-the-loop safeguards.

---

## Official Documentation

- [OpenAI Function Calling (strict mode)](https://platform.openai.com/docs/guides/function-calling) — Explains `strict: true` parameter that enforces JSON schema at inference time, preventing argument manipulation.
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — Claude's tool use protocol including best practices for minimal footprint and confirmation patterns.
- [Microsoft AutoGen UserProxyAgent](https://microsoft.github.io/autogen/docs/reference/agentchat/user_proxy_agent/) — Multi-agent framework with `human_input_mode` settings (`ALWAYS`, `NEVER`, `TERMINATE`) for configurable HITL.

## Provider & Cloud Docs

- [Lakera Guard API](https://www.lakera.ai/lakera-guard) — Managed prompt injection detection API (~10ms latency) with continuously updated threat database.
- [NVIDIA NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/index.html) — Open-source framework for adding programmable guardrails to LLM-powered applications, including input/output rails.

## Blog Posts & Articles

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — Industry-standard security risks for LLM apps, including prompt injection (LLM01) and insecure tool use.
- [Simon Willison — Prompt Injection Explained](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/) — Foundational blog series on why prompt injection is fundamentally difficult to solve.
- [LangChain Human-in-the-Loop Guide](https://python.langchain.com/docs/how_to/tools_human/) — Community patterns for wrapping tools with `HumanApprovalCallbackHandler` for production HITL.
- [Principle of Least Privilege in Agentic AI](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic's guidance on scoping agent permissions to minimize blast radius.

## Research Papers

- [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) — Greshake et al. (2023). Seminal paper demonstrating indirect prompt injection attacks against LLM-integrated applications.
- [Prompt Injection attack against LLM-integrated Applications](https://arxiv.org/abs/2306.05499) — Liu et al. (2023). Systematic analysis of prompt injection attack vectors and defence mechanisms.

## Framework Documentation

- [LangChain Tool Calling](https://python.langchain.com/docs/concepts/tool_calling/) — How LangChain agents invoke tools, including schema validation and callback hooks.
- [AutoGen Conversable Agent](https://microsoft.github.io/autogen/docs/tutorial/conversable-agent/) — Tutorial on configuring multi-agent conversations with human proxy patterns.
