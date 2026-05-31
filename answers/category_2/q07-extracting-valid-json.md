# Question 7: Extracting Valid JSON

**Question:** You need to extract structured JSON data (like user profiles) from unstructured customer emails. How would you design the prompt and API call to guarantee valid JSON output?

**Answer:**

### 1. Question Explanation
Okay folks, this is a very practical, day-to-day GenAI engineering question. The interviewer wants to know if you've ever actually tried to get an LLM to output structured data in production—because anyone who has, knows it can be a nightmare if you don't do it right! A huge red flag is if you just say "I'd tell it in the prompt to return JSON"—that alone is not enough to *guarantee* it. They are looking to see if you know about temperature settings, JSON mode / structured output APIs, Pydantic schema validation, and retry logic. Basically, they want to know you can build something reliable.

### 2. Concept Explanation
Here's something most beginners learn the hard way: **telling an LLM "return JSON" in the prompt is not a guarantee**. Without the right setup, the model might return JSON with a markdown code fence around it, add commentary before the opening brace, or subtly hallucinate a field name—any of which will break your `json.loads()` call. In production, a broken parsing step means your entire pipeline crashes. So you need layers.

**Layer 1 — Force it at the API level.** Modern LLM APIs have a `response_format` or structured output parameter. OpenAI's is `response_format={"type": "json_object"}`. Google Gemini has `response_schema`. This constrains the model at the *token generation* level—it literally cannot output tokens that would produce invalid JSON. This is your strongest guarantee and should always be your first tool.

**Layer 2 — Define the schema explicitly in the prompt.** Even with JSON mode on, the model needs to know *which fields* to return. Put the exact schema in your system prompt—field names, types, whether they're optional, and a short example. The more precise you are, the less the model has to guess. Something like: `{"name": "string", "email": "string", "years_experience": "integer", "skills": ["string"]}`.

**Layer 3 — Set temperature to 0.** You already know why from our earlier lesson. Any randomness here is your enemy. Zero temperature means the model always picks the most deterministic, well-formatted output.

**Layer 4 — Validate with Pydantic.** Even with everything above, treat every LLM response as untrusted input. Parse it with a Pydantic model that enforces your exact field types and constraints. If validation fails, you'll get a clear, structured exception you can act on—not a silent runtime error halfway through your pipeline.

**Layer 5 — Retry with the error message.** If Pydantic validation fails, don't just retry blindly. Feed the specific validation error *back to the LLM* and ask it to fix it: "Your previous response failed validation with this error: `field 'years_experience' expected int, got str`. Please return the corrected JSON." One retry with a specific error message fixes the problem the vast majority of the time.

### 3. Real-World Example
An HR SaaS company receives thousands of unstructured CVs via email. They build a pipeline where each CV email is passed to GPT-4o with a Pydantic schema defining `name`, `email`, `years_experience`, and `skills_list`. They use `response_format=json_object`, temperature 0, and validate every response against the Pydantic model before writing to their database. Failed validations trigger an automatic retry with the error message appended to the prompt.

### 4. This is how I would answer this
"I'd use a three-layer approach. First, I'd use the API's structured output or JSON mode to force the model to only emit valid JSON. Second, I'd include the exact schema I want in the system prompt with an example, and set temperature to zero for consistency. Third, on the application side, I'd parse the response with Pydantic. If validation fails, I'd automatically feed the error back to the model and ask it to fix the output—usually one retry is enough in my experience."
