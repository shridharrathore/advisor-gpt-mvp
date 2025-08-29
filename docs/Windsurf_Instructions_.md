Use the “Advisor GPT – MVP” brief below as binding context. 
Deliver: docs/PLAN.md with 10–12 epics and task tables (ID | Title | AC | Deps | Owner), 
Reflect these guardrails: 3-pane workbench; RAG contract (chunk_size≈800, overlap≈120, top_k=4, min_score≈0.35, fixed JSON {answer,steps[],cited_spans[],confidence,disclaimers}, evidence gate+fallback); 
Responsible AI (agent-only, PII redaction pre-index, per-response audit JSONL with version tags); 
Success (retrieval@3, groundedness≥95%, P95<3s); 
Observability (latency P50/P95 from logs); 
Show PLAN.md draft only and ask for approval before writing files.