# Question 27: Browser Edge Or Server Inference

**Question:** Where should inference run — browser, edge, server — and why?

**Answer:**

### 1. Question Explanation
Alright, this is a practical architecture question. The interviewer is checking whether you understand that model inference is not just about "where can I call the API?" It is about latency, privacy, cost, scalability, security, and operational control. A red flag is giving a one-size-fits-all answer like "always run it on the server" or "edge is always faster." Good engineers choose the runtime based on the constraints of the product.

### 2. Concept Explanation
Think of inference placement as a trade-off between **control, latency, privacy, and cost**.

**Browser inference** means the model or API call runs from the user's device. This can reduce server load and sometimes improve privacy if data stays local, especially for small on-device models. But it also exposes more implementation details to the client, depends heavily on device capability, and is harder to control consistently across users. You usually avoid browser-side inference for sensitive API keys or large hosted model calls.

**Edge inference** runs close to the user, usually in a geographically distributed runtime. The benefit is lower latency than a central server and better scalability for lightweight inference or request preprocessing. The downside is that edge environments often have stricter compute, memory, package, and execution-time limits. Edge is great when you need fast regional responses, but not always ideal for heavy workloads.

**Server inference** gives you the most control. You can protect secrets, centralize logging, apply rate limits, manage retries, route across providers, and enforce security policies. The trade-off is that latency may be higher if the server is far from the user, and you carry more infrastructure cost. For most production LLM applications that call managed APIs, server-side orchestration is the safest default.

The best answer is not a location; it is a decision framework. Ask: Is the data sensitive? Do I need to protect API keys? How large is the model? What latency target do I have? Do I need observability and centralized policy enforcement? Those answers determine where inference belongs.

### 3. Real-World Example
Imagine an AI writing assistant. A tiny grammar model might run in the browser for instant local suggestions. A low-latency autocomplete endpoint might run at the edge. But calls to GPT-4 or Claude that require API keys, billing controls, audit logs, and safety filters should usually go through the server. The product may use all three layers for different parts of the experience.

### 4. How Other Platforms and Runtimes Handle This

**Vercel AI SDK + Edge Runtime**
Vercel's AI SDK is designed with streaming in mind and supports both Node.js server routes and Edge runtime routes. When you deploy an AI route on the Edge, the LLM API call originates from a Vercel edge node geographically close to the user, reducing time-to-first-token. The SDK handles streaming back to the browser natively. The constraint: edge functions on Vercel have a 25MB bundle limit and can't use Node.js-native modules — so complex orchestration logic needs to stay in a serverless Node function, not the edge layer.

**Cloudflare Workers AI**
Cloudflare takes edge inference a step further — it actually runs small models (Llama 3, Mistral, Whisper) on GPU-enabled Cloudflare edge nodes worldwide. You write a Worker (JS/TS) and call `env.AI.run()` with a model ID. The model runs at the edge, not via a remote API call. Latency is extremely low for supported models. The limitation: only smaller open-weight models are supported; you can't run GPT-4 at the edge this way. Used heavily for classification, summarisation, and embedding generation close to the user.

**WebLLM / WebGPU (true browser inference)**
WebLLM is an open-source project that runs quantised LLMs (Llama, Mistral, Phi) directly in the browser using WebGPU. The model is downloaded to the user's device and inference happens entirely client-side — zero API calls, zero server involvement. Privacy is absolute. The constraints: the first load requires downloading a multi-hundred-MB model, device GPU support is required (not available on all hardware), and models are limited to smaller quantised variants. Used in privacy-sensitive demos and offline-capable tools.

**AWS Lambda + CloudFront (server, globally distributed)**
The classic AWS pattern: LLM orchestration logic runs in a Lambda function, placed behind CloudFront (CDN). CloudFront routes each request to the nearest Lambda regional endpoint, providing geo-distribution without true edge compute. API keys are kept in AWS Secrets Manager, logging goes to CloudWatch, and IAM policies control what the Lambda can call. This is "server inference with geographic distribution" — more control than Cloudflare Workers AI but less latency than a single-region server.

**On-device inference (iOS / Android)**
Apple's Core ML and Google's MediaPipe / TFLite enable running quantised models on-device on mobile. Apple Intelligence uses on-device models for low-latency, privacy-preserving tasks, falling back to server inference for complex requests. The pattern: classify the request complexity first, run lightweight tasks on-device, and route heavier tasks to the server. This tiered model is increasingly common in mobile AI products.

| Runtime | Latency | Privacy | Model Size Limit | API Key Safety | Best For |
|---|---|---|---|---|---|
| Server (Node / Lambda) | Medium | High (data stays server-side) | Unlimited | Full | Production LLM apps |
| Vercel Edge + AI SDK | Low | High | Limited by bundle | Full | Streaming chat UIs |
| Cloudflare Workers AI | Very low | High | Small OSS models only | Full | Edge classification / embeddings |
| WebLLM (WebGPU) | Very low (after load) | Absolute (no server) | Small quantised models | N/A | Offline / privacy-critical |
| On-device (Core ML / MediaPipe) | Very low | Absolute | Small quantised models | N/A | Mobile AI features |

The decision tree: start with server inference as the safe default. Move to edge only when latency is the primary constraint and the model/task fits within edge limits. Move to browser/device only when privacy is absolute and you can accept smaller models and download overhead.

### 5. This is how I would answer this
"I choose browser, edge, or server based on latency, privacy, cost, and control. Browser inference can be useful for small local models, but I would not expose sensitive API keys there. Edge is good for low-latency lightweight work near the user. Server-side inference is usually my default for production LLM apps because it gives me centralized security, logging, routing, and rate limiting."
