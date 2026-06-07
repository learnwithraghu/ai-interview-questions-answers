# Question 29: Pinning LLM Model Versions

**Question:** An AI Engineer deployed a RAG system and it functioned fine, but after 2 months it started giving bad results. No code change and no data change occurred. What could be the issue?

**Answer:**

### 1. Question Explanation
Alright, when an interviewer asks you this question, they are testing your real-world production experience. In a classroom or a weekend project, models feel static. In production, they are dynamic, moving targets. The interviewer is watching out for developers who think LLM APIs are immutable libraries. They want to see if you immediately suspect **model drift** caused by relying on generic model aliases (like `gpt-4o`) rather than pinning your code to a specific, dated snapshot (like `gpt-4o-2024-08-06`).

### 2. Concept Explanation
The root cause of a system suddenly degrading without code or data changes is almost always **API-side model updates** (often called model drift).

When you initialize an LLM client, you specify a model identifier:
```python
# The dangerous way
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    input="Explain Kubernetes in one paragraph"
)

print(response.output_text)
```
Here, `gpt-4o` is a **dynamic alias**, not a static model. It points to whatever OpenAI currently considers the default, stable version of GPT-4o. Every few months, providers update this pointer to a new snapshot (e.g., moving from `gpt-4o-2024-05-13` to `gpt-4o-2024-08-06`).

While these updates usually improve general benchmarks, they can introduce subtle changes that break production applications:
1. **Prompt Sensitivity:** LLMs are highly sensitive to prompt structure. A prompt optimized for one model version might perform poorly on the next version because of changes in instruction-following behaviors or safety training.
2. **Output Formatting:** If your application relies on parsing text output or specific JSON structures, a model update can alter the formatting, leading to parsing failures.
3. **Reasoning Paths:** The way the model reasons through complex or few-shot prompts changes. In a RAG system, this can degrade its ability to synthesize retrieved chunks or cause it to ignore system instructions it previously respected.

**The Solution: Pinning Model Versions**
To guarantee deterministic behavior, you must use **pinned, dated snapshot versions** in production:
```python
# The robust way
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-2024-08-06",  # Pinned to a specific, immutable snapshot
    input="Explain Kubernetes in one paragraph"
)

print(response.output_text)
```
Dated snapshots are immutable; the provider guarantees they will not change under the hood (though they will eventually be deprecated, typically after 12-18 months).

**How to safely upgrade:**
Treat an LLM version upgrade like upgrading a database version. Do not change it in production directly. Instead:
- Maintain a golden dataset of query-answer pairs.
- Run offline evaluations (using LLM-as-a-judge or traditional metrics) comparing the new snapshot against the current production model.
- Verify that accuracy, formatting, and latency meet your criteria before updating the model ID in your configuration.

### 3. Real-World Example
A company deployed a customer support bot using the alias `gpt-4o`. The bot was instructed to only answer questions using retrieved document snippets. It worked perfectly. Two months later, customers started complaining that the bot was making up answers (hallucinating) and ignoring the retrieval context.
The engineering team checked their logs and found no changes to their retrieval database or their code. However, they realized OpenAI had rolled out an update to the `gpt-4o` alias that morning. The new model version had slightly different prompt alignment, making it more eager to answer questions even when the retrieved context was empty.
The team immediately updated their code to use the specific dated version `gpt-4o-2024-05-13`. The bot's behavior reverted to normal. They then set up an evaluation pipeline to test the newer model snapshot (`gpt-4o-2024-08-06`) on a test set and tweak the prompt before upgrading.

### 4. This is how I would answer this
"If a production RAG system suddenly starts giving bad results with no code or data changes, the first thing I would check is whether we pinned our model versions. 

Using dynamic aliases like `gpt-4o` or `claude-3-5-sonnet` is a major risk because API providers periodically update these aliases to point to newer underlying snapshots. These updates can alter prompt alignment, change output formats, or cause regressions on specific tasks.

To prevent this, I always pin model calls to specific, immutable, dated snapshots in production, such as `gpt-4o-2024-08-06`. When we want to upgrade to a newer model version, we treat it as a database migration: we run the new model against a golden evaluation dataset to measure performance and tune our prompts before making the switch in production."
