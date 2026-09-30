# LeadLens

**AI Decision Engine for Business Data** — PS-04, AI Build Challenge 2026 (Build Fast with AI)

LeadLens reads a sales team's CRM data and ranks every open lead by how likely it
is to convert — with a plain-English reason behind every score, traced back to the
exact data behind it. Instead of manually scanning through hundreds of leads, a rep
gets a ranked shortlist, can ask "why this lead?", and approves outreach with one
click.

## Why we built it

Sales reps lose 30–45 minutes a day manually re-triaging CRM leads, and a
meaningful share of high-intent leads go cold before anyone reaches out — not
because the data isn't there, but because no one has time to read all of it.
LeadLens turns that manual triage into a ranked, explainable shortlist.

## How it works

1. **Rank (v1: rule-based)** — every lead is scored on a weighted blend of deal
   value, recency of last contact, and engagement score. See `ranking.py`.
2. **Explain (RAG-lite)** — for any lead a rep opens, LeadLens retrieves the
   structured + unstructured facts behind its score (deal size, recency,
   engagement, CRM notes) and generates a one-line, plain-English explanation.
   See `explain.py`.
3. **Approve** — the system only ranks and explains. A human always approves
   the outreach action; LeadLens never contacts a lead on its own.

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app runs end-to-end out of the box using a deterministic fallback
explanation — no API key required. To get LLM-generated explanations instead,
set an API key before running:

```bash
export OPENAI_API_KEY=your_key_here
streamlit run app.py
```

## Project structure

```
leadlens/
├── app.py              # Streamlit dashboard
├── ranking.py           # Rule-based priority scoring
├── explain.py            # RAG-lite explanation generation (LLM + offline fallback)
├── generate_data.py        # Synthetic CRM dataset generator
├── data/leads.csv            # Sample CRM data (70 leads)
└── requirements.txt
```

## Evaluation

- **Baseline (today):** ~30–45 min/day per rep manually triaging leads in the CRM.
- **Target (with LeadLens):** under 5 min/day to review an AI-ranked shortlist
  and approve outreach — same task, from raw data to decision.
- Ranking quality was sanity-checked by hand against the sample dataset: leads
  with larger deal value, recent contact, and high engagement consistently
  surface at the top, and the generated explanations correctly cite the actual
  fields driving each score.

## What's next (out of scope for this submission)

- Replace the rule-based scorer with a model trained on real won/lost outcomes.
- Natural-language querying over the full lead base ("show me leads that went
  cold in the last two weeks").
- Duplicate/stale-record detection before leads enter the ranking pipeline.

## Team

Built by [Your Name] and Thirumalaivasan N for AI Build Challenge 2026.