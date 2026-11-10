---
name: confluence-docs
description: Write, update, re-organise and publish Confluence pages in a proven house style: brief, an "In one minute" summary, numbered sections built from tables, panels for warnings and decisions, a drawn diagram for anything with more than three moving parts, every figure with its source, no credential values. Use it whenever someone asks to document, write up, record a decision, "put it in Confluence", create or update a page, add a diagram or screenshot to a page, clean up a space or build an entry page, even when they only say "write the doc" or "add a page" for a feature, benchmark, deployment, incident, architecture or how-it-works topic. Not for issue-tracker tickets, emails or chat messages on their own.
compatibility: Python 3.9+ for scripts/confluence.py (standard library only). Optional for image diagrams, mmdc (mermaid-cli) and a Chrome or Chrome for Testing binary. Works with the Atlassian MCP connector when it is connected, or with a personal API token through the script.
---

# Confluence docs

A Confluence page is read by busy people, usually right before a decision: a manager who has one
minute, an engineer who needs the exact table, a newcomer who inherits the project. The page has to
work for all three at once. That is what the house style below buys: the first screen answers "what,
so what, what next"; the body holds checkable facts; nothing is left for the reader to guess.

## The house style, and why each rule exists

- **Brief.** One short paragraph, then bullets and tables. A sentence that does not change what the
  reader will do gets cut. Long material (logs, SQL, benchmark tables) lives at its source and gets a link.
- **Open with the purpose, the tickets and the safety line.** First paragraph: what the page is for,
  the ticket links, and for engineering pages "No credential value appears on this page." Readers
  decide in that paragraph whether to keep reading.
- **"In one minute" next.** Five to seven bullets with the numbers in them (dates, counts, costs,
  durations). Someone who reads only this block must leave with the right picture.
- **Then numbered `## 1.` sections, built from tables.** Tables make gaps visible: an empty cell is a
  question, prose hides it. Use a header row, short cells, one idea per row.
- **Panels for the things people must not miss.** One info panel for scope or a precondition, one
  warning panel for a risk, one success panel for the recommendation or decision. More than three
  panels on a page means nothing stands out.
- **Status at the top.** A small table (or a status lozenge): Status, Since/Updated, Owner, Tickets,
  Review. Pages drift; the date tells the reader how much to trust it.
- **Every figure has its source and its method.** "$0.27 per ticket (cost table over 30 days, SQL in
  section 5)" beats "$0.27". Add a Sources section at the end: code paths with their revision, queries,
  tickets, earlier pages.
- **Absolute dates** (10 Nov 2026), ISO when sorting matters, times with their zone (UTC or local).
- **Plain words.** Say what happens, not that something "leverages" or "ensures". No em dashes.
  English by default; another language only when the surrounding pages and readers use it, and even
  then keep technical terms in English where that is natural.
- **A diagram when there are more than three moving parts or a hand-off.** A flow with steps and
  arrows is read ten times faster than the paragraph describing it. Draw it (section "Diagrams");
  never publish a page with a placeholder where a picture should be.
- **No secrets, no customer personal data.** Names of settings and secrets are fine; values never are.
  Customer data is described by shape ("the ticket text"), not quoted.

## Patterns worth copying from the best release and decision pages

The strongest pages we have seen (a tech lead's release pages) share one shape. Copy it:

- A **Field / Value table** at the top (Status, Owner, Dates, Tickets, Participants), then **one line
  of scope** ("What this release covers"), then a **links line**.
- **Short `##` sections, each with a table**, no section longer than one screen.
- A **"Results and feedback" section** created empty at publication, so the page already has the
  place where reality will be recorded.
- A **"Decision of <date>" panel** at the end: the decision in one sentence, who took it, what it
  changes. Later decisions are added as new dated panels; earlier ones are never rewritten.
- **One line per decision on the overview page**, linking to the detailed page. Detailed "how X
  works" pages live under their section overview (for example Architecture & runtime, Knowledge &
  ingestion, Integrations, Deployment & security, Evaluation), and the overview lists its children.

## Workflow

### 1. Get the brief straight

Before writing, know: who reads it and what they will do with it; whether a decision is pending;
which tickets it belongs to; where in the space it goes (which parent page); the language; the
deadline. If the request leaves one of these open, choose the natural default, state it in one line
and carry on. Do not ask a round of questions.

### 2. Read before you write

- The parent page and two or three sibling pages: match their layout and vocabulary so the space
  reads as one voice. Fetch the page tree (`getConfluencePageDescendants`, or `confluence.py children`)
  rather than trusting a remembered map: ids and titles move.
- The ticket(s): the Outcome and Done-when lines tell you what the page must prove.
- The source of truth for every fact: code at a named revision, migrations, dashboards, queries. Never
  write a number or a behaviour from memory. If you could not check something, write "not verified"
  next to it rather than guessing.

### 3. Choose the page type and start from its template

| You are writing | Template in `references/page-templates.md` |
|---|---|
| How a feature or system works | How-it-works page |
| A release, a plan, a decision to take or record | Decision / release page |
| A benchmark, a measurement, an A/B result | Results page |
| An operating procedure or runbook | Runbook page |
| The entry point of a space or section | Entry (start here) page |

### 4. Outline, fill, cut

Write the title as subject plus angle ("Ticket history: how the agent uses earlier tickets"). Draft
the "In one minute" block last, from the finished sections, so it carries the real numbers. Then cut:
every paragraph that could be a table row becomes one; every sentence that repeats a table is removed.

### 5. Draw the diagram

Two ways, by situation. Both are in `references/page-formats.md`.

- **Native, on the page** (default): a layout section with one custom panel per step, "➜" in step
  titles, a centred "⬇" paragraph between rows, two columns with success and warning panels for a
  "kept vs never kept" contrast. It needs no attachment, survives edits by others and renders
  everywhere. Use palette colours only; panels cannot hold tables.
- **An image** when you need real topology (boxes with many edges, a sequence diagram, a chart):
  write Mermaid, render it with `scripts/render_diagram.sh`, upload it with
  `scripts/confluence.py upload`, and reference it with the media markup. Keep the `.mmd` source in
  the repository so it can be re-rendered. Look at the PNG before uploading it.

### 6. Publish

Two paths, two body formats. Pick the body format from the path, never the other way round:

- **The Atlassian MCP connector** (`createConfluencePage` / `updateConfluencePage`): call
  `getContentFormatGuide` once, then author the body in its HTML dialect (`<div data-type="panel-info">`,
  `<section data-type="layout-three-equal">`, `<span data-type="status">`, `<pre><code>`). Confluence
  storage XML (`<ac:structured-macro>`) renders as raw text there. It cannot upload attachments.
- **`scripts/confluence.py`** (REST, standard library, personal API token): takes Confluence storage
  format, uploads attachments, lists trees, archives pages. `references/publishing.md` covers the
  token and the commands.

Create the page under the right parent, then **re-read it** (or open it) and fix what renders badly.
A page is published when it reads well in the browser, not when the API returned 200.

### 7. Update safely

Other people add images, comments and lines. A full-body replace silently removes what they added.
So, before every update: fetch the live body, keep every media node, `data-local-id` and inline comment
marker you did not write, apply your change to that body, bump the version with a message, publish,
re-read. `confluence.py update` fetches the current version for you and refuses to publish when the
new body drops attachments the live page shows, unless you pass `--allow-media-loss`. Keep other
people's dated sections and decision panels intact; add a new dated row or panel instead.

### 8. Close the loop

Link the page from the ticket, post a short comment (what the page says, what is still open, who
reviews), and set the ticket status the team uses for "ready for review" (for example In Review; the
ticket owner closes it). Record the page id where the project keeps its notes.

## Checklist before you publish

- Title says subject and angle; parent page is the right section; the section overview lists the page.
- First paragraph: purpose, tickets, safety line.
- "In one minute" has the numbers; nothing in it is only in the body.
- Sections are numbered; each table has a header row; no empty cells without a reason.
- Dates absolute; every figure has source and method; Sources section present.
- Diagram present where the flow has more than three parts; no placeholder.
- No credential value, no customer personal data, no em dashes.
- Status table current; "Open points" or "Before it ships" table present when something is pending.
- Body format matches the publishing path (connector HTML vs storage format).
- Re-read after publishing, in the browser or by fetching the page.

## Pitfalls seen on real pages

- A page that only had a 📎 "image to insert here" placeholder was rejected. Draw natively or upload.
- A republish wiped the images the owner had dropped into the page minutes earlier. Re-read before
  every update and keep media nodes.
- Storage XML sent through the connector rendered as raw text; the connector's own HTML dialect works.
  In that dialect, wrap table-cell content in `<p>`, use `<time datetime>` for calendar dates, and
  write source-list links as inline smart links (`<a href="URL" data-card-appearance="inline"></a>`).
- A connector update failed with HTTP 500 until copied `data-local-id` attributes that did not belong
  to the page were removed. Keep the ids you fetched from that page; never invent or copy ids.
- "Put it in Engineering" meant directly under the Engineering page, not under one of its sections.
  When a request names a page, put it there and say in one line where the space's own rules would
  have placed it.
- Stale facts (an old switch name, last month's dates, a retired job) are the most common complaint.
  When touching a page, update its status table and check each named setting still exists.
- Rendering tools: Mermaid's bundled Chrome path goes stale; point `puppeteer.json` at a Chrome for
  Testing binary. `sips` crops from the centre; do not use it to crop screenshots.
- Mermaid renders a node label that starts with "1. " as "Unsupported markdown: list". Write
  "Step 1 ·" or put the number after a word.

## Files

- `references/page-templates.md`: the five page templates (connector HTML dialect), house style baked in.
- `references/page-formats.md`: the connector's HTML dialect and the REST storage format side by side,
  with the native-diagram recipe.
- `references/publishing.md`: connector vs REST, token setup, update safety, verification, archiving
  and space clean-up.
- `scripts/confluence.py`: `whoami`, `space`, `get`, `children`, `search`, `create`, `update`,
  `upload`, `attachments`, `archive` (REST, storage format).
- `scripts/render_diagram.sh`: Mermaid to PNG at 2x with the bundled theme.
- `assets/theme.json`, `assets/puppeteer.example.json`: diagram theme and renderer config.
- `evals/`: two test prompts for the skill.
