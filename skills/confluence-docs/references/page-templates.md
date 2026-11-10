# Page templates

Five skeletons in the Atlassian connector's HTML dialect (the common publishing path). Replace the
`{{...}}` parts, delete the rows you do not need. For the REST path, convert the few connector-specific
elements with the table in `page-formats.md` (panels, status, layouts, code blocks); the structure is
the same.

Contents: 1. How-it-works · 2. Decision / release · 3. Results · 4. Runbook · 5. Entry (start here)

## 1. How-it-works page

Title pattern: `{{Subject}}: how {{system}} {{does what}}`

```html
<p>This page explains how {{system}} {{does what}}, for {{readers}}. Tickets: <a href="{{ticket url}}">{{PROJ-123}}</a>. No credential value appears on this page.</p>
<table><tbody>
<tr><th><p>Status</p></th><td><p><span data-type="status" data-color="green">Live</span> since <time datetime="{{2026-11-10}}">{{10 Nov 2026}}</time></p></td></tr>
<tr><th><p>Written</p></th><td><p><time datetime="{{2026-11-10}}">{{10 Nov 2026}}</time>, from the code at <code>{{revision}}</code></p></td></tr>
<tr><th><p>Owner</p></th><td><p>{{Name}}</p></td></tr>
<tr><th><p>Review</p></th><td><p>{{Who}}, {{date or "open"}}</p></td></tr>
</tbody></table>
<h2>In one minute</h2>
<ul>
<li>{{What it does, with the number that matters.}}</li>
<li>{{Where it runs and who triggers it.}}</li>
<li>{{What it costs or how long it takes, measured how.}}</li>
<li>{{What it never does (privacy, scope limits).}}</li>
<li>{{What is still open.}}</li>
</ul>
<!-- native diagram: one layout section per row of steps, see page-formats.md section 2 -->
<h2>1. What happens, step by step</h2>
<table><thead><tr><th><p>Step</p></th><th><p>Where</p></th><th><p>What happens</p></th><th><p>Evidence</p></th></tr></thead><tbody>
<tr><td><p>1</p></td><td><p>{{component}}</p></td><td><p>{{one sentence}}</p></td><td><p>{{file or query}}</p></td></tr>
</tbody></table>
<h2>2. Settings and switches</h2>
<table><thead><tr><th><p>Setting</p></th><th><p>Where</p></th><th><p>Default</p></th><th><p>Who can change it</p></th></tr></thead><tbody>
<tr><td><p>{{NAME}}</p></td><td><p>{{Settings page / env / table}}</p></td><td><p>{{value}}</p></td><td><p>{{role}}</p></td></tr>
</tbody></table>
<h2>3. Limits and what is excluded</h2>
<table><thead><tr><th><p>Excluded</p></th><th><p>Why</p></th><th><p>What is kept instead</p></th></tr></thead><tbody>
<tr><td><p>{{...}}</p></td><td><p>{{...}}</p></td><td><p>{{...}}</p></td></tr>
</tbody></table>
<h2>4. How to check it is working</h2>
<table><thead><tr><th><p>Question</p></th><th><p>Where to look</p></th><th><p>Expected</p></th></tr></thead><tbody>
<tr><td><p>{{...}}</p></td><td><p>{{page / query}}</p></td><td><p>{{...}}</p></td></tr>
</tbody></table>
<h2>5. Open points</h2>
<table><thead><tr><th><p>Point</p></th><th><p>Owner</p></th><th><p>Next step</p></th></tr></thead><tbody>
<tr><td><p>{{...}}</p></td><td><p>{{...}}</p></td><td><p>{{...}}</p></td></tr>
</tbody></table>
<h2>Sources</h2>
<ul>
<li>Code: <code>{{path}}</code> ({{repo}}, branch {{name}}, revision {{sha}}, {{date}})</li>
<li>Queries: {{where the SQL is}}</li>
<li><a href="{{ticket url}}" data-card-appearance="inline"></a></li>
</ul>
```

## 2. Decision / release page

Title pattern: `{{Release or decision name}}` (short, the version or the question)

```html
<table><tbody>
<tr><th><p>Status</p></th><td><p><span data-type="status" data-color="blue">In progress</span></p></td></tr>
<tr><th><p>Owner</p></th><td><p>{{Name}}</p></td></tr>
<tr><th><p>Dates</p></th><td><p>{{start}} to {{end}}; review on {{date}}</p></td></tr>
<tr><th><p>Tickets</p></th><td><p>{{PROJ-...}}</p></td></tr>
<tr><th><p>Participants</p></th><td><p>{{names and roles}}</p></td></tr>
</tbody></table>
<p><strong>Scope.</strong> {{One line: what this release or decision covers, and what it does not.}}</p>
<p>Links: <a href="{{url}}">{{PRD}}</a> · <a href="{{url}}">{{previous release page}}</a> · <a href="{{url}}">{{project}}</a></p>
<h2>What {{this release}} adds</h2>
<table><thead><tr><th><p>Item</p></th><th><p>Ticket</p></th><th><p>Status</p></th><th><p>Note</p></th></tr></thead><tbody>
<tr><td><p>{{feature}}</p></td><td><p>{{PROJ-123}}</p></td><td><p><span data-type="status" data-color="green">Done</span></p></td><td><p>{{one line}}</p></td></tr>
</tbody></table>
<h2>Feedback from {{previous phase}}</h2>
<table><thead><tr><th><p>Item</p></th><th><p>Raised by</p></th><th><p>Ticket</p></th><th><p>Status</p></th></tr></thead><tbody>
<tr><td><p>{{...}}</p></td><td><p>{{name}}</p></td><td><p>{{PROJ-...}}</p></td><td><p><span data-type="status" data-color="yellow">Open</span></p></td></tr>
</tbody></table>
<h2>Options considered</h2>
<table><thead><tr><th><p>Option</p></th><th><p>Cost or effort</p></th><th><p>Risk</p></th><th><p>Recommendation</p></th></tr></thead><tbody>
<tr><td><p>{{A}}</p></td><td><p>{{...}}</p></td><td><p>{{...}}</p></td><td><p>{{keep / drop}}</p></td></tr>
</tbody></table>
<h2>Results and feedback</h2>
<p><em>Filled after {{the test window}}.</em></p>
<div data-type="panel-success"><p><strong>Decision of {{date}}.</strong> {{The decision in one sentence.}} Taken by {{who}}. It changes {{what}}.</p></div>
```

Later decisions are added as new "Decision of {{date}}" panels below; earlier panels are never edited.

## 3. Results page (benchmark, measurement, A/B)

Title pattern: `{{What was measured}}: {{the headline result}}`

```html
<p>{{What question this measurement answers}}, for {{who decides}}. Tickets: {{PROJ-...}}. No credential value appears on this page.</p>
<div data-type="panel-success"><p><strong>Recommendation.</strong> {{Keep / change / drop}}: {{one sentence with the decisive number and its confidence range}}.</p></div>
<h2>In one minute</h2>
<ul>
<li>{{Headline metric, with the before and after and the range.}}</li>
<li>{{Cost and latency change.}}</li>
<li>{{Where it did not change anything.}}</li>
<li>{{Sample size and judge.}}</li>
</ul>
<h2>1. Method</h2>
<table><thead><tr><th><p>Element</p></th><th><p>Value</p></th></tr></thead><tbody>
<tr><td><p>Dataset</p></td><td><p>{{n cases, source, how chosen}}</p></td></tr>
<tr><td><p>Judge</p></td><td><p>{{model or people, rubric}}</p></td></tr>
<tr><td><p>Variants</p></td><td><p>{{A vs B, exact settings}}</p></td></tr>
<tr><td><p>Repeats</p></td><td><p>{{runs per case}}</p></td></tr>
<tr><td><p>Known noise</p></td><td><p>{{A/A difference measured}}</p></td></tr>
</tbody></table>
<h2>2. Results</h2>
<table><thead><tr><th><p>Metric</p></th><th><p>A</p></th><th><p>B</p></th><th><p>Difference (95% range)</p></th></tr></thead><tbody>
<tr><td><p>{{...}}</p></td><td><p>{{...}}</p></td><td><p>{{...}}</p></td><td><p>{{...}}</p></td></tr>
</tbody></table>
<h2>3. What this means</h2>
<ul><li>{{Interpretation, one bullet per finding.}}</li></ul>
<h2>4. Limits</h2>
<ul><li>{{What the measurement cannot say.}}</li></ul>
<h2>5. Decision and next step</h2>
<table><thead><tr><th><p>Decision</p></th><th><p>By</p></th><th><p>Date</p></th><th><p>Next</p></th></tr></thead><tbody>
<tr><td><p>{{...}}</p></td><td><p>{{...}}</p></td><td><p>{{...}}</p></td><td><p>{{...}}</p></td></tr>
</tbody></table>
<h2>Sources</h2>
<ul><li>{{Eval repo path, PR, raw results location, SQL}}</li></ul>
```

## 4. Runbook page

Title pattern: `{{Task}}: how to {{do it}}`

```html
<p>How to {{task}}, for {{who}}. Takes about {{duration}}. Tickets: {{PROJ-...}}. No credential value appears on this page.</p>
<div data-type="panel-info"><p><strong>Before you start.</strong> {{access needed}}; {{state to check}}.</p></div>
<h2>1. Steps</h2>
<table><thead><tr><th><p>#</p></th><th><p>Do</p></th><th><p>Where</p></th><th><p>You should see</p></th></tr></thead><tbody>
<tr><td><p>1</p></td><td><p>{{action}}</p></td><td><p>{{page / command}}</p></td><td><p>{{result}}</p></td></tr>
</tbody></table>
<h2>2. If something goes wrong</h2>
<table><thead><tr><th><p>Symptom</p></th><th><p>Likely cause</p></th><th><p>Do</p></th></tr></thead><tbody>
<tr><td><p>{{...}}</p></td><td><p>{{...}}</p></td><td><p>{{...}}</p></td></tr>
</tbody></table>
<div data-type="panel-error"><p><strong>Never.</strong> {{The one action that causes damage, and why.}}</p></div>
<h2>Sources</h2>
<ul><li>{{...}}</li></ul>
```

## 5. Entry (start here) page

Title pattern: `{{Project}} {{area}}: start here` (or the existing overview page, with a "Start here" table added at the top)

```html
<p>Where to start on {{project area}}. One line per page; sections hold the detail. Newest pages are marked <span data-type="status" data-color="blue">New</span>.</p>
<h2>In one minute</h2>
<ul>
<li>{{Current phase, date, who leads.}}</li>
<li>{{The three pages to read first.}}</li>
<li>{{Where decisions are recorded.}}</li>
</ul>
<h2>Start here</h2>
<table><thead><tr><th><p>Page</p></th><th><p>What it answers</p></th><th><p>Updated</p></th></tr></thead><tbody>
<tr><td><p><a href="{{url}}">{{title}}</a></p></td><td><p>{{one line}}</p></td><td><p><time datetime="{{date}}">{{date}}</time></p></td></tr>
</tbody></table>
<h2>By section</h2>
<table><thead><tr><th><p>Section</p></th><th><p>Use it for</p></th></tr></thead><tbody>
<tr><td><p><a href="{{url}}">{{Section overview}}</a></p></td><td><p>{{one line}}</p></td></tr>
</tbody></table>
<h2>Archived or superseded</h2>
<table><thead><tr><th><p>Page</p></th><th><p>Replaced by</p></th><th><p>Date</p></th></tr></thead><tbody>
<tr><td><p>{{old page}}</p></td><td><p><a href="{{url}}">{{new page}}</a></p></td><td><p>{{date}}</p></td></tr>
</tbody></table>
```
