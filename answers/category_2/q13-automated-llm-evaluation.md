# Question 13: LLM-as-a-Judge Evaluation

**Question:** You are evaluating two different LLMs for a summarization task. One is cheaper but potentially less accurate. How do you set up an automated evaluation pipeline (e.g., using LLM-as-a-judge) to quantify the trade-off at scale?

**Answer:**

### 1. Question Explanation
Listen up folks, this is a data-driven decision-making question. The interviewer wants to know if you can build a systematic, repeatable evaluation framework—not just eyeball a few outputs and pick a winner. They want to verify you understand that in production, you need quantified metrics you can defend to stakeholders. A red flag is if you suggest only using human evaluation—that doesn't scale. They are looking for you to describe a concrete pipeline: a benchmark dataset, automated scoring using an LLM-as-a-judge, quantitative metrics, and a cost-per-quality analysis.

### 2. Concept Explanation
Before LLM-as-a-judge existed, evaluating LLM outputs at scale meant either: (a) manually reading hundreds of outputs—which doesn't scale, or (b) using metrics like ROUGE or BLEU scores—which measure word overlap but say nothing about whether the output is actually *good*. A summary can have high ROUGE overlap with a reference while still being factually wrong or incoherent. We needed something smarter.

**The LLM-as-a-judge pattern** solves this by using a powerful, trusted LLM (typically GPT-4o) to evaluate the outputs of the models you're testing. You feed it a structured prompt: "Here is the original document. Here is a summary. Rate this summary on a scale of 1-5 for Factual Accuracy, Conciseness, and Relevance. Return a JSON object with these scores and a brief justification." Then you run this across your entire benchmark dataset automatically.

**Building the benchmark dataset:** The foundation of any good evaluation is a "golden dataset." This is a curated set of 100–500 representative inputs—chosen to reflect the actual distribution of inputs you'll see in production—paired with either human-written reference outputs or human quality labels. The quality of your evaluation is directly limited by the quality of this dataset. Garbage in, garbage out.

**Calculating the trade-off:** Once you have scores for both models across the benchmark, you calculate average scores per dimension and compare them side by side with cost. Cost should be measured as cost-per-1000-API-calls (input tokens + output tokens), not just the listed price per token, since summarization tasks tend to have predictable input/output ratios.

The key decision is defining your **acceptance threshold** before you look at the results—not after. Something like: "If the cheaper model scores within 10% of the expensive model on Factual Accuracy, we'll use it for the majority of tasks." This prevents you from unconsciously adjusting the threshold to fit a preferred outcome.

**Caveats:** LLM-as-a-judge has known biases—judge models tend to prefer longer, more detailed responses and can favour outputs from models similar to themselves. Mitigate this by using a judge model from a *different* provider than the models you're evaluating, and by randomising the order of outputs presented to the judge.

### 3. Real-World Example
A media company needs to summarize 50,000 news articles per day. They evaluate GPT-4o vs. Gemini Flash on a 300-article benchmark. Their LLM-as-a-judge scores both on conciseness, accuracy, and readability. Gemini Flash scores 4.1/5 on accuracy versus GPT-4o's 4.4/5, but at 1/10th the cost. For non-breaking-news summaries, they deploy Gemini Flash and reserve GPT-4o only for high-stakes editorial content, cutting their daily LLM bill by 80%.

### 4. This is how I would answer this
"I'd build a benchmark dataset of representative inputs with human-written reference summaries. Then I'd run both models across the entire benchmark and use a powerful LLM like GPT-4o as the judge—scoring each output on dimensions like factual accuracy, conciseness, and relevance using a structured rubric. That gives me quantitative scores I can compare side by side with the cost per 1000 calls. The decision then becomes: if the cheaper model scores within an acceptable threshold on the most critical metric—usually factual accuracy—the cost savings justify using it, potentially with the expensive model as a fallback for edge cases."
