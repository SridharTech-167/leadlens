"""
Generates a synthetic CRM leads dataset for LeadLens.
Run once: python generate_data.py
Produces data/leads.csv
"""

import csv
import random

random.seed(42)

FIRST_NAMES = ["Ananya", "Rohan", "Priya", "Karthik", "Sneha", "Arjun", "Divya",
               "Vikram", "Meera", "Aditya", "Kavya", "Sanjay", "Neha", "Rahul",
               "Pooja", "Suresh", "Anjali", "Manoj", "Deepa", "Kiran"]

LAST_NAMES = ["Sharma", "Reddy", "Iyer", "Nair", "Gupta", "Menon", "Rao",
              "Verma", "Pillai", "Krishnan", "Joshi", "Kumar", "Mehta", "Das"]

COMPANIES = ["Verdant Labs", "Blue Ridge Tech", "Orbit Systems", "Nimbus Cloud",
             "Terra Analytics", "Skyline Retail", "Coral Fintech", "Pinewood Foods",
             "Quantum Robotics", "Amber Logistics", "Solstice Media", "Harbor Health",
             "Granite Manufacturing", "Willow Education", "Delta Energy",
             "Lumen Marketing", "Cedar Consulting", "Ironclad Security",
             "Meridian Travel", "Frostline Apparel"]

SOURCES = ["Website Demo Request", "LinkedIn Outreach", "Referral", "Webinar Signup",
           "Trade Show", "Cold Email Reply", "Paid Ad Click", "Partner Referral"]

STATUSES = ["New", "Contacted", "Qualified", "Proposal Sent", "Negotiation"]

NOTE_TEMPLATES = [
    "Requested a demo after downloading our pricing guide. Asked specifically about API integration limits.",
    "Replied to outreach email within an hour, said budget is approved for this quarter.",
    "Attended our webinar and stayed for the full Q&A, asked about enterprise plan.",
    "Referred by an existing customer, mentioned they need a decision before next board meeting.",
    "Filled out contact form but hasn't responded to two follow-up emails yet.",
    "Met at trade show booth, exchanged cards, said team is evaluating three vendors.",
    "Clicked pricing page three times this week according to site analytics.",
    "Asked for a custom quote for 200+ seats, said current contract with competitor ends next month.",
    "Opened last two emails but no reply yet, engagement dropping over past 10 days.",
    "Requested case studies from similar industry, said they're comparing us to one competitor.",
    "Initial contact only, no further engagement recorded since form submission.",
    "Had a discovery call, raised concerns about implementation timeline.",
    "Fast-growing startup, mentioned urgency due to upcoming funding round deadline.",
    "Long-time newsletter subscriber, first time showing direct purchase intent.",
    "Asked detailed technical questions about data security and compliance.",
]

def make_lead(lead_id: int) -> dict:
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    company = random.choice(COMPANIES)
    source = random.choice(SOURCES)
    status = random.choice(STATUSES)
    deal_value = random.choice([15000, 25000, 40000, 60000, 80000, 120000, 200000])
    last_contact_days_ago = random.randint(0, 30)
    engagement_score = random.randint(10, 95)
    notes = random.choice(NOTE_TEMPLATES)
    return {
        "lead_id": f"L{lead_id:03d}",
        "name": name,
        "company": company,
        "source": source,
        "status": status,
        "deal_value": deal_value,
        "last_contact_days_ago": last_contact_days_ago,
        "engagement_score": engagement_score,
        "notes": notes,
    }

def main():
    leads = [make_lead(i) for i in range(1, 71)]  # 70 leads
    fieldnames = list(leads[0].keys())
    with open("data/leads.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
    print(f"Wrote {len(leads)} leads to data/leads.csv")

if __name__ == "__main__":
    main()