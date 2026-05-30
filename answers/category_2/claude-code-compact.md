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

### 4. How Other Tools Handle This Problem

Claude Code's `/compact` is one solution, but every major AI coding assistant runs into the same finite-context constraint and solves it differently. Understanding these approaches helps you answer follow-up questions and shows you're thinking about the problem at the platform level, not just the Claude level.

**GitHub Copilot (VS Code / JetBrains)**
Copilot doesn't maintain a persistent session history the way Claude Code does. Each inline suggestion or Copilot Chat turn is a short, isolated context window built on the fly: the current file, a sliding window of surrounding lines, and a small set of "retrieved" snippets from other open files (via its workspace indexing). There is no concept of compaction because there's no long-running session to compress. The trade-off: it never gets "confused" by a long session, but it also has no memory of decisions made five minutes ago unless you manually re-state them in the chat.

**Cursor (AI-native IDE)**
Cursor uses a system it calls **"Notepads"** and **rules files** (`cursor_rules` / `.cursorrules`) to persist context across sessions — similar in spirit to Claude Code's CLAUDE.md. For in-session context, Cursor's `Composer` (its multi-file agent) dynamically selects which files to include in the prompt using a retrieval step, rather than letting history grow unboundedly. When the agent needs to reason across many files, it picks the most relevant ones rather than cramming everything in. This is a retrieval-based approach vs. Claude Code's summarisation-based approach. Cursor also lets users pin specific files or ranges to the context manually.

**Aider (open-source CLI)**
Aider is probably the closest conceptual cousin to Claude Code. It keeps a running `/chat-history` and exposes explicit context management commands. Its equivalent of `/compact` is a combination of `/drop` (remove specific files from the context) and the `--no-dirty-commits` and `--map-tokens` flags, which control how much of the repository map (a summary of all files and symbols) is included each turn. Aider also has a `--compress` flag that condenses prior messages. The key difference: Aider gives you fine-grained control over what goes in and out, while Claude Code's `/compact` is a higher-level "summarise everything and move on" action.

**Windsurf (Codeium)**
Windsurf's `Cascade` agent uses a concept it calls **"persistent memory"** across sessions — it can remember facts about a project (e.g., "we're using PostgreSQL, not SQLite") between separate sessions, not just within one. For within-session context overflow, it uses a sliding window approach that prioritises the most recent turns and the most recently edited files, and silently drops older exchanges. This is the most invisible approach — you don't trigger anything manually; the tool just decides what to keep. The downside is you lose visibility into what was dropped.

**The Core Trade-off Across All Tools**

| Tool | Approach | User Control | Risk |
|---|---|---|---|
| Claude Code `/compact` | LLM-generated summary | High (manual trigger, inspect via Ctrl+O) | Summary may drop edge-case details |
| Copilot Chat | No persistent session | N/A | No cross-turn memory |
| Cursor Composer | Retrieval-based file selection | Medium (pin files manually) | Relevant files may not be retrieved |
| Aider | Drop commands + repo map | High (explicit per-file control) | More manual overhead |
| Windsurf Cascade | Silent sliding window + persistent memory | Low | Opaque about what was dropped |

The pattern: tools built around an agent loop (Claude Code, Aider, Cursor Composer) need an explicit strategy because the loop accumulates state. Tools built around single-turn completions (classic Copilot) sidestep the problem by never accumulating state in the first place — at the cost of session-level continuity.

### 5. This is how I would answer this

"When a long session starts degrading, I use `/compact`. It compresses the full conversation into a structured summary — key decisions, edited files, open tasks — and injects that as a fresh context window. I use it proactively before starting a new major subtask rather than waiting for the hard stop. For durable things like architecture rules, I keep those in CLAUDE.md. `/compact` is for the session trail — the exploration and back-and-forth that's useful now but just noise later."
