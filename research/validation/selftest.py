"""Self-test for the validation kit. It never touches your real files.
It fakes a 'human' coding by copying the AI codes and changing about 15% of them at random, then runs compare.py
and write_method_note.py on copies inside research/validation/test_run/.
Run from the project root:  .venv/bin/python research/validation/selftest.py
"""
import csv, json, pathlib, random, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
T = ROOT / "research/validation/test_run"
shutil.rmtree(T, ignore_errors=True); T.mkdir()
key = list(csv.DictReader(open(ROOT / "research/validation/answer_key.csv")))
random.seed(7)
with open(T / "fake_human.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["sample_id", "issue", "denial_reason", "support_or_refund_complaint"])
    for r in key:
        issue, reason, comp = r["issue"], r["denial_reason"], r["support_or_refund_complaint"]
        if random.random() < .15: issue = random.choice("DCELQROX")
        if issue == "D" and (not reason or random.random() < .15): reason = random.choice(["full", "norec", "price", "gone", "unst"])
        if issue != "D": reason = ""
        if random.random() < .1: comp = "no" if comp == "yes" else "yes"
        w.writerow([r["sample_id"], issue, reason, comp])
py = sys.executable
subprocess.run([py, str(ROOT / "research/validation/compare.py"), str(T / "fake_human.csv"), "--out", str(T / "results.json")], check=True, cwd=ROOT)
for name, src in [("page.html", "case-study/index.html"), ("analysis.md", "research/review_analysis.md")]:
    shutil.copy(ROOT / src, T / name)
subprocess.run([py, str(ROOT / "research/validation/write_method_note.py"), "--results", str(T / "results.json"),
                "--page", str(T / "page.html"), "--analysis", str(T / "analysis.md"), "--no-render"], check=True, cwd=ROOT)
r = json.load(open(T / "results.json"))
assert r["n"] == 100 and 0 <= r["fields"]["issue"]["kappa"] <= 1
assert "coded a random sample of 100" in (T / "page.html").read_text()
print("\nSELF-TEST PASSED: the kit ran end to end on a fake input. Your real files were not changed.")
