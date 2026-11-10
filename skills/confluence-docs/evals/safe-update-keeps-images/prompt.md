---
tags: [confluence-docs]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Our Confluence page "Supabase deployment and branches" (id 1696366608, space ENG) is out of date: the pre-generation switch is no longer the PREGEN_ENABLED secret, it is the enabled row of the pregeneration_settings table, flipped by admins from Settings. We publish this one through the REST script with my token. The live body in storage format is in live-1696366608.html (a colleague dropped two images into it yesterday). Prepare the corrected body as updated-1696366608.html and give me the exact command to publish it with the skill's script, with a version message naming PROJ-751. Do not lose anything the colleague added.

Input files: live-1696366608.html
