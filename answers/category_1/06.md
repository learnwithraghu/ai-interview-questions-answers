# Question 6: Hallucinations In AI Coding Workflows

**Question:** In your AI coding experience, what is an example of an LLM hallucination you saw, and why do you think it happened?

**Answer:**

### 1. Question Explanation
Alright, this is a very practical question. The interviewer is not asking you to fix the hallucination yet. They are trying to find out whether you have actually used AI coding tools enough to notice when they are confidently wrong. A strong answer should describe a real coding hallucination, explain what made it wrong, and then reason about why it happened. A red flag is giving a generic definition of hallucination without tying it to code, context, APIs, files, or documentation.

### 2. Concept Explanation
An **LLM hallucination** is when the model produces something that looks plausible but is not actually true. In normal chat, that might be a fake citation or a made-up historical fact. In AI coding, it usually looks more specific: a fake method name, a library API that does not exist, a file path that is not in the repo, a config option from an older version, or a confident explanation of code it has not really inspected.

The key thing to understand is that an LLM is not checking truth by default. It is predicting the next likely token based on the prompt, its training data, and any context you give it. That means it can be very good at producing code-shaped answers even when it is missing the grounding needed to be correct.

In coding workflows, hallucinations usually happen for a few common reasons.

First, the model may not have enough **repo context**. If it has not read the actual file structure, type definitions, helper functions, or local conventions, it may invent a function that sounds like it should exist.

Second, it may rely on **stale or mixed training knowledge**. Many frameworks change quickly. The model might suggest an API from an older version of LangChain, Next.js, OpenAI, or a Python package because that pattern appeared frequently in its training data.

Third, the prompt may be **underspecified**. If you ask "add auth" without saying which auth library, which version, which storage layer, and what constraints exist, the model has to fill in the blanks. Sometimes those guesses are useful. Sometimes they become hallucinations.

So the important interview skill is diagnosis. You want to show that you can separate "the model made a syntax mistake" from "the model invented a false fact about the system." That distinction matters because hallucination is usually a grounding problem, not just a coding typo.

### 3. Real-World Example
Suppose you are using an AI coding assistant in a Python project and ask it to load environment variables before calling an API. The assistant writes code like this:

```python
from dotenv import load_env

load_env()
```

At a glance, this looks totally believable. But the real function from `python-dotenv` is `load_dotenv()`, not `load_env()`. The model hallucinated a function name that sounds natural because many Python libraries use short helper names like that.

The bug is not that the model failed to understand Python syntax. The bug is that it acted as if a specific API existed without checking the actual library documentation or installed package. The likely cause is stale or pattern-based knowledge: it generated something that looked like common Python code, but it was not grounded in the real dependency.

### 4. This is how I would answer this
"Yes. One common example I have seen is an AI coding assistant inventing a helper function or library method that looked completely reasonable but did not exist in the actual repo. I think it happened because the model was pattern-matching from common codebases without enough local context. It produced something that was syntactically plausible, but it was not grounded in the real files, dependency versions, or available APIs."
