"""
LeadLens ranking engine (v1: rule-based).

Priority score = weighted blend of:
  - deal value        (bigger deals ranked higher)
  - recency of contact (recently contacted leads ranked higher, stale ones lower)
  - engagement score   (higher engagement ranked higher)

This is intentionally simple and explainable -- a defensible v1 baseline.
A learned model (e.g. gradient boosting on historical won/lost outcomes)
is the natural next step once real conversion-outcome data exists.
"""

import pandas as pd

# Weights: must sum to 1.0
WEIGHT_DEAL_VALUE = 0.40
WEIGHT_RECENCY = 0.35
WEIGHT_ENGAGEMENT = 0.25


def _normalize(series: pd.Series) -> pd.Series:
    """Min-max normalize a numeric column to the 0-100 range."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return series * 0 + 50.0
    return (series - lo) / (hi - lo) * 100.0


def score_leads(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with recency_score, deal_value_score, and
    priority_score columns added, sorted by priority_score descending."""
    df = df.copy()

    # Recency: fewer days since last contact = higher score.
    # Invert days-ago so "0 days ago" scores highest.
    max_days = df["last_contact_days_ago"].max()
    df["recency_score"] = _normalize(max_days - df["last_contact_days_ago"])

    df["deal_value_score"] = _normalize(df["deal_value"])
    df["engagement_score_norm"] = _normalize(df["engagement_score"])

    df["priority_score"] = (
        WEIGHT_DEAL_VALUE * df["deal_value_score"]
        + WEIGHT_RECENCY * df["recency_score"]
        + WEIGHT_ENGAGEMENT * df["engagement_score_norm"]
    ).round(1)

    return df.sort_values("priority_score", ascending=False).reset_index(drop=True)


def top_factors(row: pd.Series) -> list[str]:
    """Return the (up to 2) factors that most drove this lead's ranking,
    used to seed the explanation step."""
    factors = {
        "deal size": row["deal_value_score"],
        "recent activity": row["recency_score"],
        "engagement": row["engagement_score_norm"],
    }
    ranked = sorted(factors.items(), key=lambda kv: kv[1], reverse=True)
    return [name for name, _ in ranked[:2]]