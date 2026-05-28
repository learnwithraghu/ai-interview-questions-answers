# Question 4: Purpose Of AGENTS.md In Repos

**Question:** What is the purpose of `AGENTS.md` in a GitHub repository?

**Answer:**

### 1. Question Explanation
Alright, this one is showing up more and more as teams actually ship with AI coding agents—not just paste into ChatGPT once and hope for the best. The interviewer wants to know if you understand **repo-level context**: how you make an AI assistant behave consistently inside *your* codebase, follow your conventions, and not re-discover the same rules every session. A red flag is confusing `AGENTS.md` with a random README, or saying "I'd just put instructions in the chat each time."

### 2. Concept Explanation
Here's the problem first. When you open Cursor, Copilot, or Claude Code on a repo, the model knows general programming—but it doesn't know *your* project. How are answers formatted? Which files must stay in sync? What stack and tone do you use? Without durable instructions, every new chat is a blank slate. You end up re-prompting the same rules, and the agent drifts.

**`AGENTS.md`** is a simple, open convention—a markdown file at the **root of your repository** that tells AI coding agents how to work in that project. Think of it as **onboarding docs for AI**, the same way `CONTRIBUTING.md` onboards human contributors. It's not executable code; it's instructions the agent reads before editing.

The format is intentionally lightweight. There's a community effort around [agentsmd/agents.md](https://github.com/agentsmd/agents.md) to standardize it across tools, and many editors now support it natively or via symlinks—GitHub Copilot, Cursor, Claude Code, and others can treat it as the canonical "here's how we build in this repo" file.

What goes inside? Typically: project overview, coding conventions, how to run tests, file structure, things the agent must always do, and things it must never do. Some teams use it as a **router**—a short file that points the agent to deeper docs only when needed (e.g., "For course content workflows, see `.agent/course_content_management.md`"). That keeps the main file slim and avoids context bloat.

The value is **consistency and repeatability**. Rules live in git—reviewable in PRs, shared across the team, updated once and applied forever. When you change `AGENTS.md`, every future agent session inherits the new standard. You're doing **prompt engineering at the repository level**: turning fragile one-off chat instructions into durable system context that ships with the code.

Here's the part that trips people up: `AGENTS.md` is not a replacement for tool-specific config. You might still have `.cursor/rules/`, `.cursor/skills/`, or a `.agent/` folder for modular workflows. `AGENTS.md` is usually the **entry point**—the first file an agent reads. Tool-specific folders handle specialized skills. They work together, not instead of each other.

### 3. Real-World Example
This bootcamp repo includes an `AGENTS.md` at the root that tells any coding agent the high-level project purpose and points to `.agent/course_content_management.md` for the detailed workflow—how to write four-part answers, sync `udemy_question_heading.md`, and match the course teaching voice. A contributor asks Cursor to "add Question 27." The agent reads `AGENTS.md` first, follows the link to the skill file, and produces content that matches the rest of the course instead of inventing a new format.

### 4. This is how I would answer this
"`AGENTS.md` is a markdown file at the repo root that gives AI coding agents durable project context—conventions, structure, and rules they should follow. In my experience, the value is consistency: instead of re-explaining how we work in every chat, we version-control those instructions alongside the code. Tools like Copilot and Cursor can read it automatically, and teams often use it as a router to deeper skill files when the project needs more detail."
