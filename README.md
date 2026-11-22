# OYO Check-in Denial — Product Case Study

**[View Live Case Study](https://vanshhgupta.github.io/oyo-case-study/)**

---

An independent student product case study, not affiliated with OYO. Start with `index.html` (it opens `case-study/index.html`).

| Folder | What is in it |
|---|---|
| `case-study/` | The case study page, the one-page PDF and the prototype screenshots |
| `research/` | Review data and analysis, codebook, feature audit, sources, validation kit |
| `strategy/` | Problem, solutions, metrics, and the impact model (`impact_model.xlsx`, live formulas) |
| `prd/` | Product requirements |
| `prototype/` | Clickable prototype, one self-contained file |

The reviews were coded by an AI model against a written codebook; see `research/validation/README.md` to check that coding.

**Rebuild everything** (Python 3.12):

```
python3.12 -m venv .venv && .venv/bin/pip install google-play-scraper openpyxl pypdf markdown reportlab pycel
.venv/bin/python research/analyse_guest.py && .venv/bin/python research/analyse_owner.py
.venv/bin/python strategy/build_model.py
.venv/bin/python build_docs.py
.venv/bin/python check_quotes.py
.venv/bin/python case-study/build_one_pager.py
```

The one-page PDF uses the Georgia font from macOS for the rupee sign.
