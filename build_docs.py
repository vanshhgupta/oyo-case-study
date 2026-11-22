"""Renders the project's Markdown documents to HTML pages so every link works on GitHub Pages.
Run from the project root after editing any .md file:  .venv/bin/python build_docs.py
Links between documents that end in .md are rewritten to .html in the rendered pages.
"""
import html, pathlib, re
import markdown

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ["research/review_analysis.md", "research/feature_audit.md", "research/sources.md", "research/codebook.md",
        "strategy/problem.md", "strategy/solutions.md", "strategy/metrics.md", "prd/PRD.md"]

TPL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root{{--ink:#1d1b26;--muted:#5d5a6b;--line:#e4e1ea;--bg:#f7f6f2;--card:#ffffff;--accent:#4338ca;--warm:#b45309;--code:#efedf5}}
@media (prefers-color-scheme: dark){{:root{{--ink:#ecebf2;--muted:#aaa7b8;--line:#2e2c3a;--bg:#14131b;--card:#1c1b25;--accent:#a5b4fc;--warm:#f5b25b;--code:#24232f}}}}
*{{box-sizing:border-box}} html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16.5px/1.65 "Avenir Next","Segoe UI",system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif}}
main{{max-width:860px;margin:0 auto;padding:22px 16px 72px}}
a{{color:var(--accent)}} h1{{font-size:clamp(26px,5vw,36px);line-height:1.15;letter-spacing:-.01em;margin:10px 0 18px}}
h2{{font-size:22px;margin-top:38px;padding-top:14px;border-top:1px solid var(--line)}} h3{{font-size:18px;margin-top:26px}}
.tablewrap{{overflow-x:auto;margin:12px 0}} table{{border-collapse:collapse;width:100%;font-size:14.5px}}
th,td{{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}} th{{color:var(--muted);font-weight:600}}
blockquote{{margin:14px 0;padding:8px 16px;border-left:3px solid var(--warm);background:var(--card);border-radius:0 8px 8px 0}}
code{{background:var(--code);border-radius:4px;padding:0 4px;font-size:90%}} pre{{background:var(--code);padding:12px;overflow-x:auto;border-radius:8px}}
.back{{font-size:14px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:var(--muted)}}
</style></head>
<body><main>
<p class="back"><a href="{home}">← Back to the case study</a><span>Independent student case study · not affiliated with OYO</span></p>
{body}
</main></body></html>"""

def render(rel):
    p = ROOT / rel
    text = p.read_text()
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    body = re.sub(r'href="([^"#:]+)\.md(#[^"]*)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', body)
    body = body.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")
    home = "../case-study/index.html"
    out = p.with_suffix(".html")
    out.write_text(TPL.format(title=html.escape(title), body=body, home=home))
    return out

if __name__ == "__main__":
    for d in DOCS:
        if (ROOT / d).exists():
            print("wrote", render(d).relative_to(ROOT))
