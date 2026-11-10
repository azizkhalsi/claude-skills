# Publishing: connector, REST script, tokens, safe updates, clean-up

Contents: 1. Which path · 2. The connector · 3. Token setup · 4. REST with scripts/confluence.py ·
5. Update safely · 6. Verify · 7. Archive, merge, entry page · 8. Endpoints used

## 1. Which path

| Need | Use |
|---|---|
| Text, tables, panels, native diagram, and the connector is connected | The connector (HTML dialect) |
| Images, PDFs, any attachment | The script (REST, storage format). The connector cannot upload |
| Listing a page tree, searching, archiving many pages | Either: the connector has `getConfluencePageDescendants` and `searchConfluenceUsingCql`; the script has `children`, `search`, `archive` |
| No connector in the session and no API token yet | Prepare the body in a file, ask for one of the two |

## 2. The connector

The Atlassian MCP connector exposes `getConfluencePage`, `getConfluencePageDescendants`,
`searchConfluenceUsingCql`, `createConfluencePage`, `updateConfluencePage` and `getContentFormatGuide`.
Site hostname works as `cloudId` (for example `your-site.atlassian.net`); a space key works as
`spaceId`.

- Call `getContentFormatGuide` with the tool name before writing the first body; author in its HTML
  dialect (`references/page-formats.md`). Storage XML renders as raw text.
- `updateConfluencePage` replaces the whole body: fetch with `contentFormat: "html"` first, merge,
  then send. Keep the fetched `data-local-id` attributes of that page; never copy ids between pages.
- On a 500, remove ids you did not fetch from that page and retry once.
- It cannot attach files. Draw natively, or upload with the script, or hand the owner the file.
- The create and update responses include the stored body: read it once to check that panels, layouts
  and code blocks were understood (they come back as `ac:structured-macro` and `ac:layout`).

## 3. Token setup for the REST path (once per person)

A token acts as the person who created it. Each person uses their own; never a token found in a repo
or in someone else's environment, because every edit would be signed with the wrong name.

1. Create a token: Atlassian account → Security → API tokens → Create API token
   (https://id.atlassian.com/manage-profile/security/api-tokens). Give it a name and an expiry.
2. Store it where no command prints it:
   - macOS keychain: `security add-generic-password -s "Confluence API" -a you@company.com -w` (it
     prompts for the value), or
   - a `0600` file in your home that you `source`, exporting the variables below.
3. The script reads, in this order: `CONFLUENCE_API_TOKEN` from the environment, else the keychain
   item "Confluence API" for `CONFLUENCE_EMAIL`. It never echoes the value.

Environment variables: `CONFLUENCE_SITE` (for example `your-site.atlassian.net`), `CONFLUENCE_EMAIL`,
`CONFLUENCE_API_TOKEN` (optional with the keychain).

Check the token: `python3 scripts/confluence.py whoami` prints your display name and account id.

## 4. REST with scripts/confluence.py

```bash
S=path/to/confluence-docs/scripts/confluence.py
export CONFLUENCE_SITE=your-site.atlassian.net CONFLUENCE_EMAIL=you@company.com

python3 $S whoami
python3 $S space ENG                                   # space id for the key
python3 $S children 123456 --tree                      # the page tree under a parent
python3 $S get 123456 --out live.html                  # title, version, parent, body to a file
python3 $S search 'space = ENG and title ~ "deploy" and type = page'
python3 $S create --space ENG --parent 123456 --title "Macros: nightly embedding" --file page.html
python3 $S update 123456 --file page.html --message "PROJ-123: switch moved to Settings"
python3 $S upload 123456 diagrams/flow.png --comment "PROJ-123"
python3 $S attachments 123456
python3 $S archive 234567 345678                       # archive pages (asks for confirmation)
```

`create` and `update` take storage-format bodies. `update` fetches the live page, compares the
attachments referenced in the live body with the new body, and stops if some would disappear
(override with `--allow-media-loss` only when that is the intent). Every write prints the page URL and
the new version number so the result can be checked.

## 5. Update safely

People add images and comments to pages between your edits, often within minutes of publication. A
blind republish removes them. The procedure:

1. Fetch the live body (connector `getConfluencePage` in html, or `confluence.py get`). Note the
   version, every media node and every inline comment marker.
2. Apply your change to that live body, not to your last local copy.
3. Publish with a version message that names the ticket and the change.
4. Fetch again, or open the page, and check that the images and comments are still there.

Same rule for other people's sections: do not rewrite a decision panel or a dated section someone else
wrote; add a new dated panel or a row. When you add a page to a section, add it to the section
overview's list as well, with the version message naming the ticket.

## 6. Verify

After every publish: open the page URL. Check the first screen (purpose, status table, "In one
minute"), the tables (header row rendered, no empty rows), the diagram, the links (one click on each
new link), and that no secret or personal data slipped in. Then link the page from the ticket and
post the short comment.

## 7. Archive, merge, entry page

Space clean-up is a judgement call on other people's work, so propose before doing:

1. List every page of the section with id, title, owner and last-modified date (connector
   `getConfluencePageDescendants` with `depth`, or `confluence.py children --tree`).
2. Mark each page: keep, update (stale facts), merge into X, archive (superseded). Put the list in a
   table with the reason per page and share it with the owners before archiving anything that is not
   yours. Pages already in a History folder need nothing.
3. Merge = move the still-true rows into the surviving page, add a one-line "Superseded by" note on
   the old page, then archive the old page. Archived pages stay searchable and can be restored.
4. The entry page lists only the pages that remain, grouped by section, with the newest marked. Keep
   an "Archived or superseded" table on it for the first weeks so old links still make sense.

`confluence.py archive <ids...>` calls the archive endpoint after a confirmation prompt.

## 8. Endpoints used (checked against Atlassian's published specs, Nov 2026)

- v2 `GET /wiki/api/v2/pages/{id}?body-format=storage&include-version=true`
- v2 `POST /wiki/api/v2/pages` body `{spaceId, status: "current", title, parentId, body: {representation: "storage", value}}`
- v2 `PUT /wiki/api/v2/pages/{id}` body `{id, status: "current", title, body: {...}, version: {number, message}}` (required: id, status, title, body, version)
- v2 `GET /wiki/api/v2/pages/{id}/children`, `GET /wiki/api/v2/pages/{id}/attachments`, `GET /wiki/api/v2/spaces?keys=KEY`
- v1 `PUT /wiki/rest/api/content/{id}/child/attachment` multipart `file`, `minorEdit`, optional `comment`, header `X-Atlassian-Token: nocheck` (create or update by file name)
- v1 `GET /wiki/rest/api/search?cql=...`, `GET /wiki/rest/api/user/current`, `POST /wiki/rest/api/content/archive` body `{pages: [{id}]}`
- Auth: HTTP Basic with email and API token.
