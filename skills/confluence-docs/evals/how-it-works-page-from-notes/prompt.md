---
tags: [confluence-docs]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

We need a Confluence page in our Engineering space (key ENG) under Engineering › Architecture & runtime explaining how the nightly macros embedding job works, for our tech lead and the two engineers who will maintain it. Facts: the job runs every day at 00:00 UTC from a pg_cron entry called macros-embed; it reads the support macros dump (about 1,900 macros), embeds the ones whose text changed with text-embedding-3-large, writes them into a pgvector table macro_embeddings, and the assistant's search_macros tool reads that table. Before this job we embedded at query time and it cost about $31 a month; now it is about $0.12 a month. If the job fails, the tool falls back to the previous embeddings for up to 26 hours, then returns "macros unavailable". The switch is PRODUCTION_MACROS_VARIANT (v3 today, v2 is the rollback). Tickets PROJ-957 and PROJ-963. We publish through the Atlassian connector. Write the page body into macros-embedding.html in the format the connector takes, with a drawn diagram of the flow, and tell me which parent page to use and what you would still need to verify.
