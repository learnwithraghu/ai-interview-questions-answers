# References: Filtering Hallucinated Citations in Production

Curated resources for deeper study on hallucination detection, citation verification, and grounding techniques.

---

## Official Documentation

- [Azure AI Content Safety — Groundedness Detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness) — Managed API that checks if LLM outputs are grounded in provided source documents, returning per-sentence confidence scores.
- [AWS Bedrock Guardrails — Grounding Check](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) — Amazon's inline grounding check that compares model outputs against the provided context, integrated directly into the Bedrock inference pipeline.
- [Perplexity AI — How It Works](https://www.perplexity.ai/hub/about) — Citations-first architecture where every claim is hyperlinked to a retrieved source before generation.

## Provider & Cloud Docs

- [Guardrails AI Documentation](https://www.guardrailsai.com/docs) — Open-source Python library with composable validators including `ValidURL` (HTTP HEAD checks) and `FactuallyConsistentSummary` (NLI-based consistency).
- [Guardrails AI — ValidURL Validator](https://hub.guardrailsai.com/validator/guardrails/valid_url) — Fires HTTP HEAD requests on every extracted URL and flags non-200 responses as hallucinated.
- [Vectara HHEM (Hughes Hallucination Evaluation Model)](https://huggingface.co/vectara/hallucination_evaluation_model) — Open-source NLI-based hallucination detection model, available on Hugging Face.

## Blog Posts & Articles

- [Anthropic — Reducing Hallucination in AI](https://www.anthropic.com/news/reducing-ai-generated-hallucinations-with-citations) — Anthropic's technical approach to reducing hallucinated content through citation-aware generation.
- [LLM-as-a-Judge: A Practical Guide](https://eugeneyan.com/writing/llm-as-judge/) — Eugene Yan's guide on using secondary LLMs to fact-check and evaluate primary LLM outputs.
- [Microsoft Copilot Citation Architecture](https://blogs.microsoft.com/blog/2023/09/21/announcing-microsoft-copilot-your-everyday-ai-companion/) — How Copilot embeds citations during constrained decoding rather than adding them as an afterthought.
- [Natural Language Inference for Fact Checking](https://huggingface.co/tasks/text-classification) — Hugging Face overview of NLI models and how to use them for entailment checking against source passages.

## Research Papers

- [FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation](https://arxiv.org/abs/2305.14251) — Min et al. (2023). Breaks LLM outputs into atomic facts and verifies each against a knowledge source.
- [SAFE: Search-Augmented Factuality Evaluator](https://arxiv.org/abs/2403.18802) — Wei et al. (2024). Google DeepMind's approach to automated factuality evaluation using search-augmented verification.
- [A Survey on Hallucination in Large Language Models](https://arxiv.org/abs/2311.05232) — Huang et al. (2023). Comprehensive survey of hallucination types, detection methods, and mitigation strategies.

## Framework Documentation

- [LangChain — Output Parsers & Validators](https://python.langchain.com/docs/concepts/output_parsers/) — Patterns for structured output parsing and post-generation validation in LangChain pipelines.
- [LlamaIndex — Response Evaluator](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/) — Built-in evaluation modules for faithfulness and relevancy checking of RAG responses.
