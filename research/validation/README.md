# Validation kit: check the AI's coding yourself

The reviews in this project were coded by an AI model against `research/codebook.md`. This kit lets a person check that coding on a random sample of 100 reviews and puts the result on the case study page.

1. Open `validation_sample.xlsx`. Read the "How to code" tab, then fill in the three columns on "Code these" for all 100 reviews using the codebook. Do not open `answer_key.csv` or `research/guest_reviews.csv` until you finish. About 60 to 90 minutes.
2. Compare your codes with the AI's (agreement and Cohen's kappa for each tag):
   `.venv/bin/python research/validation/compare.py research/validation/validation_sample.xlsx`
3. Write the result into the method note on the case study page and in `review_analysis.md`, and re-render the documents:
   `.venv/bin/python research/validation/write_method_note.py`
4. Rebuild the one-page PDF so it carries the same method note:
   `.venv/bin/python case-study/build_one_pager.py`

To check the kit works without touching anything real: `.venv/bin/python research/validation/selftest.py`

Until step 3 is done, the page says that human validation is pending, which is true.
