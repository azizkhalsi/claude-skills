# Page formats: the connector's HTML dialect and the REST storage format

Two ways to write a Confluence body, and they are not interchangeable:

| Path | Body format | Tell-tale markup |
|---|---|---|
| Atlassian MCP connector (`createConfluencePage`, `updateConfluencePage`) | Its HTML dialect, described by `getContentFormatGuide` | `<div data-type="panel-info">`, `<section data-type="layout-two-equal">`, `<span data-type="status">` |
| REST API (`scripts/confluence.py`, `body-format=storage`) | Confluence storage format (XHTML with `ac:` and `ri:` namespaces) | `<ac:structured-macro ac:name="info">`, `<ac:layout>`, `<ri:attachment>` |

Storage XML sent through the connector renders as raw text. Connector HTML sent through REST as
"storage" is rejected or mangled. When unsure how the editor stores an element, fetch an existing page
that has it, in the format you are going to write, and copy the exact markup.

Contents: 1. Element table (both dialects) · 2. Native diagram recipe · 3. Images · 4. Rules that
apply to both · 5. Connector specifics · 6. Storage specifics

## 1. Element table

| Element | Connector HTML dialect | Storage format |
|---|---|---|
| Status lozenge | `<span data-type="status" data-color="green">Live</span>` (colors: neutral, purple, blue, red, yellow, green) | `<ac:structured-macro ac:name="status"><ac:parameter ac:name="colour">Green</ac:parameter><ac:parameter ac:name="title">Live</ac:parameter></ac:structured-macro>` |
| Info / note / warning / success panel | `<div data-type="panel-info"><p>…</p></div>` (`panel-note`, `panel-warning`, `panel-success`, `panel-error`) | `<ac:structured-macro ac:name="info"><ac:parameter ac:name="title">Scope</ac:parameter><ac:rich-text-body><p>…</p></ac:rich-text-body></ac:structured-macro>` (`note`, `warning`, `tip`) |
| Custom panel (colour + emoji) | `<div data-type="panel-custom" data-icon=":robot:" data-icon-id="1f916" data-icon-text="🤖" data-color="#EAE6FF"><p>…</p></div>` | `<ac:structured-macro ac:name="panel"><ac:parameter ac:name="bgColor">#EAE6FF</ac:parameter><ac:parameter ac:name="panelIcon">:robot:</ac:parameter><ac:parameter ac:name="panelIconId">1f916</ac:parameter><ac:parameter ac:name="panelIconText">🤖</ac:parameter><ac:rich-text-body><p>…</p></ac:rich-text-body></ac:structured-macro>` |
| Two or three columns | `<section data-type="layout-three-equal" data-breakout="wide"><div data-type="column">…</div>…</section>` (`layout-two-equal`, `layout-two-left-sidebar`, `layout-two-right-sidebar`, `layout-three-with-sidebars`) | `<ac:layout><ac:layout-section ac:type="three_equal"><ac:layout-cell>…</ac:layout-cell>…</ac:layout-section></ac:layout>` (`two_equal`, `two_left_sidebar`, `two_right_sidebar`, `three_with_sidebars`) |
| Table | `<table><thead><tr><th><p>H</p></th></tr></thead><tbody><tr><td><p>cell</p></td></tr></tbody></table>` (wrap cell text in `<p>`) | `<table><tbody><tr><th>H</th></tr><tr><td>cell</td></tr></tbody></table>` |
| Code block | `<pre><code class="language-sql">select 1;</code></pre>` (escape `<` and `>` as `&lt;` `&gt;`) | `<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">sql</ac:parameter><ac:plain-text-body><![CDATA[select 1;]]></ac:plain-text-body></ac:structured-macro>` |
| Expand (fold detail) | `<details><summary>Full SQL</summary><p>…</p></details>` | `<ac:structured-macro ac:name="expand"><ac:parameter ac:name="title">Full SQL</ac:parameter><ac:rich-text-body>…</ac:rich-text-body></ac:structured-macro>` |
| Date | `<time datetime="2026-11-10">10 Nov 2026</time>` (renders as a date chip) | plain text, or the same `<time>` element |
| Link in a sentence | `<a href="URL">text</a>` | same |
| Link in a sources list | `<a href="URL" data-card-appearance="inline"></a>` (smart link, empty anchor) | `<ac:link><ri:page ri:space-key="KEY" ri:content-title="Title"/></ac:link>` or a plain `<a href>` |
| Table of contents | `<div data-type="extension" data-extension-key="toc" data-extension-type="com.atlassian.confluence.macro.core" data-parameters='{"macroParams":{"maxLevel":{"value":"2"}}}'></div>` | `<ac:structured-macro ac:name="toc"><ac:parameter ac:name="maxLevel">2</ac:parameter></ac:structured-macro>` |
| Centred text | `<p style="text-align: center">⬇</p>` | `<p style="text-align: center;">⬇</p>` |
| Image (uploaded attachment) | `<figure data-type="media-single" data-layout="center" data-width="80" data-width-type="percentage"><div data-type="media" data-media-type="file" data-id="MEDIA_ID" data-collection="contentId-PAGEID" data-alt="x.png"></div></figure>` (ids come from the upload response or a fetched page; never invent them) | `<ac:image ac:align="center" ac:layout="center" ac:width="900"><ri:attachment ri:filename="x.png"/></ac:image>` |

Palette colours that render well for custom panels and cell backgrounds: `#EAE6FF` (purple),
`#E3FCEF` (green), `#DEEBFF` (blue), `#FFFAE6` (yellow), `#FFEBE6` (red), `#F4F5F7` (grey).

## 2. Native diagram recipe

A flow with 3 to 6 steps, no attachment, survives edits:

1. One three-column (or two-column) layout section per row of steps, `data-breakout="wide"`.
2. One custom panel per step: title ending with "➜" when it leads to the next, a colour per kind of
   actor (people yellow, the system purple, data stores blue, external systems grey, fixes green).
3. Between rows, a centred paragraph with "⬇".
4. For a contrast ("kept" vs "never kept", "sent" vs "never sent"), a two-column section with a success
   panel on the left and a warning panel on the right.
5. Keep each panel to a title and one or two short lines; the reader should get the flow in five
   seconds. Details go in the table below the diagram.

Connector example (one row):

```html
<section data-type="layout-three-equal" data-breakout="wide">
  <div data-type="column"><div data-type="panel-custom" data-icon=":inbox_tray:" data-icon-id="1f4e5" data-icon-text="📥" data-color="#FFFAE6"><p><strong>1. A run starts ➜</strong></p><p>one short line</p></div></div>
  <div data-type="column"><div data-type="panel-custom" data-icon=":robot:" data-icon-id="1f916" data-icon-text="🤖" data-color="#EAE6FF"><p><strong>2. During the run ➜</strong></p><p>one short line</p></div></div>
  <div data-type="column"><div data-type="panel-custom" data-icon=":floppy_disk:" data-icon-id="1f4be" data-icon-text="💾" data-color="#DEEBFF"><p><strong>3. At the end</strong></p><p>one short line</p></div></div>
</section>
<p style="text-align: center">⬇</p>
```

The same flow can be kept as Mermaid in the repository for slides (`scripts/render_diagram.sh`).

## 3. Images

- REST: upload with `scripts/confluence.py upload <page-id> diagram.png`, then reference by file name
  with `<ac:image>`. Re-uploading the same name creates a new version; the page shows the newest.
- Connector: it cannot upload. Either draw natively, upload with the script and reference the media
  id, or hand the owner the file.
- An image referenced before its upload shows as broken until the file exists.

## 4. Rules that apply to both

- Header row with `<th>`; one idea per cell; avoid merged cells (they break the column tools).
- Panels cannot hold tables; alignment inside panels is not reliable.
- Headings no deeper than `h3`; if you need `h4`, split the page.
- Colour is never the only signal: always a word too ("Live", "Failed").
- No `style` or `class` attributes beyond the ones listed; the editor drops or mangles them.
- Lists, cells, panels and columns must hold at least one child.

## 5. Connector specifics

- Call `getContentFormatGuide` with the tool name before the first body of a session; the dialect
  evolves and the guide is authoritative.
- Fetched pages come back with `data-local-id` on every node. Keep the ids of the page you are
  editing; never copy ids from one page into another and never invent them. Omit ids on new nodes.
- `panel-warning` may be stored as a `note` (yellow) panel; use `panel-error` when red is needed.
- `<time>` loses its inner text and renders as a date chip: that is expected.
- Bare URLs in lists become smart links by default; use `<a href>` with text only inside sentences.

## 6. Storage specifics

- The body is XHTML: close every tag, escape `&` as `&amp;`, keep the `ac:`/`ri:` prefixes.
- `ac:local-id` and `ac:macro-id` attributes from a fetched page can be kept; omit them on new macros
  (Confluence generates them).
- Status colours are capitalised words: `Grey`, `Red`, `Yellow`, `Green`, `Blue`, `Purple`.
- A page link by title survives moves; a link by URL survives renames. Either is fine.
