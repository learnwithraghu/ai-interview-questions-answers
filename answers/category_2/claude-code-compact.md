# Question 9: /compact in Claude Code

**Question:** You are an hour into a complex debugging session with Claude Code — many files edited, lots of back-and-forth. Responses are getting less focused and you're approaching the context window limit. How do you keep the session going without losing your work or starting over?

**Answer:**

### 1. Question Explanation

Alright, when an interviewer asks you this, what they're really testing is whether you understand the practical limits of working with LLMs in long sessions — and whether you know the tools available to manage those limits gracefully. Context windows are finite. A senior AI engineer knows this isn't a dead-end; it's an engineering constraint with a clear solution. The red flag they're watching for is someone who says "I'd just start a new chat" — that's losing all your session context for no reason.

### 2. Concept Explanation

Every conversation with an LLM is stateless under the hood. Claude Code holds your session history as a growing list of messages that gets passed into the model on every turn. As that list grows, two things happen: you consume more of the finite context window, and the model's attention gets diluted across an increasingly noisy transcript full of exploratory back-and-forth, repeated context, and dead ends.

The `/compact` command solves this cleanly. When you run it, Claude Code takes the entire conversation history and generates a structured summary — capturing the key decisions made, which files were edited and why, any open tasks or constraints you stated, and the current goal. That summary then replaces the full history as the new starting context for the session.

The result: a fresh, lean context window that still knows everything that matters. A 50,000-token session can compress down to under 5,000 tokens, which means you can keep working for far longer without hitting the hard limit.

There are two ways to trigger it. **Manual**: you run `/compact` yourself, proactively, before responses start degrading — ideally before starting a new major subtask so Claude gets a clean brief. **Automatic**: Claude Code can trigger compaction on its own when it detects the context window is nearly full. The auto mode is a safety net; the manual mode gives you control over timing and intent.

A useful pairing: **CLAUDE.md** handles the durable, session-independent facts — architecture rules, preferences, project conventions. `/compact` handles the ephemeral session trail. Don't conflate the two. After compaction, use `Ctrl+O` to inspect the generated summary and verify nothing critical was silently dropped before continuing.

### 3. Real-World Example

Imagine you're using Claude Code to refactor a complex authentication module. You've explored three different approaches over 45 minutes, settled on one, edited six files, and had a long exchange about edge cases. Responses are now noticeably less precise — Claude is referencing the discarded approaches as if they're still live options.

You run `/compact`. Claude Code summarises: the chosen auth approach, the six files modified and the reason for each change, the two edge cases flagged, and the next open task (updating the test suite). The old exploratory noise is gone. You continue with a sharp, focused model that has everything it needs and nothing it doesn't.

### 4. This is how I would answer this

"When a long session starts degrading, I use `/compact`. It compresses the full conversation into a structured summary — key decisions, edited files, open tasks — and injects that as a fresh context window. I use it proactively before starting a new major subtask rather than waiting for the hard stop. For durable things like architecture rules, I keep those in CLAUDE.md. `/compact` is for the session trail — the exploration and back-and-forth that's useful now but just noise later."
