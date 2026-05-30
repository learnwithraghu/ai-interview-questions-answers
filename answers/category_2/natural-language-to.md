# Question 10: Text-to-SQL Challenges

**Question:** Your application uses an LLM to generate SQL queries from natural language. How do you handle database schema changes and prevent the LLM from hallucinating column names?

**Answer:**

### 1. Question Explanation
Listen up—this question is specifically designed to see if you've thought about the reliability and maintainability of a Text-to-SQL system in production. Anyone can get an LLM to generate a SQL query in a demo. The real challenge is keeping it accurate as your database evolves. The interviewer is looking for you to mention schema injection into the prompt, and they want to see you understand that if the model doesn't *know* the schema, it will make up column names. A red flag is if you don't mention any form of schema management, validation, or automated schema-syncing mechanism.

### 2. Concept Explanation
Text-to-SQL is one of the most exciting and treacherous LLM use cases. It sounds simple in a demo, but in production you'll quickly discover that an LLM with no information about your database schema will just invent column names with supreme confidence. The solution comes down to two principles: **ground it in the real schema** and **validate before you execute**.

**Grounding with Schema Injection:** The LLM doesn't know your database exists. You have to tell it. At query time, you dynamically fetch the schema for the relevant tables—their names, column names, data types, primary keys, and foreign key relationships—and inject it directly into the system prompt. Now the model can only reference columns that you've told it about. If the column doesn't appear in the prompt, it can't hallucinate it (mostly).

A smart enhancement here is to not inject the *entire* schema if your database is large. Instead, use a retrieval step (embedding your table descriptions) to first identify which tables are likely relevant to the user's question, then inject only those schemas. This keeps your prompt focused and avoids hitting token limits.

**Few-shot examples** are also critical here. Include 2–3 examples of natural language question → correct SQL query pairs in the system prompt. This guides the model's output format and teaches it how to handle things like JOINs, WHERE clauses, and aggregations in your specific schema.

**The schema change problem:** Databases evolve. A column gets renamed, a new table is added, a field changes type. If you don't update the schema you inject into the prompt, your LLM is working with stale information and will generate broken queries. The fix is to automate the schema sync—hook into your database migration pipeline (whether it's Alembic, Flyway, or plain SQL scripts) and regenerate your stored schema definition whenever a migration runs.

**Validation before execution:** Even with perfect schema injection, always validate the generated SQL before running it. Parse the query, extract the referenced table and column names, and cross-check them against the live database schema. If anything doesn't match, reject the query and retry with a corrected prompt. Never execute unvalidated SQL from an LLM against your production database.

### 3. Real-World Example
An e-commerce company builds a tool for analysts to query their sales database using plain English. They store the full schema as a structured dictionary in their system and automatically update it via a CI/CD hook whenever a database migration runs. Every generated SQL query is validated against the live schema before execution. If a column doesn't exist, the error is fed back to the LLM with the correct schema for a retry.

### 4. This is how I would answer this
"The main strategy is schema injection—I dynamically pull the current table schemas and inject them directly into the system prompt so the model only knows about columns that actually exist. To handle schema changes, I'd automate the schema sync so that whenever a database migration is deployed, the schema definition in the prompt is updated automatically. Before executing any generated SQL, I'd also validate the column names against the live DB schema and use that as a safeguard—if a column doesn't exist, I reject the query and retry with a corrected prompt."
