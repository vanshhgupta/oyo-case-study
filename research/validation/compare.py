"""Compares your codes with the AI's codes for the 100-review validation sample.
Usage (from the project root):
  .venv/bin/python research/validation/compare.py research/validation/validation_sample.xlsx
Accepts the filled .xlsx, or a .csv with the same columns. Writes research/validation/results.json and prints a report.
Optional: --key PATH (answer key, default research/validation/answer_key.csv), --out PATH (results file).
"""
import argparse, csv, json, collections, pathlib, sys

def cohen_kappa(a, b):
    """Cohen's kappa for two equal-length lists of labels. Returns None when it is undefined (one label only)."""
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    if pe == 1:
        return None
    return (po - pe) / (1 - pe)

def band(k):
    if k is None: return "undefined (only one label present)"
    return ("poor" if k < 0 else "slight" if k < .2 else "fair" if k < .4 else "moderate" if k < .6
            else "substantial" if k < .8 else "almost perfect")

def read_human(path):
    p = pathlib.Path(path)
    if p.suffix == ".xlsx":
        from openpyxl import load_workbook
        ws = load_workbook(p, data_only=True)["Code these"]
        rows = list(ws.iter_rows(values_only=True))
        head = [str(h) for h in rows[0]]
        data = [dict(zip(head, r)) for r in rows[1:] if r and r[0]]
    else:
        data = list(csv.DictReader(open(p)))
    out = {}
    for r in data:
        g = lambda k: (str(r.get(k) or "").strip())
        out[g("sample_id")] = {"issue": g("issue").upper(), "denial_reason": g("denial_reason").lower(),
                               "support_or_refund_complaint": g("support_or_refund_complaint").lower()}
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("human")
    ap.add_argument("--key", default="research/validation/answer_key.csv")
    ap.add_argument("--out", default="research/validation/results.json")
    a = ap.parse_args()
    human = read_human(a.human)
    key = {r["sample_id"]: r for r in csv.DictReader(open(a.key))}
    missing = [s for s in key if not human.get(s, {}).get("issue")]
    if missing:
        sys.exit(f"{len(missing)} reviews have no issue code yet (first few: {missing[:5]}). Finish coding, then run again.")
    ids = sorted(key)
    res = {"n": len(ids), "fields": {}, "per_issue": {}}

    def add(name, A, B, note=""):
        agree = sum(x == y for x, y in zip(A, B))
        k = cohen_kappa(A, B)
        res["fields"][name] = {"n": len(A), "agreement_pct": round(100 * agree / len(A), 1) if A else None,
                               "kappa": None if k is None else round(k, 2), "band": band(k), "note": note}

    hi = [human[s]["issue"] for s in ids]; ai = [key[s]["issue"] for s in ids]
    add("issue", hi, ai, "the main issue, 8 categories")
    for code in "DCELQROX":
        A = [x == code for x in hi]; B = [x == code for x in ai]
        k = cohen_kappa(A, B)
        res["per_issue"][code] = {"human_n": sum(A), "ai_n": sum(B), "agreement_pct": round(100 * sum(x == y for x, y in zip(A, B)) / len(A), 1),
                                  "kappa": None if k is None else round(k, 2), "band": band(k)}
    both_d = [s for s in ids if human[s]["issue"] == "D" and key[s]["issue"] == "D"]
    add("denial_reason", [human[s]["denial_reason"] or "unst" for s in both_d], [key[s]["denial_reason"] for s in both_d],
        "only reviews that both coders marked as denials")
    add("support_or_refund_complaint", [human[s]["support_or_refund_complaint"] for s in ids],
        [key[s]["support_or_refund_complaint"] for s in ids], "yes or no")
    conf = collections.Counter((h, x) for h, x in zip(hi, ai) if h != x)
    res["disagreements_issue"] = {f"you {h} / AI {x}": n for (h, x), n in conf.most_common()}
    json.dump(res, open(a.out, "w"), indent=1)

    print(f"Validation of AI coding on {res['n']} randomly sampled reviews\n")
    for f, v in res["fields"].items():
        print(f"  {f:30s} agreement {v['agreement_pct']}%   kappa {v['kappa']}   ({v['band']}; n={v['n']}; {v['note']})")
    print("\n  One-vs-rest, by issue code:")
    for c, v in res["per_issue"].items():
        print(f"    {c}: you {v['human_n']:3d}  AI {v['ai_n']:3d}  agreement {v['agreement_pct']}%  kappa {v['kappa']} ({v['band']})")
    print("\n  Most common disagreements on issue:", res["disagreements_issue"] or "none")
    print(f"\nWrote {a.out}. Next: .venv/bin/python research/validation/write_method_note.py")

if __name__ == "__main__":
    main()
