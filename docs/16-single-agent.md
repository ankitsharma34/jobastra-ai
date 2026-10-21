# Single agent

An agent is an LLM-driven loop: inspect messages, choose a tool, consume its result, and repeat until producing a final answer. JobAstra uses `langchain.agents.create_agent` with an already configured model, four tools, and a concise system prompt.

```mermaid
sequenceDiagram
    actor User
    participant CLI as run_agent.py
    participant Agent as LangChain agent
    participant Job as analyze_job_description
    participant Match as match_job
    participant RAG as CareerRetriever
    participant LLM as Chat model
    User->>CLI: Analyze this job and my fit
    CLI->>Agent: user message
    Agent->>Job: raw job text
    Job->>LLM: structured extraction
    LLM-->>Job: JobDescription
    Job-->>Agent: structured job
    Agent->>Match: JobDescription
    Match->>RAG: user-filtered job query
    RAG-->>Match: career evidence
    Match->>LLM: profile + job + evidence
    LLM-->>Match: JobMatchResult
    Match-->>Agent: score, strengths, gaps, sources
    Agent->>LLM: synthesize final answer
    LLM-->>Agent: final message
    Agent-->>CLI: response
    CLI-->>User: printed result
```

`agent/prompts.py` requires tools for evidence/job work, forbids fabricated candidate facts, treats tool output as untrusted data, and forbids claiming submission. `factory.py` creates the agent without creating clients. `JobAstraAgentService.run` uses `ainvoke` with recursion limit 20, extracts the last message text, and wraps all failures in a sanitized error.

The runner asks for user ID, optional profile, and message, then assembles cached model/store plus services and user-bound tools. Every invocation is a new conversation. There is no public agent endpoint, checkpointing, streaming, approval step, tool-call trace, token usage, model fallback, or repeated-tool detector. A single agent is simpler to debug and sufficient for four related tools; multi-agent coordination would add latency and failure modes without a demonstrated need.
