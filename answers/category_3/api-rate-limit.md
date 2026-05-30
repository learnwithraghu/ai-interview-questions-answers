# Question 16: API Rate Limits & Fallbacks

**Question:** During a product launch, your primary LLM API provider hits a severe rate limit (HTTP 429), causing complete service failure. How do you implement robust fallback mechanisms and load balancing across different models?

**Answer:**

### 1. Question Explanation
Alright, this question is about resilience engineering for AI systems. The interviewer is checking if you have thought about what happens when your *entire* AI stack depends on a single third-party API—a single point of failure that you do not control. A huge red flag is if you say "I'd contact OpenAI support"—that is not an engineering solution! They are looking for you to describe a multi-provider fallback strategy, retry logic with exponential backoff, and circuit breakers. This is standard backend reliability engineering applied to the LLM world.

### 2. Concept Explanation
Building a production LLM application on a single API provider is like running your entire business through a single internet connection with no backup. It works fine on a normal day, but the moment that provider has an outage or rate-limits you during peak traffic, you're completely down. The pattern to fix this is borrowed directly from traditional backend reliability engineering.

**Understanding HTTP 429 Rate Limits:** LLM API providers impose rate limits in two dimensions—requests per minute (RPM) and tokens per minute (TPM). When you hit either limit, you get a 429 Too Many Requests response. During a product launch or viral event, your traffic can spike far beyond your normal baseline and breach these limits in minutes. You need an architecture that responds automatically, not one that requires a human to make an emergency call to support.

**The LLM Gateway / Proxy Pattern:** Tools like **LiteLLM** or **Portkey** act as a proxy layer between your application and multiple LLM providers. You send all your LLM requests to the proxy using a consistent OpenAI-compatible API, and the proxy handles routing, fallback, and load balancing. Your application code doesn't change when you add a new provider or switch one out. This is the single most impactful architectural decision for LLM reliability.

**Retry with Exponential Backoff:** When you hit a 429, the worst thing you can do is immediately retry—you'll just keep getting 429s and pile up even more requests. Instead, wait before retrying: after the first failure, wait 1 second; after the second, wait 2 seconds; after the third, wait 4 seconds (doubling each time). Set a maximum retry count (typically 3). This gives the provider time to recover its rate limit window.

**The Circuit Breaker Pattern:** Exponential backoff is a retry strategy for *individual requests*. The circuit breaker is a *provider-level* strategy. If a provider fails 5 consecutive requests within 30 seconds, "open the circuit" for that provider—stop routing any traffic to it for a cooldown period (e.g., 60 seconds). This prevents your entire application from hanging on a provider that's clearly having a bad time. After the cooldown, the circuit closes again and you test whether the provider has recovered.

**Fallback Hierarchy:** Define your providers in a priority order: `GPT-4o → Claude Sonnet → Gemini Flash → your self-hosted Llama`. The tradeoff as you go down the list is typically capability vs. guaranteed availability. The key insight is that a slightly less capable model serving 100% of requests is infinitely better than a slightly more capable model failing 50% of them.

### 3. Real-World Example
A startup launched a viral AI feature that received 50x normal traffic. Their primary OpenAI API key hit its rate limit within minutes. Because they had implemented LiteLLM as a proxy with a configured fallback chain (OpenAI → Anthropic Claude), the system automatically rerouted 100% of traffic to Claude within seconds, with no user-visible downtime. After the traffic spike, the proxy automatically shifted back to OpenAI once its rate limits recovered.

### 4. How Other Tools and Frameworks Handle This

Understanding the landscape of LLM gateway options gives you stronger answers and shows you know the ecosystem.

**LiteLLM (open-source)**
The most widely used open-source LLM proxy. Supports 100+ providers behind a single OpenAI-compatible interface. Configures fallback chains and load balancing in a YAML file. Can be self-hosted or used as a managed service (LiteLLM Proxy). Great for teams that want full control and don't want vendor lock-in on the gateway itself.

**Portkey**
A managed LLM gateway SaaS. Similar to LiteLLM but adds built-in analytics, cost tracking per request, and A/B testing of different models. Also supports "semantic caching"—if two requests are semantically similar, return the cached response from the first, saving tokens entirely. Better fit for teams that want observability out of the box.

**OpenRouter**
A managed API routing service that acts as a single endpoint for 50+ models from OpenAI, Anthropic, Google, Meta, and others. It handles fallback and load balancing at the infrastructure level—you just pick your model preferences and it handles the rest. Less code overhead than self-hosted LiteLLM but less control.

**Kong AI Gateway**
Kong extended its traditional API gateway (widely used for REST APIs) with an AI layer. If your team already runs Kong for standard API traffic, the AI Gateway adds LLM routing, rate limiting, and prompt logging on top of existing infrastructure. Better suited for enterprise teams with a Kong footprint who want one unified gateway.

**AWS Bedrock + API Gateway**
Amazon's approach is to offer multiple foundation models (Claude, Titan, Llama) behind a single managed endpoint. You switch models by changing a parameter, not by reconfiguring infrastructure. AWS API Gateway sits in front and handles throttling natively. The trade-off: you're locked into the AWS ecosystem but get SLA-backed uptime and native IAM integration.

| Tool | Hosting | Key Strength | Best For |
|---|---|---|---|
| LiteLLM | Self-hosted or managed | Full control, 100+ providers | Teams wanting OSS + customisation |
| Portkey | Managed SaaS | Semantic caching + analytics | Teams wanting observability OOTB |
| OpenRouter | Managed SaaS | Zero-config model switching | Rapid prototyping |
| Kong AI Gateway | Self-hosted | Unified with existing API gateway | Enterprise Kong users |
| AWS Bedrock | Managed (AWS) | IAM + SLA-backed | AWS-native teams |

The common thread: every production LLM architecture eventually installs *something* between application code and provider APIs. The choice between them is mostly about self-hosting vs. managed, and how much observability you need baked in.

### 5. This is how I would answer this
"I'd architect the LLM layer with a proxy like LiteLLM so I can route to multiple providers without changing application code. I'd configure a fallback chain—OpenAI first, then Anthropic, then Gemini—so if one provider hits rate limits, traffic automatically shifts. On top of that, I'd implement retry logic with exponential backoff so we don't hammer a provider that's struggling, and a circuit breaker to stop routing to a provider that's consistently failing. For high-traffic situations, I'd also put a request queue in front to absorb spikes smoothly instead of failing requests outright."
