#!/usr/bin/env python3
"""Generate the terminal-style SVG assets for the profile README.

Edit the CONFIG block, then run:  python3 scripts/gen_assets.py
Output goes to ./assets/. Static renderers show the final state of every
animation, so the images still read correctly when animation is disabled.
"""
import os
import textwrap
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# ----------------------------------------------------------------------------
# CONFIG - edit freely
# ----------------------------------------------------------------------------
HANDLE = "QDeinmaar"
NAME = "ARGON"
HOST = "argon@qdeinmaar"

HEADER_LINES = [
    ("whoami", "argon // cs engineering student"),
    ("cat focus.txt", "reverse engineering | cryptography | offensive security"),
    ("echo $CREED", "break it to understand it. understand it to secure it."),
]

NOW_LINES = [
    ("learning", "reverse engineering, applied cryptography"),
    ("building", "AI_Rev_agent, EDR"),
    ("playing", "CTFs, then writing up every one of them"),
]

PROJECTS = [
    {
        "file": "project-st4f1t.svg",
        "name": "ST4F1T_CTF",
        "tags": ["crypto", "ctf", "writeup"],
        "desc": "Post-event crypto writeup. Dead ends included: leetspeak, ROT, "
                "Caesar. Then a many-to-one hint from repeated letters, an "
                "affine cipher, and a brute-forced key.",
        "link": "github.com/QDeinmaar/ST4F1T_CTF",
    },
    {
        "file": "project-aes.svg",
        "name": "aes-gcm-256",
        "tags": ["crypto", "c", "aes-gcm"],
        "desc": "Encrypt and decrypt tool built around AES-256-GCM, "
                "written in C.",
        "link": "github.com/QDeinmaar/Simple-encryption-decryption-aes-gcm-256-code",
    },
    {
        "file": "project-ai-rev-agent.svg",
        "name": "AI_Rev_agent",
        "tags": ["reverse-engineering", "ai-agent"],
        "desc": "An AI agent for reverse engineering work.",
        "link": "github.com/QDeinmaar/AI_Rev_agent",
    },
    {
        "file": "project-edr.svg",
        "name": "EDR",
        "tags": ["security", "detection"],
        "desc": "An endpoint detection and response project.",
        "link": "github.com/QDeinmaar/EDR",
    },
]

STACK = [
    ("langs", "c, c++, python, java, javascript, php, html, css"),
    ("web", "node.js, next.js, laravel, sqlite"),
    ("re/sec", "ghidra, gdb, x64dbg, wireshark, burp suite, cyberchef"),
]

FOOTER = "break it. understand it. secure it."

# ----------------------------------------------------------------------------
# Theme
# ----------------------------------------------------------------------------
BG = "#0a0e0a"
PANEL = "#0d130d"
EDGE = "#1f3a26"
GREEN = "#39ff88"
DIM = "#5f8a6b"
TEXT = "#c9d8cc"
AMBER = "#ffb454"
RED = "#ff4d6d"
CYAN = "#34e5ff"
FONT = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"
CW = 8.45  # approx glyph width at 14px


def esc(s):
    return escape(s, {'"': "&quot;"})


STYLE = f"""
<style>
  text {{ font-family: {FONT}; font-size: 14px; fill: {TEXT}; }}
  .dim {{ fill: {DIM}; }}
  .g {{ fill: {GREEN}; }}
  .a {{ fill: {AMBER}; }}
  .b {{ font-weight: 700; }}
  .t {{ animation: type 1.1s steps(40) backwards; }}
  .cur {{ animation: blink 1s steps(1) infinite; }}
  .fade {{ animation: fade .6s ease-out backwards; }}
  .gl1 {{ animation: gl1 3.2s steps(1) infinite; }}
  .gl2 {{ animation: gl2 3.2s steps(1) infinite; }}
  @keyframes type {{ from {{ width: 0; }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes fade {{ from {{ opacity: 0; }} }}
  @keyframes gl1 {{ 0%,92%,100% {{ transform: translate(0,0); }}
                    93% {{ transform: translate(-3px,1px); }}
                    96% {{ transform: translate(3px,-1px); }} }}
  @keyframes gl2 {{ 0%,92%,100% {{ transform: translate(0,0); }}
                    94% {{ transform: translate(3px,-1px); }}
                    97% {{ transform: translate(-3px,1px); }} }}
</style>
"""


def defs(w, h, uid):
    return f"""
<defs>
  <pattern id="scan{uid}" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity="0.18"/>
  </pattern>
  <linearGradient id="bar{uid}" x1="0" x2="1">
    <stop offset="0" stop-color="{EDGE}"/><stop offset="1" stop-color="{PANEL}"/>
  </linearGradient>
</defs>
"""


def window(w, h, title, body, uid):
    """Terminal chrome around body markup."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
{STYLE}{defs(w, h, uid)}
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="8" fill="{BG}" stroke="{EDGE}"/>
<path d="M1 8a7 7 0 0 1 7-7h{w-16}a7 7 0 0 1 7 7v22H1z" fill="url(#bar{uid})"/>
<circle cx="20" cy="16" r="5" fill="{RED}"/>
<circle cx="38" cy="16" r="5" fill="{AMBER}"/>
<circle cx="56" cy="16" r="5" fill="{GREEN}"/>
<text x="{w/2}" y="20" text-anchor="middle" class="dim" style="font-size:12px">{esc(title)}</text>
{body}
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" fill="url(#scan{uid})" pointer-events="none"/>
</svg>
"""


def typed(x, y, n_chars, delay, uid, inner):
    """A text line revealed by a growing clip rect."""
    cid = f"c{uid}"
    wpx = n_chars * CW + 8
    return (
        f'<clipPath id="{cid}"><rect class="t" style="animation-delay:{delay}s" '
        f'x="{x}" y="{y-16}" width="{wpx:.0f}" height="22"/></clipPath>'
        f'<g clip-path="url(#{cid})">{inner}</g>'
    )


def prompt_line(y, host, cmd, out, delay, uid, x=24):
    p = f"{host}:~$ "
    cmd_x = x + len(p) * CW
    s = typed(x, y, len(p) + len(cmd), delay, uid + "a",
              f'<text x="{x}" y="{y}" class="g">{esc(p)}</text>'
              f'<text x="{cmd_x:.1f}" y="{y}">{esc(cmd)}</text>')
    s += (f'<g class="fade" style="animation-delay:{delay+1.1}s">'
          f'<text x="{x}" y="{y+22}" class="dim">&gt; </text>'
          f'<text x="{x+2*CW:.1f}" y="{y+22}" class="a">{esc(out)}</text></g>')
    return s


# ----------------------------------------------------------------------------
# Assets
# ----------------------------------------------------------------------------
def header():
    w, h = 880, 330
    body = []
    # glitch title
    ty = 98
    body.append(f'<text x="24" y="{ty}" class="gl1" style="font-size:64px;font-weight:800;fill:{CYAN};opacity:.55" letter-spacing="6">{NAME}</text>')
    body.append(f'<text x="24" y="{ty}" class="gl2" style="font-size:64px;font-weight:800;fill:{RED};opacity:.55" letter-spacing="6">{NAME}</text>')
    body.append(f'<text x="24" y="{ty}" style="font-size:64px;font-weight:800;fill:{GREEN}" letter-spacing="6">{NAME}</text>')
    body.append(f'<text x="{w-24}" y="{ty-30}" text-anchor="end" class="dim" style="font-size:12px">uid=1000({HANDLE}) gid=1000(root-in-progress)</text>')
    y = 148
    d = 0.3
    for i, (cmd, out) in enumerate(HEADER_LINES):
        body.append(prompt_line(y, HOST, cmd, out, d, f"h{i}"))
        y += 52
        d += 1.7
    body.append(f'<text x="24" y="{y}" class="g">{esc(HOST)}:~$ </text>')
    cx = 24 + (len(HOST) + 4) * CW
    body.append(f'<rect class="cur" x="{cx:.1f}" y="{y-13}" width="9" height="17" fill="{GREEN}"/>')
    return window(w, h, f"{HOST}: ~", "\n".join(body), "hd")


def now():
    w = 880
    h = 84 + 28 * len(NOW_LINES)
    body = [f'<text x="24" y="52" class="g b">$ ./now.sh</text>']
    y = 80
    for i, (k, v) in enumerate(NOW_LINES):
        body.append(
            f'<g class="fade" style="animation-delay:{0.2+i*0.35}s">'
            f'<text x="24" y="{y}" class="dim">[</text>'
            f'<text x="{24+CW:.1f}" y="{y}" class="a">{esc(k)}</text>'
            f'<text x="{24+(len(k)+1)*CW:.1f}" y="{y}" class="dim">]</text>'
            f'<text x="{24+(len(k)+3)*CW:.1f}" y="{y}">{esc(v)}</text></g>')
        y += 28
    return window(w, h, "now", "\n".join(body), "nw")


def project(p, idx):
    w = 432
    wrapped = textwrap.wrap(p["desc"], 46)
    max_lines = max(len(textwrap.wrap(q["desc"], 46)) for q in PROJECTS)
    h = 138 + 20 * max_lines  # same height for every card
    body = [f'<text x="20" y="56" class="g b">~/{esc(p["name"])}</text>']
    tags = " ".join(f"[{t}]" for t in p["tags"])
    body.append(f'<text x="20" y="80" class="a" style="font-size:12px">{esc(tags)}</text>')
    y = 108
    for line in wrapped:
        body.append(f'<text x="20" y="{y}">{esc(line)}</text>')
        y += 20
    link = p["link"] if len(p["link"]) <= 48 else p["link"][:45] + "..."
    body.append(f'<text x="20" y="{h-16}" class="dim" style="font-size:12px">{esc(link)}</text>')
    return window(w, h, p["name"], "\n".join(body), f"p{idx}")


def stack():
    w = 880
    rows = []
    for k, v in STACK:
        rows.append((k, textwrap.wrap(v, 86)))
    lines = sum(len(r[1]) for r in rows)
    h = 70 + 24 * lines + 12 * len(rows)
    body = [f'<text x="24" y="52" class="g b">$ cat stack.txt</text>']
    y = 80
    for k, ls in rows:
        body.append(f'<text x="24" y="{y}" class="a">{esc(k.ljust(7))}</text>')
        for j, ln in enumerate(ls):
            body.append(f'<text x="{24+8*CW:.1f}" y="{y}">{esc(ln)}</text>')
            y += 24
        y += 12
    return window(w, h, "stack", "\n".join(body), "st")


def log(entries=None):
    """entries: list of (sha, repo, message, age)"""
    w = 880
    if not entries:
        entries = [("0000000", HANDLE + "/...", "waiting for the first daily refresh", "now")]
    entries = entries[:8]
    h = 70 + 24 * len(entries)
    body = [f'<text x="24" y="52" class="g b">$ git log --all --oneline -n {len(entries)}</text>']
    y = 80
    for i, (sha, repo, msg, age) in enumerate(entries):
        repo = repo.split("/")[-1][:20]
        msg = msg if len(msg) <= 52 else msg[:49] + "..."
        body.append(
            f'<g class="fade" style="animation-delay:{0.1+i*0.15}s">'
            f'<text x="24" y="{y}" class="a">{esc(sha)}</text>'
            f'<text x="{24+9*CW:.1f}" y="{y}" class="g">{esc(repo.ljust(20))}</text>'
            f'<text x="{24+30*CW:.1f}" y="{y}">{esc(msg)}</text>'
            f'<text x="{w-24}" y="{y}" text-anchor="end" class="dim">{esc(age)}</text></g>')
        y += 24
    return window(w, h, "git log", "\n".join(body), "lg")


def footer():
    w, h = 880, 84
    body = (f'<text x="{w/2}" y="62" text-anchor="middle" class="dim">~ {esc(FOOTER)} ~</text>')
    return window(w, h, "exit 0", body, "ft")


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.normpath(path))


def main(entries=None, only_log=False):
    os.makedirs(OUT, exist_ok=True)
    if only_log:
        write("log.svg", log(entries))
        return
    write("header.svg", header())
    write("now.svg", now())
    for i, p in enumerate(PROJECTS):
        write(p["file"], project(p, i))
    write("stack.svg", stack())
    write("log.svg", log(entries))
    write("footer.svg", footer())


if __name__ == "__main__":
    main()
