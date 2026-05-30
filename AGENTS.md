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

## Project structure

- `questions.md` — interview question bank
- `udemy_question_heading.md` — 4–5 word Udemy video titles
- `answers/` — four-part answer files per question
- `answers/**/html-learning/` — standalone visual HTML learning pages generated from answer files
- `.agent/` — detailed agent skills and SOPs
