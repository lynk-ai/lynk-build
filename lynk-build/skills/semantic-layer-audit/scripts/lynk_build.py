#!/usr/bin/env python3
"""Trigger / read Lynk semantic-layer builds — the AUTHORITATIVE verification surface.

Reads the API token from an .env file (never prints it). The .env path and API base
are configurable via env so no secret or tenant path is ever hard-coded.

    LYNK_ENV=/path/to/.env \
    LYNK_API_BASE=<your Lynk API base>/semantics \
    uv run --with requests python3 lynk_build.py <cmd> [args]

LYNK_ENV defaults to `.env` in the current working directory; LYNK_API_BASE defaults
to the prod base. Note: this duplicates lynk_api.py's build trigger (POST
semantics/builds); converging on one builder is a known follow-up.

Commands:
    probe                 GET openapi.json + list builds — confirm base URL + auth (read-only)
    list [branch]         GET /builds  (optionally filter by branch)
    build <branch> [-f]   POST /builds?branch=...  (TRIGGERS a build of that branch's HEAD)
    get <build_id>        GET /builds/{id}  (full issues)

Only prints status + build issues. Never prints the token.
"""
import json
import os
import sys
from pathlib import Path
from urllib import request, error, parse

TOKEN_KEY = "LYNK_API_TOKEN"


def load_token() -> str:
    env_path = Path(os.path.expanduser(os.environ.get("LYNK_ENV", ".env")))
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == TOKEN_KEY:
            return _normalize(v.strip().strip("'").strip('"'))
    raise SystemExit(f"error: {TOKEN_KEY} not found in {env_path}")


def _normalize(v: str) -> str:
    """Accept raw JWT, 'Bearer <jwt>', or the JSON form {'Authorization': 'Bearer <jwt>'}."""
    v = v.strip()
    if v.startswith("{"):
        try:
            v = json.loads(v).get("Authorization", v)
        except Exception:  # noqa: BLE001
            pass
    while v.lower().startswith("bearer "):
        v = v[len("bearer "):].strip()
    return v.strip().strip("'").strip('"')


BASE = os.environ.get("LYNK_API_BASE", "https://app.getlynk.ai/api/semantics").rstrip("/")


def call(method: str, path: str, token: str, params: dict | None = None):
    url = f"{BASE}{path}"
    if params:
        url += "?" + parse.urlencode(params)
    req = request.Request(url, method=method)
    # API tokens authenticate via the x-api-key header (openapi ApiKeyAuth scheme).
    # Do NOT also send Authorization: Bearer — an opaque (non-JWT) key there can make
    # the middleware reject on the bearer check before it reaches x-api-key.
    req.add_header("x-api-key", token)
    req.add_header("Accept", "application/json")
    try:
        with request.urlopen(req, timeout=120) as r:
            return r.status, r.read().decode()
    except error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:  # noqa: BLE001
        return None, f"CONNECTION ERROR: {type(e).__name__}: {e}"


def show_issues(body: str) -> None:
    try:
        b = json.loads(body)
    except Exception:  # noqa: BLE001
        print(body[:2000]); return
    if "detail" in b and isinstance(b["detail"], dict):
        b = b["detail"]
    print(f"status={b.get('status')}  branch={b.get('branch')}  id={b.get('id')}")
    issues = b.get("validation_issues") or b.get("issues") or b.get("errors") or []
    print(f"validation_issues: {len(issues)}")
    from collections import Counter
    cats = Counter(i.get("category") for i in issues if isinstance(i, dict))
    sev = Counter(i.get("severity") for i in issues if isinstance(i, dict))
    print(f"  by severity: {dict(sev)}   by category: {dict(cats)}")
    for i in issues[:40]:
        if isinstance(i, dict):
            loc = (i.get("location") or {}).get("file_path", "")
            print(f"  [{i.get('severity','?')}/{i.get('category','?')}] {loc}: {i.get('message','')}")
        else:
            print(f"  {i}")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__); return 2
    cmd = sys.argv[1]
    token = load_token()
    print(f"(base={BASE}, token=***{'set' if token else 'MISSING'}***)")

    if cmd == "probe":
        for path in ("/openapi.json", "/builds"):
            code, body = call("GET", path, token)
            head = body[:200].replace("\n", " ")
            print(f"GET {path} -> {code}  {head}")
        return 0
    if cmd == "list":
        params = {"branch": sys.argv[2]} if len(sys.argv) > 2 else None
        code, body = call("GET", "/builds", token, params); print(f"-> {code}"); print(body[:2000]); return 0
    if cmd == "build":
        if len(sys.argv) < 3:
            print("usage: build <branch> [-f]"); return 2
        params = {"branch": sys.argv[2]}
        if "-f" in sys.argv or "--force" in sys.argv:
            params["force"] = "true"
        code, body = call("POST", "/builds", token, params)
        print(f"POST /builds -> {code}"); show_issues(body); return 0 if code in (200, 202) else 1
    if cmd == "get":
        code, body = call("GET", f"/builds/{sys.argv[2]}", token); print(f"-> {code}"); show_issues(body); return 0
    print(f"unknown command: {cmd}"); return 2


if __name__ == "__main__":
    raise SystemExit(main())
