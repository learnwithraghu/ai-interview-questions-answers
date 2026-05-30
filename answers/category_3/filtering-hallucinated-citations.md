# Question 18: Mitigating Hallucinated Citations

**Question:** Users report that your LLM app occasionally hallucinates highly realistic but fake citations and URLs. How do you detect, mitigate, and filter hallucinated facts in a production pipeline before the user sees them?

**Answer:**

### 1. Question Explanation
Alright, this is one of the most dangerous failure modes in production AI—and it's deceptive because the hallucinations look real. The interviewer is checking if you understand that hallucination is not just an annoyance, it's a trust and liability issue. They want to see if you have a concrete pipeline for catching these before they reach users. A red flag is if you say "I'd tell the model not to hallucinate"—that doesn't work! They are looking for you to describe a verification pipeline: grounding responses in retrieved sources, URL validation, and using a secondary model to fact-check outputs.

### 2. Concept Explanation
Hallucination is one of the most insidious problems in production AI because the model doesn't signal uncertainty—it presents made-up facts with the same confident tone as real ones. A fake URL looks exactly like a real URL. A hallucinated academic citation is formatted correctly, sounds plausible, and could easily fool a non-expert. In domains like legal, medical, or financial services, this isn't just a UX problem—it's a liability.

The key mental model is **prevent → detect → filter**, applied in sequence.

**Prevention — Stop hallucinations from being generated in the first place.** The most effective prevention technique is grounding. If you anchor the model's response entirely in retrieved source documents (RAG), it has far less opportunity to invent things. Your system prompt should explicitly say: "Only cite facts that appear in the provided source documents. If the answer isn't there, say you don't know." You should also require structured citations: instruct the model to tag every factual claim with a source reference like `[Doc: invoice-policy-2024.pdf, page 3]`. Now every claim is traceable.

**Detection — Catch what slipped through.** Even well-grounded models occasionally hallucinate. Your pipeline needs automated checks:

- **URL Validation:** After generation, use a regex to extract every URL in the response. Fire an HTTP HEAD request to each one. If you get anything other than a 200 OK (especially a 404 or a DNS failure), that URL is hallucinated. Flag it.
- **LLM-as-a-Fact-Checker:** Pass the generated response and the source documents to a secondary LLM with a specific prompt: "Does every factual claim in the response appear in the provided sources? List any claims you cannot find in the sources." This is slower and more expensive, but catches subtle hallucinations that URL checking won't find.
- **NLI Entailment Checking:** For high-stakes applications, use a Natural Language Inference (NLI) model—a lightweight model specifically trained to determine if a statement is entailed by (supported by) a given passage. Run this against each sentence in the response vs. the retrieved chunks. Anything with low entailment confidence gets flagged.

**Filtering — Block it before the user sees it.** When a check fails, you have three options: silently regenerate the response (best for high-confidence detections), strip the hallucinated claim and fill with a disclaimer (good for partial hallucinations), or display the response with a warning banner. Log everything for post-hoc analysis so you can improve your retrieval and prompting over time.

### 3. Real-World Example
A legal research AI tool was generating case citations that looked real but didn't exist—a critical trust failure. The team added a two-step verification: first, all case citations were validated against a legal database API. Second, a fact-checking LLM compared every generated claim against the retrieved source documents. Any response with an unverifiable citation was automatically regenerated. Hallucinated citations dropped by 94%.

### 4. This is how I would answer this
"My strategy is prevent, detect, and filter. For prevention, I ground all responses in RAG—the model only cites what's in the retrieved context. For detection, I extract all URLs and citations post-generation and validate them programmatically—checking URLs with an HTTP request, and checking factual claims with a secondary LLM that compares the output against the source documents. If anything can't be verified, it gets filtered out before the user sees it—either through regeneration or by stripping the hallucinated claim and flagging it for review."
