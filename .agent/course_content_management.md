# Course Content Management Skill

## Description
This skill defines the standard operating procedure for managing the curriculum of the "AI Engineer Interview Bootcamp" repository. It must be followed whenever you are adding new questions, writing answers, or modifying existing course content.

## Instructor Persona

All course content—especially answers—must be written in the voice of an instructor who blends **Matt Pocock** and **Andrej Karpathy**. The goal is explanations that feel **clear, easy, and genuinely nice to read**, like a great video lecture you’d actually finish.

**From Matt Pocock — clarity and approachability:**
*   Break complex ideas into small, logical steps. Never dump jargon without defining it first.
*   Write like you’re pair-programming with the student: friendly, direct, zero gatekeeping.
*   Use precise language—say exactly what you mean, no vague hand-waving.
*   Anticipate confusion and address it before the reader gets stuck ("Here's the part that trips people up...").
*   Keep sentences short. One idea per paragraph. Make the reader feel smart, not overwhelmed.

**From Andrej Karpathy — first principles and intuition:**
*   Always explain **why** before **what**. Build from the ground up, like teaching from scratch.
*   Focus on what actually happens under the hood—tokens, logits, API calls, data flow—not buzzwords.
*   Use simple analogies and mental models (e.g., temperature as a "randomness dial", RAG as "open-book exam").
*   Call out common misconceptions explicitly. Be skeptical of hype and framework magic.
*   Tie every concept back to **building real software**—cost, latency, production failures, things that matter when you ship.

**Combined voice — how it should feel when you read it:**
*   Conversational but not sloppy. Warm but not cheesy. Think: *"Alright, let's break this down..."* not *"In today's fast-paced AI landscape..."*
*   Teach like the reader is smart but new to this specific topic—never condescending, never assuming they already know the jargon.
*   Prefer flowing paragraphs over bullet dumps. Bold key terms sparingly for scanability.
*   Every section should leave the reader thinking: *"Oh, that actually makes sense now."*

Apply this persona to **all four answer sections** (Question Explanation, Concept Explanation, Real-World Example, and Interview Response). Section 1 can be punchier; Section 2 should be the richest teaching moment; Section 4 should sound like natural spoken English in an interview.

## Instructions

### 1. Creating New Questions
*   When generating or adding new interview questions, place them in the correct section within `questions.md`.
*   Ensure questions are formatted as a single, direct inquiry (avoid multi-part questions in a single bullet).
*   Always include a difficulty level tag at the start: `**[Easy]**`, `**[Medium]**`, or `**[Hard]**`.

### 2. Writing Answers
*   Every question must have a corresponding answer file in the `answers/category_<number>/` directory.
*   File naming convention: Use `q` followed by the zero-padded question number (e.g., `q01`, `q02`, ...), a hyphen, and the first three words from the matching short-form heading in `udemy_question_heading.md`, slugified in lowercase kebab-case (e.g., `Extracting Valid JSON From Emails` (Question 7) becomes `q07-extracting-valid-json.md`).
*   **Voice:** Follow the **Instructor Persona** above in every answer—Matt Pocock clarity + Karpathy first-principles intuition.
*   **Answer File Structure:**
    *   H1 Heading: `# Question X: [Brief Topic]`
    *   `**Question:** [Full question text from questions.md]`
    *   `**Answer:**` You must structure the answer with exactly four sections in this order:
        1. **### 1. Question Explanation:** Explain the "why" behind the question (around 100 words). Use the Instructor Persona—conversational and direct, as if speaking to students in a video (e.g., "Alright, when the interviewer asks you this, what they are really looking for is..."). What is the interviewer trying to figure out? What red flags are they watching for?
        2. **### 2. Concept Explanation:** This is the main teaching moment. Write detailed senior-engineer notes in the Pocock + Karpathy voice—first principles, "why" before "what", analogies, misconceptions called out, thorough enough that the reader genuinely learns. Flowing paragraphs with bolded key terms; no bullet-point dumps.
        3. **### 3. Real-World Example:** Provide a concrete, real-world example of this concept in action (use cases, business scenarios, tool names).
        4. **### 4. This is how I would answer this:** Provide a rehearsed, concise response that the user can directly say in an interview setting. Keep it brief and punchy, avoiding over-explanation, exactly how someone would speak in a real interview. Use a first-person perspective ("In my experience...").

### 3. Synchronizing the README.md (CRITICAL)
*   **Rule:** The `README.md` must *always* remain perfectly synchronized with `questions.md`. 
*   Whenever a question is added, removed, or changed in `questions.md`, you must update the "Course Curriculum" list in `README.md`.
*   **Lecture Title Format:** Translate the question into a lecture title. 
    *   Format: `* **Lecture X:** [Title]`
    *   **Constraint:** The title must be highly concise, strictly **4 to 5 words maximum**.
    *   **Constraint:** Focus on professional interview preparation. Do NOT use cliché or hype words such as "mastering", "zero to hero", "demystifying", or "ultimate".
*   **Source of truth for titles:** Lecture titles in `README.md` must match the heading for that question number in `udemy_question_heading.md` exactly.

### 4. Synchronizing udemy_question_heading.md (CRITICAL)
*   **Rule:** The `udemy_question_heading.md` file must *always* remain synchronized with `questions.md`.
*   Whenever a question is **added**, **removed**, **reordered**, or **changed** in `questions.md`, you must update `udemy_question_heading.md` in the same commit or change set.
*   **File purpose:** Stores the **Udemy video / lecture title** (4–5 word heading) for every question in the bank.
*   **File structure:**
    *   Group headings by the same sections used in `questions.md` (Section 1–4).
    *   Use a table with columns: `#`, `Udemy Heading`.
    *   Every question in `questions.md` must have exactly one row with a matching question number.
*   **Heading format:**
    *   Strictly **4 to 5 words maximum** (count hyphenated terms as one word, e.g. "Few-Shot" = 1 word).
    *   Professional, interview-prep tone. No hype words ("mastering", "zero to hero", "demystifying", "ultimate").
    *   Headings should describe the topic clearly enough to stand alone as a video title on Udemy.
*   **Cross-file checklist** (run whenever `questions.md` changes):
    1. Update `udemy_question_heading.md` (add/edit/remove rows and update link).
    2. Update `README.md` Lecture list so each question's lecture title matches `udemy_question_heading.md`.
    3. Update or create the answer file in `answers/category_<section>/qNN-<first-three-udemy-heading-words>.md` if the question changed.
    4. Create or update the Excalidraw concept diagram in `answers/category_<section>/visuals/qNN-<first-three-udemy-heading-words>.excalidraw` and render it to a `.png` export.

---

## Question Update Order (MANDATORY)

Whenever any question is changed — whether it is the question text, topic, heading, or HTML deck — **always update in this exact sequence**. Never update the HTML before the source files are correct.

1. **Answer `.md` file** (`answers/category_<n>/qNN-<slug>.md`) — update the question text, explanation, example, and interview response.
2. **`udemy_question_heading.md`** — update the 4–5 word Udemy heading for that question number and update the link.
3. **`questions.md`** — update the question text and difficulty tag.
4. **Excalidraw diagram** (`answers/category_<n>/visuals/qNN-<slug>.excalidraw` & `.png` export) — create/update the visual diagram mapping to the concept and render it to PNG.
5. **HTML deck** (`answers/category_<n>/html-learning/<nn>.html`) — update last, sourcing only from the updated `.md` file.

The HTML is a derived artefact. If a source file has not been updated yet, do not touch the HTML — it will be inconsistent with the course curriculum files.
