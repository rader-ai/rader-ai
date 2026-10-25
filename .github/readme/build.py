"""Build the profile README visuals: the shipping-log hero and the receipts chart.

    python3 .github/readme/build.py

Made with github-readme-designer (svgkit.py is vendored from it). Every log
entry and number below is real: repo creation dates from GitHub, results from
each repo's published evals.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import svgkit as sk  # noqa: E402

OUT = HERE.parent / "assets"

# Light: a baseball scorebook. Dark: the dugout chalkboard.
THEMES = {
    "light": dict(bg="#EDF2ED", rule="#CFDFD3", margin="#D46A5E", ink="#1D2B3A", muted="#5E6C76", faint="#A8B6AE",
                  card="#F8FAF7", line="#D2DED5", stamp="#C2412D", shipped="#2E7D4F", early="#B7791F", design="#6B7A84",
                  grey="#9DAAB2", accent="#C2412D"),
    "dark": dict(bg="#18231F", rule="#24332D", margin="#7A3F3A", ink="#ECEFE6", muted="#9DAAA2", faint="#3C4E46",
                 card="#1D2A25", line="#2C3D36", stamp="#F2877A", shipped="#8FD3A6", early="#F3D27A", design="#9DAAA2",
                 grey="#56685F", accent="#F3D27A"),
}

# (date, repo, what it is, status): creation dates from GitHub; inp-fix is left out because its repo is still empty.
LOG = [
    ("10-24", "github-readme-designer", "READMEs that sell the project, with motion", "shipped"),
    ("10-23", "hackathon-skill", "teams of agents build rival takes; judges rank", "shipped"),
    ("10-23", "Glyphmotion", "interfaces drawn in living, full-color glyphs", "shipped"),
    ("10-21", "lighthouse-fix", "Lighthouse reports into ranked, agent-ready fixes", "shipped"),
    ("10-20", "auto-inspection-audit", "checks what an auto shop's inspection claims", "shipped"),
    ("10-17", "clay-motion", "a stop-motion studio run from Claude Code", "early"),
    ("10-17", "lego-motion", "brick-built films; design docs so far", "design"),
    ("10-11", "lasso", "explains hard things with a coach's warmth", "shipped"),
    ("10-11", "baseball-coach", "practice plans and drills for ages 4-12", "shipped"),
    ("09-26", "baseball-swing-analysis", "grades a swing from phone video", "shipped"),
    ("09-26", "exit-velo-eval", "exit velocity from phone video, or no guess", "shipped"),
    ("09-26", "sales-call-review", "calls into timelines and a coaching report", "shipped"),
    ("09-26", "youth-baseball-league-benchmarks", "fees and sponsors across 37 Little Leagues", "shipped"),
    ("09-25", "Recording-Atlas", "makes recorded knowledge searchable again", "shipped"),
]


def paper(w, h, t):
    """Scorebook ruling: horizontal rules every 28px and a red margin line."""
    rules = "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{t["rule"]}" stroke-width="1"/>' for y in range(28, h, 28))
    return (f'<rect width="{w}" height="{h}" rx="18" fill="{t["bg"]}"/>\n<g>{rules}</g>\n'
            f'<line x1="40" y1="0" x2="40" y2="{h}" stroke="{t["margin"]}" stroke-width="1.2" opacity=".55"/>\n')


def ledger(x, y, w, h, t, cycle=30):
    css, out = [], []
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["card"]}" stroke="{t["line"]}"/>'
               f'<text class="mono" x="{x + 20}" y="{y + 32}" font-size="13" font-weight="700" letter-spacing="2" fill="{t["ink"]}">SHIPPING LOG</text>'
               f'<text class="mono" x="{x + w - 20}" y="{y + 32}" font-size="12" text-anchor="end" fill="{t["muted"]}">SEP 25 – OCT 24, 2026</text>'
               f'<line x1="{x}" y1="{y + 48}" x2="{x + w}" y2="{y + 48}" stroke="{t["line"]}"/>'
               f'<text class="mono" x="{x + 20}" y="{y + 68}" font-size="11" letter-spacing="1.5" fill="{t["muted"]}">DATE</text>'
               f'<text class="mono" x="{x + 92}" y="{y + 68}" font-size="11" letter-spacing="1.5" fill="{t["muted"]}">PROJECT</text>'
               f'<text class="mono" x="{x + w - 20}" y="{y + 68}" font-size="11" letter-spacing="1.5" text-anchor="end" fill="{t["muted"]}">STATUS</text>'
               f'<line x1="{x + 78}" y1="{y + 52}" x2="{x + 78}" y2="{y + h - 8}" stroke="{t["margin"]}" stroke-width="1.2" opacity=".7"/>')
    top, rh = y + 78, 48
    view = h - 86
    rows = []
    for i, (date, repo, what, status) in enumerate(LOG + LOG):
        ry = top + i * rh
        tag_w = sk.text_width(status.upper(), 11.5) + 6
        name = sk.fit(repo, 14, w - 92 - 20 - tag_w - 10)
        rows.append(f'<line x1="{x + 8}" y1="{ry + rh}" x2="{x + w - 8}" y2="{ry + rh}" stroke="{t["line"]}"/>'
                    f'<text class="mono" x="{x + 20}" y="{ry + 21}" font-size="12.5" fill="{t["muted"]}">{date}</text>'
                    f'<text class="mono" x="{x + 92}" y="{ry + 21}" font-size="14" font-weight="700" fill="{t["ink"]}">{sk.esc(name)}</text>'
                    f'<text class="mono" x="{x + 92}" y="{ry + 39}" font-size="12" fill="{t["muted"]}">{sk.esc(sk.fit(what, 12, w - 92 - 20))}</text>'
                    f'<text class="mono" x="{x + w - 20}" y="{ry + 21}" font-size="11.5" font-weight="700" letter-spacing="1" text-anchor="end" fill="{t[status]}">{status.upper()}</text>')
    css.append(f"""
.log {{ animation: log {cycle}s linear infinite; }}
@keyframes log {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-{len(LOG) * rh}px); }} }}""")
    out.append(f'<defs><clipPath id="logclip"><rect x="{x}" y="{top}" width="{w}" height="{view}"/></clipPath>'
               f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["card"]}" stop-opacity="0"/>'
               f'<stop offset="1" stop-color="{t["card"]}"/></linearGradient>'
               f'<linearGradient id="fadetop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["card"]}"/>'
               f'<stop offset="1" stop-color="{t["card"]}" stop-opacity="0"/></linearGradient></defs>'
               f'<g clip-path="url(#logclip)"><g class="log">{"".join(rows)}</g></g>'
               f'<rect x="{x + 1}" y="{y + h - 60}" width="{w - 2}" height="59" rx="9" fill="url(#fade)"/>'
               f'<rect x="{x + 1}" y="{top}" width="{w - 2}" height="22" fill="url(#fadetop)"/>')
    return "".join(css), "\n".join(out)


def stamp(cx, cy, t, r=58, cycle=10):
    css = f"""
.stamp {{ transform-box: fill-box; transform-origin: center; transform: rotate(-12deg); animation: stamp {cycle}s cubic-bezier(.3,1.6,.5,1) infinite both; }}
@keyframes stamp {{ 0%,4% {{ transform: rotate(-12deg) scale(1.7); opacity: 0; }} 9%,92% {{ transform: rotate(-12deg) scale(1); opacity: .92; }} 100% {{ transform: rotate(-12deg) scale(1); opacity: 0; }} }}"""
    s = t["stamp"]
    svg = (f'<g class="stamp" opacity=".92">'
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["bg"]}" fill-opacity=".85" stroke="{s}" stroke-width="3"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{r - 7}" fill="none" stroke="{s}" stroke-width="1.2"/>'
           f'<text class="mono" x="{cx}" y="{cy - 14}" font-size="11" font-weight="700" letter-spacing="2" text-anchor="middle" fill="{s}">SHIPPED</text>'
           f'<text class="serif" x="{cx}" y="{cy + 16}" font-size="32" font-weight="700" text-anchor="middle" fill="{s}">14</text>'
           f'<text class="mono" x="{cx}" y="{cy + 34}" font-size="10.5" font-weight="700" letter-spacing="1.5" text-anchor="middle" fill="{s}">IN 30 DAYS</text></g>')
    return css, svg


def hero(t, size):
    wide = size == "wide"
    W, H = (1280, 480) if wide else (640, 900)
    tx = 72 if wide else 64
    if wide:
        ey, ny, ty, by, cy = 104, 172, 222, 300, 352
        lcss, log = ledger(690, 60, 526, 380, t)
        scss, stp = stamp(606, 318, t)
    else:
        ey, ny, ty, by, cy = 62, 128, 178, 254, 300
        lcss, log = ledger(56, 372, 544, 480, t)
        scss, stp = stamp(552, 372, t, r=50)
    name_size, tag_size = (60, 29) if wide else (52, 26)
    chips, cx, chip_svg = ["Claude Code", "SwingDino · beta", "Little League coach"], tx, []
    for c in chips:
        cw = sk.text_width(c, 13) + 26
        chip_svg.append(f'<rect x="{cx}" y="{cy}" width="{cw:.0f}" height="30" rx="15" fill="none" stroke="{t["faint"]}"/>'
                        f'<text class="mono" x="{cx + cw / 2:.0f}" y="{cy + 20}" font-size="13" text-anchor="middle" fill="{t["ink"]}">{sk.esc(c)}</text>')
        cx += cw + 10
    body = f"""{paper(W, H, t)}
<text class="mono" x="{tx}" y="{ey}" font-size="13" letter-spacing="2.5" fill="{t['muted']}">BUILDER · PRODUCT MARKETER · COACH</text>
<text class="serif" x="{tx - 3}" y="{ny}" font-size="{name_size}" fill="{t['ink']}">Chris Rader</text>
<text class="serif" x="{tx - 1}" y="{ty}" font-size="{tag_size}" font-style="italic" fill="{t['ink']}">I decide what's worth building,</text>
<text class="serif" x="{tx - 1}" y="{ty + tag_size + 8}" font-size="{tag_size}" font-style="italic" fill="{t['ink']}">set the rules, and check the work.</text>
<text class="mono" x="{tx}" y="{by}" font-size="14" fill="{t['muted']}">VP of Product Marketing at Centercode by day.</text>
<text class="mono" x="{tx}" y="{by + 22}" font-size="14" fill="{t['muted']}">Agent skills, apps and coaching tools on my own time.</text>
{"".join(chip_svg)}
{log}
{stp}"""
    return sk.svg_doc(W, H, "Chris Rader",
                      "Chris Rader: builder, product marketer, coach. A scorebook-style shipping log scrolls through 14 projects "
                      "shipped between September 25 and October 24, 2026, from Recording-Atlas to github-readme-designer, "
                      "and a stamp reads: shipped, 14 in 30 days.",
                      lcss + scss, body)


# ---------- receipts ----------

RECEIPTS = [  # label, what was measured, without, with
    ("lighthouse-fix · Haiku", "report analysis, graded blind", 74, 85),
    ("lighthouse-fix · Sonnet", "report analysis, graded blind", 85, 97),
    ("lighthouse-fix · Opus", "report analysis, graded blind", 83, 100),
    ("github-readme-designer", "checks passed across 3 repos", 81, 97),
]


def receipts(t, size):
    wide = size == "wide"
    CYCLE = 10
    W, H = (1280, 470) if wide else (640, 700)
    mx = 72 if wide else 64
    css = [sk.loop_fade("bars", CYCLE)]
    body = [paper(W, H, t),
            f'<text class="mono" x="{mx}" y="70" font-size="13" letter-spacing="2" fill="{t["muted"]}">{"RECEIPTS · SAME MODEL, SAME TASK, WITH AND WITHOUT MY SKILLS" if wide else "RECEIPTS · WITH VS WITHOUT MY SKILLS"}</text>',
            f'<text class="serif" x="{mx - 2}" y="116" font-size="{32 if wide else 28}" fill="{t["ink"]}">I publish what I tested, and how it scored.</text>']
    if wide:
        x0, x1, row0, step = mx + 330, W - 140, 186, 56
    else:
        x0, x1, row0, step = mx + 40, W - 90, 196, 112
    sx = lambda v: x0 + (v - 60) / 40 * (x1 - x0)
    axis_bottom = row0 + step * (len(RECEIPTS) - 1) + (26 if wide else 30)
    for v in (60, 80, 100):
        body.append(f'<line x1="{sx(v):.0f}" y1="{row0 - 28}" x2="{sx(v):.0f}" y2="{axis_bottom}" stroke="{t["faint"]}" stroke-dasharray="2 5"/>'
                    f'<text class="mono" x="{sx(v):.0f}" y="{axis_bottom + 20}" font-size="12" text-anchor="middle" fill="{t["muted"]}">{v}%</text>')
    for i, (label, what, a, b) in enumerate(RECEIPTS):
        y = row0 + i * step
        ly, wy = (y + 1, y + 19) if wide else (y - 44, y - 24)
        xa, xb = sx(a), sx(b)
        s, e = 4 + i * 6, 20 + i * 6
        css.append(sk.draw(f"l{i}", CYCLE, xb - xa, s, e, off=100))
        css.append(sk.slide(f"d{i}", CYCLE, xb - xa, s, e))
        ccss, ctext = sk.count_up(f"c{i}_", CYCLE, sk.steps(a, b, 5), s, e, xb + 16, y + 5,
                                  f'class="mono" font-size="14" font-weight="700" fill="{t["ink"]}"', unit="%")
        css.append(ccss)
        body.append(f'<text class="mono" x="{mx}" y="{ly}" font-size="14" font-weight="700" fill="{t["ink"]}">{sk.esc(label)}</text>'
                    f'<text class="mono" x="{mx}" y="{wy}" font-size="12" fill="{t["muted"]}">{sk.esc(what)}</text>'
                    f'<circle cx="{xa:.1f}" cy="{y}" r="8" fill="{t["bg"]}" stroke="{t["grey"]}" stroke-width="3"/>'
                    f'<text class="mono" x="{xa - 14:.1f}" y="{y + 5}" font-size="13" text-anchor="end" fill="{t["muted"]}">{a}%</text>'
                    f'<g class="bars"><line class="l{i}" x1="{xa:.1f}" y1="{y}" x2="{xb:.1f}" y2="{y}" stroke="{t["accent"]}" stroke-width="4" stroke-linecap="round"/>'
                    f'<g class="d{i}"><circle cx="{xb:.1f}" cy="{y}" r="9" fill="{t["accent"]}"/>{ctext}</g></g>')
    ly = H - 34
    body.append(f'<g class="mono" font-size="13" fill="{t["muted"]}">'
                f'<circle cx="{mx + 8}" cy="{ly - 4}" r="7" fill="{t["bg"]}" stroke="{t["grey"]}" stroke-width="3"/><text x="{mx + 24}" y="{ly + 1}">without the skill</text>'
                f'<circle cx="{mx + 188}" cy="{ly - 4}" r="8" fill="{t["accent"]}"/><text x="{mx + 204}" y="{ly + 1}">with the skill</text>'
                + (f'<text x="{W - 72}" y="{ly + 1}" text-anchor="end">One run per setup. Methods and raw results are in each repo.</text>' if wide else
                   f'<text x="{mx}" y="{ly - 30}">One run per setup. Raw results are in each repo.</text>')
                + '</g>')
    return sk.svg_doc(W, H, "Receipts: results with and without my skills",
                      "lighthouse-fix report analysis, graded blind: Haiku 74 to 85 percent, Sonnet 85 to 97, Opus 83 to 100. "
                      "github-readme-designer checks passed across three repos: 81 to 97 percent.",
                      "".join(css), "".join(body))


if __name__ == "__main__":
    sk.write_all(OUT, {"hero": hero, "receipts": receipts}, THEMES)
