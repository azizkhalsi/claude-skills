#!/usr/bin/env python3
"""Confluence Cloud helper for the confluence-docs skill. Standard library only.

Commands
  whoami                                  check the token: display name and account id
  space KEY                               space id and homepage id for a space key
  get ID [--out FILE]                     title, version, parent; storage body to FILE (or stdout)
  children ID                             child pages (id, title, version date), recursively with --tree
  search CQL                              search pages with CQL (title, id, last updated)
  create --space KEY|--space-id ID --parent ID --title T --file BODY.html
  update ID --file BODY.html [--title T] [--message M] [--allow-media-loss]
  upload ID FILE... [--comment C]         attach files (new version when the name exists)
  attachments ID                          attachments of a page
  archive ID...                           archive pages (asks for confirmation)

Auth: CONFLUENCE_SITE (e.g. your-site.atlassian.net), CONFLUENCE_EMAIL and CONFLUENCE_API_TOKEN, or the
macOS keychain item "Confluence API" for that email. The token is never printed.
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid


def die(msg, code=2):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def token():
    value = os.environ.get("CONFLUENCE_API_TOKEN", "").strip()
    if value:
        return value
    email = os.environ.get("CONFLUENCE_EMAIL", "").strip()
    if sys.platform == "darwin" and email:
        proc = subprocess.run(["security", "find-generic-password", "-s", "Confluence API", "-a", email, "-w"],
                              capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    die("no token: set CONFLUENCE_API_TOKEN, or store it in the keychain as service 'Confluence API' for CONFLUENCE_EMAIL")


class Client:
    def __init__(self):
        self.site = os.environ.get("CONFLUENCE_SITE", "").strip().replace("https://", "").rstrip("/")
        self.email = os.environ.get("CONFLUENCE_EMAIL", "").strip()
        if not self.site or not self.email:
            die("set CONFLUENCE_SITE (e.g. your-site.atlassian.net) and CONFLUENCE_EMAIL")
        cred = base64.b64encode(f"{self.email}:{token()}".encode()).decode()
        self.auth = f"Basic {cred}"

    def call(self, method, path, body=None, params=None, raw=None, content_type=None, extra_headers=None):
        url = f"https://{self.site}{path}"
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        headers = {"Authorization": self.auth, "Accept": "application/json", "User-Agent": "confluence-docs-skill"}
        if data is not None:
            headers["Content-Type"] = content_type or "application/json"
        headers.update(extra_headers or {})
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                text = r.read().decode()
                return r.status, (json.loads(text) if text.strip() else {})
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")
            die(f"HTTP {e.code} on {method} {path}: {text[:800]}")

    # v2 pages
    def page(self, page_id, body=True):
        params = {"include-version": "true"}
        if body:
            params["body-format"] = "storage"
        _, data = self.call("GET", f"/wiki/api/v2/pages/{page_id}", params=params)
        return data

    def page_url(self, data):
        links = data.get("_links", {})
        base = links.get("base") or f"https://{self.site}/wiki"
        return base + (links.get("webui") or f"/pages/{data.get('id')}")


MEDIA_RE = re.compile(r'ri:filename="([^"]+)"')


def media_names(body):
    return set(MEDIA_RE.findall(body or ""))


def cmd_whoami(c, a):
    _, me = c.call("GET", "/wiki/rest/api/user/current")
    print(f"{me.get('displayName')}  account {me.get('accountId')}  site {c.site}")


def cmd_space(c, a):
    _, data = c.call("GET", "/wiki/api/v2/spaces", params={"keys": a.key})
    results = data.get("results", [])
    if not results:
        die(f"space {a.key} not found")
    s = results[0]
    print(f"{s['key']}  id {s['id']}  homepage {s.get('homepageId')}  name {s.get('name')}")


def cmd_get(c, a):
    data = c.page(a.id)
    body = data.get("body", {}).get("storage", {}).get("value", "")
    ver = data.get("version", {})
    print(f"title    {data.get('title')}")
    print(f"id       {data.get('id')}  parent {data.get('parentId')}  space {data.get('spaceId')}  status {data.get('status')}")
    print(f"version  {ver.get('number')}  {ver.get('createdAt')}  by {ver.get('authorId')}  message: {ver.get('message') or ''}")
    print(f"url      {c.page_url(data)}")
    names = sorted(media_names(body))
    print(f"media    {len(names)} referenced file(s)" + (": " + ", ".join(names) if names else ""))
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"body     written to {a.out} ({len(body)} chars)")
    else:
        print("---- body (storage) ----")
        print(body)


def list_children(c, page_id, depth, tree, prefix=""):
    cursor = None
    while True:
        params = {"limit": 250}
        if cursor:
            params["cursor"] = cursor
        _, data = c.call("GET", f"/wiki/api/v2/pages/{page_id}/children", params=params)
        for ch in data.get("results", []):
            print(f"{prefix}{ch['id']}  {ch.get('title')}  (status {ch.get('status')})")
            if tree and depth < 6:
                list_children(c, ch["id"], depth + 1, tree, prefix + "    ")
        nxt = data.get("_links", {}).get("next")
        if not nxt:
            break
        cursor = urllib.parse.parse_qs(urllib.parse.urlparse(nxt).query).get("cursor", [None])[0]
        if not cursor:
            break


def cmd_children(c, a):
    list_children(c, a.id, 0, a.tree)


def cmd_search(c, a):
    _, data = c.call("GET", "/wiki/rest/api/search", params={"cql": a.cql, "limit": a.limit})
    for r in data.get("results", []):
        content = r.get("content", {})
        print(f"{content.get('id')}  {content.get('title')}  updated {r.get('lastModified', '')[:10]}  {content.get('type')}")
    print(f"{data.get('size', 0)} result(s)" + (" (more available)" if data.get('_links', {}).get('next') else ""))


def read_body(path):
    with open(path, encoding="utf-8") as f:
        body = f.read()
    if not body.strip():
        die(f"{path} is empty")
    return body


def cmd_create(c, a):
    space_id = a.space_id
    if not space_id:
        _, data = c.call("GET", "/wiki/api/v2/spaces", params={"keys": a.space})
        results = data.get("results", [])
        if not results:
            die(f"space {a.space} not found")
        space_id = results[0]["id"]
    body = read_body(a.file)
    payload = {"spaceId": str(space_id), "status": "current", "title": a.title, "parentId": str(a.parent),
               "body": {"representation": "storage", "value": body}}
    _, data = c.call("POST", "/wiki/api/v2/pages", body=payload)
    print(f"created  {data.get('id')}  version {data.get('version', {}).get('number')}")
    print(f"url      {c.page_url(data)}")
    missing = media_names(body)
    if missing:
        print(f"note     the body references {len(missing)} attachment(s); upload them: {', '.join(sorted(missing))}")


def cmd_update(c, a):
    live = c.page(a.id)
    live_body = live.get("body", {}).get("storage", {}).get("value", "")
    new_body = read_body(a.file)
    lost = media_names(live_body) - media_names(new_body)
    if lost and not a.allow_media_loss:
        die("the new body drops attachment(s) the live page shows: " + ", ".join(sorted(lost)) +
            ". Merge them back, or pass --allow-media-loss if that is intended.")
    if re.search(r'data-local-id=|ac:local-id=', new_body) and not a.keep_local_ids:
        new_body = re.sub(r'\s(?:data-local-id|ac:local-id)="[^"]*"', "", new_body)
    version = live.get("version", {}).get("number")
    if version is None:
        die("could not read the live version number")
    payload = {"id": str(a.id), "status": "current", "title": a.title or live.get("title"),
               "body": {"representation": "storage", "value": new_body},
               "version": {"number": version + 1, "message": a.message or ""}}
    _, data = c.call("PUT", f"/wiki/api/v2/pages/{a.id}", body=payload)
    print(f"updated  {data.get('id')}  version {version} -> {data.get('version', {}).get('number')}")
    print(f"url      {c.page_url(data)}")


def multipart(fields, files):
    boundary = "----confluence-docs-" + uuid.uuid4().hex
    out = bytearray()
    for name, value in fields:
        out += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
    for name, path in files:
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            content = f.read()
        out += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{os.path.basename(path)}\"\r\n"
                f"Content-Type: {ctype}\r\n\r\n").encode() + content + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def cmd_upload(c, a):
    for path in a.files:
        if not os.path.isfile(path):
            die(f"not a file: {path}")
        fields = [("minorEdit", "true")]
        if a.comment:
            fields.append(("comment", a.comment))
        raw, ctype = multipart(fields, [("file", path)])
        _, data = c.call("PUT", f"/wiki/rest/api/content/{a.id}/child/attachment", raw=raw, content_type=ctype,
                         extra_headers={"X-Atlassian-Token": "nocheck"})
        for r in data.get("results", []):
            ext = r.get("extensions", {})
            print(f"uploaded {r.get('title')}  id {r.get('id')}  {ext.get('fileSize', '?')} bytes  {ext.get('mediaType', '')}")
    print(f"reference with: <ac:image ac:align=\"center\" ac:layout=\"center\"><ri:attachment ri:filename=\"NAME\"/></ac:image>")


def cmd_attachments(c, a):
    _, data = c.call("GET", f"/wiki/api/v2/pages/{a.id}/attachments", params={"limit": 250})
    for r in data.get("results", []):
        print(f"{r.get('id')}  {r.get('title')}  {r.get('fileSize', '?')} bytes  {r.get('mediaType', '')}  v{r.get('version', {}).get('number')}")
    print(f"{len(data.get('results', []))} attachment(s)")


def cmd_archive(c, a):
    titles = []
    for pid in a.ids:
        p = c.page(pid, body=False)
        titles.append(f"{pid}  {p.get('title')}")
    print("about to archive:\n  " + "\n  ".join(titles))
    if not a.yes:
        answer = input("type 'archive' to continue: ").strip()
        if answer != "archive":
            print("cancelled")
            return
    _, data = c.call("POST", "/wiki/rest/api/content/archive", body={"pages": [{"id": str(pid)} for pid in a.ids]})
    print("archive request accepted" + (f": {json.dumps(data)[:300]}" if data else ""))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami")
    s = sub.add_parser("space"); s.add_argument("key")
    s = sub.add_parser("get"); s.add_argument("id"); s.add_argument("--out")
    s = sub.add_parser("children"); s.add_argument("id"); s.add_argument("--tree", action="store_true")
    s = sub.add_parser("search"); s.add_argument("cql"); s.add_argument("--limit", type=int, default=50)
    s = sub.add_parser("create"); s.add_argument("--space"); s.add_argument("--space-id"); s.add_argument("--parent", required=True)
    s.add_argument("--title", required=True); s.add_argument("--file", required=True)
    s = sub.add_parser("update"); s.add_argument("id"); s.add_argument("--file", required=True); s.add_argument("--title")
    s.add_argument("--message"); s.add_argument("--allow-media-loss", action="store_true"); s.add_argument("--keep-local-ids", action="store_true")
    s = sub.add_parser("upload"); s.add_argument("id"); s.add_argument("files", nargs="+"); s.add_argument("--comment")
    s = sub.add_parser("attachments"); s.add_argument("id")
    s = sub.add_parser("archive"); s.add_argument("ids", nargs="+"); s.add_argument("--yes", action="store_true")
    a = p.parse_args()
    if a.cmd == "create" and not (a.space or a.space_id):
        die("create needs --space KEY or --space-id ID")
    c = Client()
    {"whoami": cmd_whoami, "space": cmd_space, "get": cmd_get, "children": cmd_children, "search": cmd_search,
     "create": cmd_create, "update": cmd_update, "upload": cmd_upload, "attachments": cmd_attachments,
     "archive": cmd_archive}[a.cmd](c, a)


if __name__ == "__main__":
    main()
