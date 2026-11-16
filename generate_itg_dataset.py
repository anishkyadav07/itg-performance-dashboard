"""
India Tech Group - Sample Dataset Generator
Tagline: Learn, Grow & Succeed | www.indiatechgroup.com

Generates 5 RAW (intentionally messy) CSV files for the
Website & Digital Marketing Data Analysis Dashboard project.
Period: 01-04-2026 to 30-09-2026 (6 months)

NOTE: This is SAMPLE (synthetic) data created for the project, not real ITG analytics.
Run:  python generate_itg_dataset.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
START, END = "2026-04-01", "2026-09-30"
DATES = pd.date_range(START, END, freq="D")

# Month multipliers (admission season peaks in Aug/Sep, Aug has big workshop push)
MONTH_MULT = {4: 0.80, 5: 0.90, 6: 1.00, 7: 1.10, 8: 1.35, 9: 1.20}

SOURCES = ["Google", "Direct", "Instagram", "LinkedIn", "Facebook", "YouTube", "Referral"]
PAGES = {  # page: base weight
    "Home": 30, "IT Services": 14, "Web Development": 12, "AI & ML Workshop": 10,
    "Python Course": 9, "Data Science Course": 8, "Digital Marketing Course": 6,
    "About Us": 5, "Contact Us": 4, "Careers": 2,
}
PROGRAMS = {  # program: (type, weight)
    "Python Programming": ("Course", 20),
    "Data Science & ML": ("Course", 14),
    "Full Stack Web Development": ("Course", 16),
    "Digital Marketing": ("Course", 9),
    "AI & ChatGPT Workshop": ("Workshop", 18),
    "Excel & Power BI Workshop": ("Workshop", 10),
    "Cyber Security Awareness Workshop": ("Workshop", 6),
    "Resume & Interview Workshop": ("Workshop", 7),
}
ENQ_TYPES = ["IT Services", "Web Development", "App Development", "Course Admission",
             "Workshop Registration", "Internship", "General Query"]


def pick(options, weights, size=None):
    w = np.array(weights, dtype=float)
    return rng.choice(options, size=size, p=w / w.sum())


# ---------------------------------------------------------------- 1. WEBSITE
def website_traffic():
    src_w = {"Google": 38, "Direct": 18, "Instagram": 14, "LinkedIn": 11,
             "Facebook": 8, "YouTube": 6, "Referral": 5}
    rows = []
    for d in DATES:
        wk = 0.85 if d.dayofweek >= 5 else 1.0
        for page, pw in PAGES.items():
            for s in pick(SOURCES, [src_w[x] for x in SOURCES], size=3):
                if s == "LinkedIn" and page == "IT Services":
                    boost = 1.8
                elif s == "Instagram" and page == "AI & ML Workshop":
                    boost = 1.8
                else:
                    boost = 1.0
                mult = MONTH_MULT[d.month]
                if d.month == 8 and "Workshop" in page:
                    mult *= 1.4
                users = max(1, int(rng.normal(3 * pw * src_w[s] / 35 * mult * wk * boost, 8)))
                sessions = int(users * rng.uniform(1.1, 1.6))
                rows.append([d, s, page, users, sessions,
                             round(rng.uniform(32, 72), 1),
                             round(rng.uniform(40, 240))])
    return pd.DataFrame(rows, columns=["date", "source", "page", "users", "sessions",
                                       "bounce_rate_pct", "avg_session_duration_sec"])


# ------------------------------------------------------------- 2. ENQUIRIES
def enquiries():
    src_w = {"Google": 30, "LinkedIn": 20, "Instagram": 18, "Direct": 12,
             "Facebook": 8, "Referral": 7, "YouTube": 5}
    rows, n = [], 1
    for d in DATES:
        for _ in range(rng.poisson(3.6 * MONTH_MULT[d.month])):
            s = pick(SOURCES, [src_w[x] for x in SOURCES])
            if s == "LinkedIn":
                tw = [28, 22, 10, 8, 4, 18, 10]
            elif s == "Instagram":
                tw = [6, 8, 4, 38, 30, 6, 8]
            elif s == "Google":
                tw = [18, 16, 8, 28, 12, 8, 10]
            else:
                tw = [14, 14, 8, 26, 14, 12, 12]
            t = pick(ENQ_TYPES, tw)
            conv = 0.35 if s == "Referral" else 0.22
            status = pick(["Converted", "In Progress", "Lost", "New"],
                          [conv, 0.25, 0.38 - conv + 0.22, 0.15])
            rows.append([f"ENQ{n:04d}", d, s, t, status])
            n += 1
    return pd.DataFrame(rows, columns=["enquiry_id", "date", "source", "enquiry_type", "status"])


# ----------------------------------------------------------- 3. REGISTRATIONS
def registrations():
    rows, n = [], 1
    names = list(PROGRAMS)
    for d in DATES:
        for _ in range(rng.poisson(4.8 * MONTH_MULT[d.month])):
            w = [PROGRAMS[p][1] * (1.8 if (d.month == 8 and PROGRAMS[p][0] == "Workshop") else 1)
                 for p in names]
            p = pick(names, w)
            typ = PROGRAMS[p][0]
            if typ == "Workshop":
                src = pick(SOURCES, [20, 8, 34, 14, 10, 8, 6])
                mode = pick(["Online", "Offline"], [62, 38])
            else:
                src = pick(SOURCES, [34, 14, 14, 16, 8, 6, 8])
                mode = pick(["Online", "Offline"], [42, 58])
            rows.append([f"REG{n:04d}", d, p, typ, mode, src])
            n += 1
    return pd.DataFrame(rows, columns=["registration_id", "date", "program", "program_type",
                                       "mode", "source"])


# ---------------------------------------------------------------- 4. SOCIAL
def social_media():
    platforms = {"Instagram": (1200, 4), "LinkedIn": (650, 3), "Facebook": (900, 3), "YouTube": (300, 1)}
    ptypes = {"Instagram": ["Reel", "Carousel", "Image", "Story"],
              "LinkedIn": ["Text Post", "Carousel", "Image", "Poll"],
              "Facebook": ["Image", "Video", "Text Post", "Reel"],
              "YouTube": ["Video", "Short"]}
    boost = {"Reel": 2.2, "Short": 1.8, "Carousel": 1.5, "Video": 1.4, "Poll": 1.2,
             "Image": 1.0, "Story": 0.8, "Text Post": 0.9}
    topics = ["AI Workshop", "Python Course", "Web Development", "Data Science",
              "IT Services", "Student Success", "Career Tips", "Digital Marketing"]
    rows, n = [], 1
    for plat, (f0, per_week) in platforms.items():
        followers = f0
        for d in DATES:
            followers += int(rng.integers(0, 6) * MONTH_MULT[d.month])
            if rng.random() < per_week / 7:
                t = rng.choice(ptypes[plat])
                topic = rng.choice(topics)
                tb = 1.4 if topic in ("AI Workshop", "Career Tips") else 1.0
                reach = int(abs(rng.normal(followers * 0.6 * boost[t] * tb, followers * 0.15)))
                reach = max(reach, 50)
                impressions = int(reach * rng.uniform(1.15, 1.7))
                likes = int(reach * rng.uniform(0.03, 0.08))
                comments = int(likes * rng.uniform(0.04, 0.15))
                shares = int(likes * rng.uniform(0.03, 0.12))
                rows.append([f"POST{n:04d}", d, plat, t, topic, reach, impressions,
                             likes, comments, shares, followers])
                n += 1
    return pd.DataFrame(rows, columns=["post_id", "date", "platform", "post_type", "topic",
                                       "reach", "impressions", "likes", "comments",
                                       "shares", "followers"])


# ---------------------------------------------------------------- 5. CAMPAIGNS
def campaigns():
    data = [
        ("Python Course Admission Drive", "Google Ads", "2026-04-05", "2026-04-30", 18000),
        ("Summer Internship Awareness", "Instagram Ads", "2026-05-02", "2026-05-25", 12000),
        ("Full Stack Batch Launch", "Google Ads", "2026-05-15", "2026-06-10", 22000),
        ("IT Services B2B Outreach", "LinkedIn Ads", "2026-06-01", "2026-06-30", 25000),
        ("Data Science Demo Class", "Facebook Ads", "2026-06-10", "2026-07-05", 15000),
        ("AI & ChatGPT Workshop Promo", "Instagram Ads", "2026-07-01", "2026-07-20", 14000),
        ("Web Development Services Push", "LinkedIn Ads", "2026-07-10", "2026-08-05", 20000),
        ("Admission Season Mega Campaign", "Google Ads", "2026-07-25", "2026-08-31", 40000),
        ("AI Workshop Early Bird", "Instagram Ads", "2026-08-01", "2026-08-20", 18000),
        ("Excel & Power BI Workshop", "Facebook Ads", "2026-08-10", "2026-08-31", 9000),
        ("Career Guidance YouTube Series", "YouTube Ads", "2026-08-15", "2026-09-15", 16000),
        ("Resume & Interview Workshop", "LinkedIn Ads", "2026-09-01", "2026-09-20", 10000),
        ("Digital Marketing Course Offer", "Instagram Ads", "2026-09-05", "2026-09-28", 13000),
        ("IT Services Retargeting", "Google Ads", "2026-09-10", "2026-09-30", 17000),
    ]
    rows = []
    eff = {"Google Ads": (0.035, 0.07), "Instagram Ads": (0.025, 0.06),
           "LinkedIn Ads": (0.012, 0.09), "Facebook Ads": (0.018, 0.045),
           "YouTube Ads": (0.010, 0.04)}
    for i, (name, plat, s, e, spend) in enumerate(data, 1):
        imp = int(spend * rng.uniform(14, 30))
        ctr, lead_rate = eff[plat]
        clicks = int(imp * ctr * rng.uniform(0.8, 1.2))
        leads = int(clicks * lead_rate * rng.uniform(0.8, 1.3))
        rows.append([f"CMP{i:03d}", name, plat, s, e, spend, imp, clicks, leads])
    return pd.DataFrame(rows, columns=["campaign_id", "campaign_name", "platform", "start_date",
                                       "end_date", "spend_inr", "impressions", "clicks", "leads"])


# ------------------------------------------------------------- MESSINESS
SRC_VARIANTS = {
    "Google": ["google", "GOOGLE", "Google ", "Google Search"],
    "Instagram": ["instagram", "Insta", "INSTAGRAM"],
    "LinkedIn": ["linkedin", "Linkedin", "LINKEDIN "],
    "Facebook": ["facebook", "FB", "Facebook "],
    "YouTube": ["youtube", "Youtube", "YOUTUBE"],
    "Direct": ["direct", "Direct "],
    "Referral": ["referral", "Referal"],
}


def make_messy(df, cat_cols=(), num_cols=(), date_cols=("date",), dup_frac=0.02,
               miss_frac=0.03, variant_frac=0.10):
    df = df.copy()
    n = len(df)
    # mixed date formats (stored as text)
    for c in date_cols:
        d = pd.to_datetime(df[c])
        out = d.dt.strftime("%Y-%m-%d").astype(object)
        idx = rng.choice(n, int(n * 0.12), replace=False)
        out.iloc[idx] = d.iloc[idx].dt.strftime("%d/%m/%Y")
        idx = rng.choice(n, int(n * 0.06), replace=False)
        out.iloc[idx] = d.iloc[idx].dt.strftime("%d-%m-%Y")
        df[c] = out
    # inconsistent category spellings
    for c in cat_cols:
        idx = rng.choice(n, int(n * variant_frac), replace=False)
        for i in idx:
            v = df.iloc[i, df.columns.get_loc(c)]
            if v in SRC_VARIANTS:
                df.iloc[i, df.columns.get_loc(c)] = rng.choice(SRC_VARIANTS[v])
            elif isinstance(v, str):
                df.iloc[i, df.columns.get_loc(c)] = rng.choice([v.lower(), v.upper(), v + " "])
    # missing values
    for c in list(cat_cols) + list(num_cols):
        idx = rng.choice(n, int(n * miss_frac), replace=False)
        df[c] = df[c].astype(object)
        df.iloc[idx, df.columns.get_loc(c)] = np.nan
    # wrong entries: a few negative values
    for c in num_cols[:1]:
        idx = rng.choice(n, max(3, int(n * 0.002)), replace=False)
        col = pd.to_numeric(df[c], errors="coerce")
        col.iloc[idx] = -col.iloc[idx].abs()
        df[c] = col
    # exact duplicate rows
    dups = df.sample(int(n * dup_frac), random_state=1)
    df = pd.concat([df, dups]).sample(frac=1, random_state=2).reset_index(drop=True)
    return df


if __name__ == "__main__":
    web = website_traffic()
    enq = enquiries()
    reg = registrations()
    soc = social_media()
    cmp_ = campaigns()

    make_messy(web, ["source", "page"], ["users", "sessions"]).to_csv("website_traffic_raw.csv", index=False)
    make_messy(enq, ["source", "enquiry_type", "status"], []).to_csv("enquiries_raw.csv", index=False)
    make_messy(reg, ["source", "mode", "program"], []).to_csv("registrations_raw.csv", index=False)
    make_messy(soc, ["platform", "post_type"], ["reach", "likes"]).to_csv("social_media_raw.csv", index=False)
    make_messy(cmp_, ["platform"], ["clicks"], date_cols=("start_date", "end_date"),
               dup_frac=0.0, miss_frac=0.05).to_csv("campaigns_raw.csv", index=False)

    for name, df in [("website_traffic", web), ("enquiries", enq), ("registrations", reg),
                     ("social_media", soc), ("campaigns", cmp_)]:
        print(f"{name}: {len(df)} clean rows generated")
