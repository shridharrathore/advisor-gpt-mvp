## Working Agreement with Windsurf:
   - Human(Tech Lead): Problem Statement, Technical Stack, Architecture, Design, core Code , security, policies
   - AI(Windsurf): Docs, tests, scaffolding, wiring, small refactors, debugging (no security/policy decisions).
   - Human(Reviewer: Final Merges, Deployment

    # How we work together:
    - We will work together in small pieces decided by tasks created under epics in PROJECT_PLAN.md
    - You will first create tests for next task and I will review those tasks and confirm
    **Tests first → minimal impl → verify → commit → update tracker.**
    - You will create boilerplate code for above task and I will review and confirm
    - You will review the completed code and suggest refactoring if needed
    - You will create boilerplate for frontend and backend but ask for approval and I will review before approving
    
    # Guardrails:
    - Max change: **≤150 LOC or ≤5 files**.
    - **Ask before writing**; list files + est. LOC.
    - Add no new dependencies without approval and no PII

    ## Definition of Done (per task)
    - Tests pass (happy + edge) and meet agreed coverage.
    - Code is clean, consistent, and smooth.
    - Code is well-documented and easy to understand.
    - Code is well-structured and easy to maintain and understand.
    - Citations are required or answer blocked by evidence gate
    - Audit log is required per response (JSONL)
    - Version tags(model/prompt) are required on every record   
    - Fairness and bias check is required