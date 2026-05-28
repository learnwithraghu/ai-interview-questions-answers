# Question 2: Few-Shot vs Zero-Shot Prompting

**Question:** Explain the concept of few-shot prompting and how it differs from zero-shot prompting. Provide an example of when you would use it.

**Answer:**

### 1. Question Explanation
Alright, this one comes up constantly because it tests whether you actually understand how to **steer model behavior through examples**—not just through instructions. The interviewer wants to see that you know the difference between asking a model to figure something out cold versus showing it a pattern first. A major red flag is treating them as interchangeable, or saying "few-shot means I give it more context from a document." That's RAG, not few-shot. They also want a concrete example of *when* you'd reach for each technique, which tells them you've shipped prompts in production and not just read about them.

### 2. Concept Explanation
Every prompt you send to an LLM falls somewhere on a spectrum of how much **demonstration** you provide before asking it to perform the task.

**Zero-shot prompting** means you give the model a task description with **no worked examples**. You rely entirely on the model's pre-trained knowledge and your instruction clarity. For example: "Classify this customer review as Positive, Negative, or Neutral." The model has to infer the format, tone, and decision boundaries purely from your words. Zero-shot works well when the task is common, the output format is simple, and the model has likely seen similar tasks during training—things like summarization, translation, or basic classification.

**Few-shot prompting** means you include **one or more input-output examples** in the prompt before the actual task. You're essentially saying: "Here's what good looks like—now do the same for this new input." For example, you might show two labeled reviews and then ask the model to classify a third. The examples teach the model your specific format, edge-case handling, and domain vocabulary without changing any model weights.

The key distinction is **demonstration vs. instruction alone**. Few-shot doesn't mean "more text" or "more retrieved documents"—those examples must be **paired demonstrations of the exact task** you want performed. The model learns the pattern in-context during inference; nothing is fine-tuned.

When should you use few-shot? Reach for it when zero-shot output is inconsistent—maybe your labels are domain-specific, your output format is unusual, or you need the model to follow a nuanced style guide. A classic production use case is **structured extraction** where showing two examples of messy input mapped to clean JSON dramatically improves accuracy. Stick with zero-shot when the task is straightforward and examples would just burn tokens without adding value.

One practical caveat: few-shot examples consume context window tokens on every request, so in high-volume production systems you need to be deliberate about how many examples you include—usually 2–5 is the sweet spot before diminishing returns kick in.

### 3. Real-World Example
An e-commerce company wants an LLM to categorize product return reasons into a fixed taxonomy like `Defective`, `Wrong Item`, `Changed Mind`, or `Not as Described`. Zero-shot alone often mislabels edge cases like "the colour looked different on my screen" as `Defective`. By adding three few-shot examples in the system prompt—each showing a raw customer message and the correct label—the team gets consistent classification without fine-tuning, and they can update the taxonomy just by swapping examples.

### 4. This is how I would answer this
"Zero-shot means I describe the task with no examples—the model relies purely on instructions. Few-shot means I include a few input-output pairs in the prompt to show the model exactly what pattern to follow. In my experience, I use zero-shot for straightforward tasks like summarization, and I switch to few-shot when I need consistent formatting or domain-specific classification—like showing two examples of customer emails mapped to sentiment labels before asking it to classify a new one."
