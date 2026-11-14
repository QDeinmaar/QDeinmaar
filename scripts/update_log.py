#!/usr/bin/env python3
"""Refresh assets/log.svg with the latest public commits.

Uses the public events API. Set GITHUB_TOKEN to avoid rate limits (the
workflow passes the built-in token). Falls back to --sample for offline tests.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_assets  # noqa: E402

USER = gen_assets.HANDLE


def age(ts):
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    s = int((datetime.now(timezone.utc) - t).total_seconds())
    for unit, n in (("d", 86400), ("h", 3600), ("m", 60)):
        if s >= n:
            return f"{s // n}{unit} ago"
    return "now"


def fetch():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/events/public?per_page=100",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-log"},
    )
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def entries_from(events):
    out = []
    for e in events:
        if e.get("type") != "PushEvent":
            continue
        for c in reversed(e["payload"].get("commits", [])):
            msg = c["message"].splitlines()[0]
            out.append((c["sha"][:7], e["repo"]["name"], msg, age(e["created_at"])))
    return out


if __name__ == "__main__":
    if "--sample" in sys.argv:
        ents = [
            ("a3f9c2e", "QDeinmaar/AI_Rev_agent", "add ghidra headless wrapper", "2h ago"),
            ("7be41d0", "QDeinmaar/EDR", "hook NtCreateThreadEx telemetry", "1d ago"),
            ("c0ffee1", "QDeinmaar/ST4F1T_CTF", "writeup: affine cipher key recovery", "3d ago"),
        ]
    else:
        try:
            ents = entries_from(fetch())
        except Exception as ex:  # keep the old image if the API is unreachable
            print("fetch failed:", ex)
            sys.exit(0)
    if ents:
        gen_assets.main(entries=ents, only_log=True)
    else:
        print("no recent commits; leaving log.svg untouched")
