# Course Content Management Skill

## Description
This skill defines the standard operating procedure for managing the curriculum of the "AI Engineer Interview Bootcamp" repository. It must be followed whenever you are adding new questions, writing answers, or modifying existing course content.

## Instructions

### 1. Creating New Questions
*   When generating or adding new interview questions, place them in the correct section within `questions.md`.
*   Ensure questions are formatted as a single, direct inquiry (avoid multi-part questions in a single bullet).
*   Always include a difficulty level tag at the start: `**[Easy]**`, `**[Medium]**`, or `**[Hard]**`.

### 2. Writing Answers
*   Every question must have a corresponding answer file in the `answers/category_<number>/` directory.
*   File naming convention: Use a two-digit number corresponding to the question number (e.g., `07.md`, `12.md`).
*   **Answer File Structure:**
    *   H1 Heading: `# Question X: [Brief Topic]`
    *   `**Question:** [Full question text from questions.md]`
    *   `**Answer:**` You must structure the answer with exactly four sections in this order:
        1. **### 1. Question Explanation:** Explain the "why" behind the question (around 100 words). The tone MUST be conversational and direct, as if you are an instructor speaking to your students in a video course (e.g., "Alright, when the interviewer asks you this, what they are really looking for is..."). What is the interviewer actually trying to figure out about the candidate? What red flags are they looking for?
        2. **### 2. Concept Explanation:** Write this as detailed senior-engineer teaching notes. The tone should feel like a knowledgeable mentor explaining the concept to a junior developer—build understanding from first principles, explain the "why" before the "what", use analogies, call out common misconceptions, and be thorough enough that the reader genuinely learns the concept by reading it. Do NOT just write bullet points—use flowing paragraphs with bolded key terms.
        3. **### 3. Real-World Example:** Provide a concrete, real-world example of this concept in action (use cases, business scenarios, tool names).
        4. **### 4. This is how I would answer this:** Provide a rehearsed, concise response that the user can directly say in an interview setting. Keep it brief and punchy, avoiding over-explanation, exactly how someone would speak in a real interview. Use a first-person perspective ("In my experience...").

### 3. Synchronizing the README.md (CRITICAL)
*   **Rule:** The `README.md` must *always* remain perfectly synchronized with `questions.md`. 
*   Whenever a question is added, removed, or changed in `questions.md`, you must update the "Course Curriculum" list in `README.md`.
*   **Lecture Title Format:** Translate the question into a lecture title. 
    *   Format: `* **Lecture X:** [Title]`
    *   **Constraint:** The title must be highly concise, strictly **4 to 5 words maximum**.
    *   **Constraint:** Focus on professional interview preparation. Do NOT use cliché or hype words such as "mastering", "zero to hero", "demystifying", or "ultimate".
