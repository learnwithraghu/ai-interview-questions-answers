# Handoff — Excalidraw Diagrams Session

**Date:** 2026-05-30  
**Status:** All category_2 diagrams created. Committed locally, NOT yet pushed to GitHub.

---

## What Was Done This Session

### 1. Color palette updated (Matt Pocock-inspired)
File: `.agent/excalidraw-diagram-skill/references/color-palette.md`

The palette was changed from a blue-dominant scheme to a **violet-primary** palette:
- Primary/Hero: `#7c3aed` stroke on `#ede9fe` fill
- AI/LLM: `#6d28d9` stroke on `#f5f3ff` fill
- Success: `#059669` stroke on `#d1fae5` fill
- Error: `#e11d48` stroke on `#ffe4e6` fill
- Warm accent: `#b45309` stroke on `#fef3c7` fill
- Title text: `#4c1d95` — Subtitle: `#7c3aed` — Body: `#475569`

### 2. Project skill file created
File: `.agent/excalidraw-course-diagrams.md`

Project-specific wrapper around the base excalidraw skill. Contains:
- Output path conventions (answers/category_N/<slug>.excalidraw)
- Per-concept design notes for RAG, tool calling, JSON, /compact
- Render command path for this project
- Category 2 diagram checklist

### 3. AGENTS.md updated
Added rule #6: agents must read `.agent/excalidraw-course-diagrams.md` before creating/editing `.excalidraw` files.

### 4. All 8 category_2 diagrams created

| File | Concept | Visual Pattern |
|------|---------|----------------|
| `rag-systems-fail.excalidraw` | RAG = two independent failure systems | Two side-by-side rooms with boundary |
| `debugging-rag-retrieval.excalidraw` | Debug RAG by isolating failure side | Decision tree (log chunks → diamond → fixes) |
| `natural-language-to.excalidraw` | Text-to-SQL with schema injection | Assembly line pipeline |
| `designing-safe-llm.excalidraw` | Tool routing with HITL gate | Fan-out from LLM router, red diamond gate |
| `advanced-rag-retrieval.excalidraw` | 4 retrieval strategies | 2×2 grid of mini-patterns |
| `automated-llm-evaluation.excalidraw` | LLM-as-a-judge evaluation | Pipeline + comparison + decision diamond |
| `extracting-valid-json.excalidraw` | 5-layer JSON defence | Stacked layers (thickest = strongest) |
| `claude-code-compact.excalidraw` | /compact session management | Before/after split + CLAUDE.md vs /compact |

---

## What Needs To Be Done Next

### Immediate (tomorrow morning)
1. **Push to GitHub** — 2 local commits are ready but not pushed:
   ```bash
   git push origin main
   ```
   This will push both commits (the diagrams + the skill-as-regular-files fix).

2. **Verify diagrams render correctly in Excalidraw** — Open a few `.excalidraw` files in [excalidraw.com](https://excalidraw.com) to confirm they look right. The render script needs network access (loads from esm.sh) so wasn't used for validation — use the web app instead.

### Optional follow-up work
- **Category 3 diagrams** — same pattern, create one per concept in `answers/category_3/`
- **Category 4 diagrams** — same pattern for `answers/category_4/`
- **Fix render script** — The playwright renderer times out because it loads `@excalidraw/excalidraw` from `esm.sh` (requires internet). Options:
  - Bundle excalidraw locally in `render_template.html`
  - Or just use the web app for validation

---

## Git State

```
Branch: main
Local commits not pushed: 2

Commit 1 (34671b5): Add category_2 Excalidraw diagrams + violet-primary skill setup
  - 8 .excalidraw files created
  - color-palette.md updated
  - excalidraw-course-diagrams.md created
  - AGENTS.md updated
  - .gitignore added

Commit 2 (staged, not yet committed): Fix excalidraw-diagram-skill as regular files
  - Removed embedded .git from skill directory
  - Re-added all skill files as normal tracked files
```

The staged changes (commit 2) still need to be committed before pushing.

---

## Key Files Reference

```
.agent/
  excalidraw-course-diagrams.md       <- PROJECT skill (read this first for diagrams)
  excalidraw-diagram-skill/
    SKILL.md                          <- Base design methodology
    references/
      color-palette.md                <- VIOLET-PRIMARY palette (Matt Pocock style)
      element-templates.md            <- JSON copy-paste templates
      render_excalidraw.py            <- Renderer (needs network to work)

answers/category_2/
  *.excalidraw                        <- 8 diagrams created this session
```
