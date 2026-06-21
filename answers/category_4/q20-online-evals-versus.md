# Question 20: Online Evals Versus Offline Evals

**Question:** What is the difference between offline evals and online evals for an LLM-powered feature? When in the development lifecycle would you use each?

**Answer:**

### 1. Question Explanation
This question checks whether you think about evaluation as a continuous process rather than a one-time pre-launch checklist. Interviewers want to see that you understand evals have to run at different points in the lifecycle — before a model or prompt change ships, and after it's live — and that you know what each stage can and can't catch. A weak answer treats "eval" as a single static test suite; a strong answer distinguishes the controlled, repeatable nature of offline evals from the noisy, real-traffic nature of online evals, and explains why neither alone is sufficient.

### 2. Concept Explanation
**Offline evals** run against a fixed, curated dataset — golden examples, regression cases, adversarial prompts — before code ships. Because the dataset and scoring method are fixed, results are reproducible: you can run the same suite against a new prompt or model version and get a clean before/after comparison. Offline evals are good at catching known failure modes (a regression on a case you've seen before) but blind to failure modes you haven't anticipated, since the dataset is necessarily a sample of imagined or historical inputs, not live traffic.

**Online evals** run against real production traffic, after the change has shipped. This includes things like sampled human review of live outputs, implicit signals (thumbs up/down, edit rate, regeneration rate, session abandonment), LLM-as-judge scoring on a rolling sample of real requests, and A/B tests comparing two prompt/model variants on actual users. Online evals catch the failure modes offline data can't represent — distribution shift, edge cases real users produce that your golden set never imagined, and regressions that only appear under production load or latency conditions. The cost is that online evals are noisier (confounded by traffic mix, seasonality, user behavior) and the feedback loop is slower and riskier, since by definition some real users saw the bad output before you caught it.

The two are complementary, not substitutes:
* **Offline evals gate the release** — they're the CI check that blocks a regression before it reaches users.
* **Online evals monitor the release** — they're the production alarm that catches what the offline suite missed.
* A common failure pattern is teams that only do offline evals (so they ship confidently but get blindsided by real-world drift) or only do online evals (so they catch regressions, but only after users were already affected, and have no fast feedback loop for iteration).

### 3. Real-World Example
A team building an AI customer-support agent maintains an offline regression suite of 200 curated tickets (refund requests, angry customers, ambiguous product questions) that runs in CI on every prompt change — if a new prompt drops accuracy on the "angry customer de-escalation" subset, the PR is blocked. Once a change passes offline and ships, the team routes 5% of live traffic through an LLM-as-judge that scores tone and resolution quality, and tracks the human-escalation rate as an implicit signal. When the escalation rate spikes a week after a prompt update, it's the online eval — not the offline suite, which had no escalation-rate signal — that surfaces the regression, prompting the team to add the failing case back into the offline golden set so it's caught earlier next time.

### 4. This is how I would answer this
"Offline evals are a fixed, repeatable test suite I run pre-deploy to gate releases — they catch known regressions quickly and cheaply. Online evals run on live traffic post-deploy — sampled judge scoring, A/B tests, implicit user signals — and catch what the offline dataset couldn't anticipate, like real-world distribution shift. I treat them as a loop: online evals surface new failure modes, and I backfill those cases into the offline suite so the same issue is caught automatically next time, before it ever reaches users again."
