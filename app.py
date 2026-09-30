"""
LeadLens -- AI Decision Engine for Business Data (PS-04)
AI Build Challenge 2026, Build Fast with AI

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

import pandas as pd
import streamlit as st

from ranking import score_leads
from explain import explain_lead

st.set_page_config(page_title="LeadLens", page_icon="🔍", layout="wide")

# ---------- Session state ----------
if "approved" not in st.session_state:
    st.session_state.approved = []  # list of lead_ids approved for outreach

if "explanations" not in st.session_state:
    st.session_state.explanations = {}  # lead_id -> explanation text (cache)


# ---------- Data loading ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/leads.csv")
    return score_leads(df)


df = load_data()

# ---------- Header ----------
st.title("🔍 LeadLens")
st.caption("An AI decision engine that ranks and explains CRM leads, so sales teams know who to contact next.")

with st.expander("ℹ️ How this works", expanded=False):
    st.markdown(
        """
        1. **Rank** — every open lead is scored on deal value, recent activity, and engagement (rule-based v1).
        2. **Explain** — for any lead you open, LeadLens retrieves the facts behind its score and generates
           a plain-English reason (RAG-style: retrieve the data, then generate the explanation).
        3. **Approve** — a rep reviews the shortlist and approves outreach with one click.
           LeadLens never contacts a lead on its own — a human always approves the action.
        """
    )

st.divider()

# ---------- Layout: ranked table + detail panel ----------
left, right = st.columns([3, 2])

with left:
    st.subheader("Ranked shortlist")
    top_n = st.slider("Show top N leads", min_value=5, max_value=len(df), value=15, step=5)

    display_df = df.head(top_n)[
        ["lead_id", "name", "company", "status", "priority_score", "deal_value", "last_contact_days_ago"]
    ].rename(columns={
        "lead_id": "ID",
        "name": "Name",
        "company": "Company",
        "status": "Status",
        "priority_score": "Priority",
        "deal_value": "Deal Value (₹)",
        "last_contact_days_ago": "Days Since Contact",
    })

    st.dataframe(display_df, use_container_width=True, hide_index=True)

with right:
    st.subheader("Why this lead?")
    selected_id = st.selectbox("Pick a lead to inspect", df.head(top_n)["lead_id"].tolist())
    row = df[df["lead_id"] == selected_id].iloc[0]

    st.markdown(f"**{row['name']}** · {row['company']}")
    st.markdown(f"Priority score: **{row['priority_score']}** / 100")
    st.markdown(
        f"- Deal value: ₹{row['deal_value']:,}\n"
        f"- Last contacted: {row['last_contact_days_ago']} day(s) ago\n"
        f"- Engagement: {row['engagement_score']}/100\n"
        f"- Status: {row['status']}"
    )

    if st.button("Generate explanation", key=f"explain_{selected_id}"):
        with st.spinner("Retrieving lead context and generating explanation..."):
            explanation = explain_lead(row)
            st.session_state.explanations[selected_id] = explanation

    if selected_id in st.session_state.explanations:
        st.info(st.session_state.explanations[selected_id])

    already_approved = selected_id in st.session_state.approved
    if already_approved:
        st.success("✅ Approved for outreach")
    else:
        if st.button("✅ Approve to Outreach", key=f"approve_{selected_id}"):
            st.session_state.approved.append(selected_id)
            st.rerun()

st.divider()

# ---------- Approved outreach log ----------
st.subheader("Approved outreach log")
if st.session_state.approved:
    approved_df = df[df["lead_id"].isin(st.session_state.approved)][
        ["lead_id", "name", "company", "priority_score"]
    ].rename(columns={
        "lead_id": "ID", "name": "Name", "company": "Company", "priority_score": "Priority",
    })
    st.dataframe(approved_df, use_container_width=True, hide_index=True)
else:
    st.caption("No leads approved yet. Approve a lead above to see it here.")