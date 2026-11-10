# claude-skills

Skills I use with Claude Code and Codex. Each folder under `skills/` is one skill: a `SKILL.md` with the
instructions, plus references, scripts and assets it needs. They are generic: no company names, ids or
credentials inside; your own defaults (site, space, parent pages) are discovered from the pages you point
the skill at.

| Skill | What it does |
|---|---|
| [confluence-docs](skills/confluence-docs/SKILL.md) | Write, update, re-organise and publish Confluence pages in a brief, table-first house style: purpose line, "In one minute", numbered sections, panels, a drawn diagram, every figure with its source. Works with the Atlassian MCP connector (its HTML dialect) or through a REST script with your own API token (storage format, attachments, archive). |

## Install

Claude Code (one skill):

```bash
git clone https://github.com/azizkhalsi/claude-skills.git
ln -s "$PWD/claude-skills/skills/confluence-docs" ~/.claude/skills/confluence-docs
```

Codex: link the same folder into `~/.codex/skills/`. Or copy the folder into a repository's `.codex/skills/`
or `.claude/skills/` so the whole team gets it.

Then say "write the Confluence page for ..." and the skill loads.

## Layout

```
skills/
  confluence-docs/
    SKILL.md              the instructions
    references/           page templates, page formats, publishing
    scripts/              confluence.py (REST helper), render_diagram.sh (Mermaid to PNG)
    assets/               diagram theme
    evals/                test prompts
```

## Licence

MIT.
