# AI Engineer Interview Bootcamp

This repository contains interview questions, answers, and course curriculum for the AI Engineer Interview Bootcamp.

## For AI coding agents

When editing course content in this repo, follow these rules:

1. Read `.agent/course_content_management.md` before adding or changing questions, answers, or lecture titles.
2. Keep these files in sync whenever `questions.md` changes:
   - `questions.md`
   - `udemy_question_heading.md`
   - `README.md` (Course Curriculum section)
   - `answers/category_<section>/<first-three-udemy-heading-words>.md`
3. Use the instructor persona defined in the agent skill (Matt Pocock clarity + Andrej Karpathy first-principles teaching).
4. Read `.agent/whiteboard_ui_skill.md` before creating or changing visual HTML learning pages under `answers/**/html-learning/`.
5. HTML learning pages must be visual-first, responsive on every screen size, and derived only from the matching answer file in `answers/`.
6. Read `.agent/excalidraw-course-diagrams.md` before creating or editing `.excalidraw` diagram files. That skill wraps `.agent/excalidraw-diagram-skill/SKILL.md` with project-specific output paths, naming conventions, and the violet-primary color palette. Always render and visually validate diagrams using the render script before marking a diagram complete.

## Project structure

- `questions.md` — interview question bank
- `udemy_question_heading.md` — 4–5 word Udemy video titles
- `answers/` — four-part answer files per question
- `answers/**/*.excalidraw` — visual concept diagrams (one per answer) using the violet-primary palette
- `answers/**/html-learning/` — standalone visual HTML learning pages generated from answer files
- `.agent/` — detailed agent skills and SOPs
  - `course_content_management.md` — rules for question/answer authoring
  - `whiteboard_ui_skill.md` — rules for HTML learning pages
  - `excalidraw-course-diagrams.md` — rules for `.excalidraw` concept diagrams
  - `excalidraw-diagram-skill/` — base excalidraw skill (design methodology + render pipeline)
