---
name: excalidraw-course-diagrams
description: Create Excalidraw concept diagrams for the AI Engineer Interview Bootcamp. Use when generating visual .excalidraw files for course concepts. Wraps the base excalidraw-diagram skill with project-specific conventions.
---

# AI Interview Bootcamp — Excalidraw Diagram Skill

Generates `.excalidraw` files for each concept in the course. One diagram per answer file. Each diagram should be a **visual argument** — not a slide with boxes.

Rendered `.png` exports should live beside the `.excalidraw` source inside the same `visuals/` folder.

## Base Skill

All design methodology, JSON structure, visual patterns, and render/validate workflow live in:

```
.agent/excalidraw-diagram-skill/SKILL.md
```

Read that file in full before generating any diagram. This file adds project-specific rules on top of it.

---

## Color Palette

All colors come from:

```
.agent/excalidraw-diagram-skill/references/color-palette.md
```

The palette is **violet-primary** (Matt Pocock-inspired):
- Hero/primary elements: violet `#7c3aed` stroke on `#ede9fe` fill
- AI/LLM elements: deep purple `#6d28d9` stroke on `#f5f3ff` fill  
- Success/output: emerald `#059669` on `#d1fae5`
- Warning/error: rose `#e11d48` on `#ffe4e6`
- Warm accent (decisions, caveats): amber `#b45309` on `#fef3c7`
- Structural lines and marker dots: violet `#7c3aed`
- Title text: `#4c1d95` — subtitle: `#7c3aed` — body: `#475569`

---

## Output Conventions

| Category | Output directory | Naming |
|----------|-----------------|--------|
| category_2 | `answers/category_2/visuals/` | `qNN-<answer-slug>.excalidraw` |
| category_3 | `answers/category_3/visuals/` | `qNN-<answer-slug>.excalidraw` |
| category_4 | `answers/category_4/visuals/` | `qNN-<answer-slug>.excalidraw` |

The answer slug is the filename of the matching `.md` file (without `.md`), which starts with `q` followed by the zero-padded question number. Example: `answers/category_2/visuals/q12-advanced-rag-retrieval.excalidraw`.

---

## Icons for Provider/Tool Comparisons

Several category_3/category_4 concepts name specific real products (OpenAI, Anthropic, Groq, vLLM, Ollama, Together AI, etc.) rather than generic roles. For those, use the real brand icon per the base skill's "Real Icons for Named Tools/Providers" section — `fetch_icon.py` checks the repo's `references/icons/` cache first and only fetches from Lobe Icons on a genuine miss. Still cap at one icon per box, and only for diagrams that genuinely compare/name specific tools — not as decoration on generic process boxes.

## Render Command

```bash
cd .agent/excalidraw-diagram-skill/references && uv run python render_excalidraw.py <absolute-path-to-file.excalidraw>
```

Run from the project root (the directory containing `answers/`). Always render after writing and fix issues in a loop until the diagram looks right.

---

## Per-Concept Design Notes

Each concept has a natural visual pattern. Match the pattern to the concept's core mechanism.

### RAG & Retrieval Concepts
- **Two-system diagrams** (retrieval + generation): Use two clear side-by-side "rooms" with a visible boundary. The boundary is the key insight — log what crosses it.
- **Pipeline concepts** (RAG retrieval, text-to-SQL): Use assembly-line flow, left-to-right. Each stage is a distinct shape. Include evidence artifacts (real query examples, schema snippets).
- **Advanced retrieval techniques**: Each technique gets its own visual mini-pattern (fan-out for decomposition, funnel for re-ranking, parallel streams for hybrid search).

### LLM Output & Validation
- **Structured output layers**: Use depth/stacking to show defence-in-depth. The thickest/most prominent layer is the API-level guarantee.
- **Evaluation pipelines**: Assembly line. Show actual metric names (Factual Accuracy, Conciseness, Relevance) — not generic "Score".

### Tool Calling & Agents
- **Tool routing architectures**: Fan-out from the LLM router. Use a red HITL gate diamond for irreversible actions. Green for safe read-only paths.

### Claude Code Features
- **Session management**: Use a before/after split (Problem → Tool → Result). Timeline patterns for showing turn accumulation. Show real numbers (50,000 tokens → 5,000).

---

## Category 2 Diagram Checklist

| Answer file | Diagram | Status |
|------------|---------|--------|
| q07-extracting-valid-json.md | 5-layer defence-in-depth | |
| q08-rag-systems-fail.md | Two independent failure systems | |
| q09-claude-code-compact.md | Before/after session flow | |
| q10-natural-language-to.md | Text-to-SQL pipeline | |
| q11-tool-calling-flow.md | Tool calling flow under the hood | |
| q12-advanced-rag-retrieval.md | 4 retrieval technique mini-patterns | |
| q13-automated-llm-evaluation.md | LLM-as-a-judge evaluation pipeline | |
