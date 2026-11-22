"""Writes the method note on the case study page (and in review_analysis.md) from the validation result.
If research/validation/results.json does not exist yet, it writes the 'validation pending' version, so the page is true either way.
Usage (from the project root):
  .venv/bin/python research/validation/write_method_note.py
Optional: --results PATH --page PATH --analysis PATH (used by the self-test so it never touches the real files).
"""
import argparse, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CFG = json.load(open(ROOT / "project_config.json"))

def note(results):
    if results is None:
        return ("<p><strong>How the reviews were coded.</strong> The reviews were coded by an AI model (Claude, made by Anthropic) "
                "against a written codebook, not by hand. Human validation of a random sample of 100 coded reviews is pending. "
                "Until it is done, treat every count from the reviews as AI-coded and not yet checked by a person.</p>")
    f = results["fields"]
    i, c, d = f["issue"], f["support_or_refund_complaint"], f["denial_reason"]
    weak = [n for n, v in f.items() if v["kappa"] is not None and v["kappa"] < 0.6]
    caution = (f" Agreement was below 0.6 kappa for {', '.join(n.replace('_', ' ') for n in weak)}, so read those counts with extra caution."
               if weak else "")
    return ("<p><strong>How the reviews were coded.</strong> The reviews were coded by an AI model (Claude, made by Anthropic) "
            f"against a written codebook, not by hand. {CFG['author']} then coded a random sample of {results['n']} of the same reviews "
            "without seeing the AI's codes, and the two were compared. "
            f"Agreement on the main issue was {i['agreement_pct']}% (Cohen's kappa {i['kappa']}, {i['band']}); "
            f"on whether a review complained about support or refunds, {c['agreement_pct']}% (kappa {c['kappa']}, {c['band']}); "
            f"and on the reason the hotel gave, among the {d['n']} reviews both coders marked as denials, {d['agreement_pct']}% "
            f"(kappa {d['kappa']}, {d['band']}).{caution}</p>")

def replace_between(text, html):
    pat = re.compile(r"(<!-- METHOD-NOTE:START -->)(.*?)(<!-- METHOD-NOTE:END -->)", re.S)
    if not pat.search(text):
        sys.exit("Method-note markers not found.")
    return pat.sub(lambda m: m.group(1) + "\n" + html + "\n" + m.group(3), text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=str(ROOT / "research/validation/results.json"))
    ap.add_argument("--page", default=str(ROOT / "case-study/index.html"))
    ap.add_argument("--analysis", default=str(ROOT / "research/review_analysis.md"))
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()
    rp = pathlib.Path(a.results)
    results = json.load(open(rp)) if rp.exists() else None
    html = note(results)
    for target in (a.page, a.analysis):
        p = pathlib.Path(target)
        p.write_text(replace_between(p.read_text(), html))
        print("updated", p)
    if not a.no_render and (ROOT / "build_docs.py").exists():
        subprocess.run([sys.executable, str(ROOT / "build_docs.py")], cwd=ROOT, check=True)
    print("Method note now says:", re.sub("<[^>]+>", "", html))

if __name__ == "__main__":
    main()
