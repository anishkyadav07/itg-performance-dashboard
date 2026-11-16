"""
India Tech Group - Website & Digital Marketing Performance Dashboard
Learn, Grow & Succeed | www.indiatechgroup.com
 
Folder layout (keep these together):
    itg project files/
        dashboard.py
        itg_logo.png          (official ITG logo)
        cleaned/              (the 5 *_clean.csv files)
 
Run:  streamlit run dashboard.py
"""
from pathlib import Path
 
import pandas as pd
import plotly.express as px
import streamlit as st
 
# ------------------------------------------------------------------ config
st.set_page_config(page_title="India Tech Group | Performance Dashboard",
                   page_icon="📊", layout="wide")
 
BASE = Path(__file__).parent
CLEAN = BASE / "cleaned"
LOGO = BASE / "itg_logo.png"
 
NAVY, ORANGE, GREEN, GREY = "#1F3A5F", "#F28C28", "#2E9E6B", "#9AA5B1"  # logo ke colors se match kar lena
PALETTE = [NAVY, ORANGE, GREEN, "#7B5EA7", "#D64550", GREY, "#3FA7D6", "#B08968"]
TAGLINE = "Learn, Grow & Succeed"
WEBSITE = "www.indiatechgroup.com"
 
st.markdown(f"""
<style>
.kpi {{background:#fff;border:1px solid #E3E8EF;border-left:6px solid {NAVY};border-radius:10px;
      padding:14px 16px;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,.06);}}
.kpi .label {{font-size:.8rem;color:#5B6776;text-transform:uppercase;letter-spacing:.04em;}}
.kpi .value {{font-size:1.6rem;font-weight:700;color:{NAVY};line-height:1.25;}}
.kpi .sub {{font-size:.8rem;color:{ORANGE};font-weight:600;}}
</style>
""", unsafe_allow_html=True)
 
 
# ------------------------------------------------------------------ helpers
def chart(fig, height=380):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=50, b=10),
                      title_font=dict(size=15), legend_title_text="")
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:  # older Streamlit
        st.plotly_chart(fig, use_container_width=True)
 
 
def kpi(col, label, value, sub=""):
    col.markdown(f'<div class="kpi"><div class="label">{label}</div>'
                 f'<div class="value">{value}</div><div class="sub">{sub}&nbsp;</div></div>',
                 unsafe_allow_html=True)
 
 
def known(df, col):
    return df[df[col] != "Unknown"]
 
 
def mlabel(m):
    return pd.Period(m).strftime("%b %Y")
 
 
def with_month_label(df):
    df = df.copy()
    df["Month"] = df["month"].map(mlabel)
    return df
 
 
# ------------------------------------------------------------------ data
@st.cache_data
def load_data():
    web = pd.read_csv(CLEAN / "website_traffic_clean.csv", parse_dates=["date"])
    enq = pd.read_csv(CLEAN / "enquiries_clean.csv", parse_dates=["date"])
    reg = pd.read_csv(CLEAN / "registrations_clean.csv", parse_dates=["date"])
    soc = pd.read_csv(CLEAN / "social_media_clean.csv", parse_dates=["date"])
    camp = pd.read_csv(CLEAN / "campaigns_clean.csv", parse_dates=["start_date", "end_date"])
    soc["engagement"] = soc["likes"] + soc["comments"] + soc["shares"]
    soc["engagement_rate"] = soc["engagement"] / soc["reach"] * 100
    camp["ctr"] = camp["clicks"] / camp["impressions"] * 100
    camp["lead_rate"] = camp["leads"] / camp["clicks"] * 100
    camp["cost_per_lead"] = camp["spend_inr"] / camp["leads"]
    return web, enq, reg, soc, camp
 
 
try:
    web, enq, reg, soc, camp = load_data()
except FileNotFoundError as e:
    st.error(f"Cleaned file nahi mili: {e.filename}\n\n"
             "dashboard.py ke saath `cleaned` folder (5 *_clean.csv files ke saath) rakho.")
    st.stop()
 
# ------------------------------------------------------------------ header
h1, h2 = st.columns([1, 6])
with h1:
    if LOGO.exists():
        st.image(str(LOGO), width=120)
    else:
        st.markdown(f"### **ITG**")
with h2:
    st.title("India Tech Group: Performance Dashboard")
    st.caption(f"{TAGLINE}  |  {WEBSITE}  |  Data period: 01 Apr 2026 to 30 Sep 2026 (sample dataset)")
 
# ------------------------------------------------------------------ sidebar filters
st.sidebar.header("Filters")
all_months = sorted(web["month"].unique())
sel_months = st.sidebar.multiselect("Month", all_months, default=all_months, format_func=mlabel)
all_sources = sorted(set(web["source"]) | set(enq["source"]) | set(reg["source"]))
sel_sources = st.sidebar.multiselect("Traffic / lead source", all_sources, default=all_sources)
sel_types = st.sidebar.multiselect("Program type", ["Course", "Workshop"], default=["Course", "Workshop"])
st.sidebar.caption("Month filter sab data par lagta hai. Source filter website, enquiries aur "
                   "registrations par. Program type sirf registrations par. Campaigns tab par koi filter nahi.")
 
if not (sel_months and sel_sources and sel_types):
    st.warning("Har filter mein kam se kam ek option select karo.")
    st.stop()
 
webf = web[web["month"].isin(sel_months) & web["source"].isin(sel_sources)]
enqf = enq[enq["month"].isin(sel_months) & enq["source"].isin(sel_sources)]
regf = reg[reg["month"].isin(sel_months) & reg["source"].isin(sel_sources) & reg["program_type"].isin(sel_types)]
socf = soc[soc["month"].isin(sel_months)]
 
# ------------------------------------------------------------------ KPIs
pages = known(webf, "page").query("page != 'Home'").groupby("page")["users"].sum().sort_values(ascending=False)
programs = known(regf, "program")["program"].value_counts()
sources = known(webf, "source").groupby("source")["users"].sum().sort_values(ascending=False)
 
top_page = pages.index[0] if len(pages) else "-"
top_page_sub = f"{pages.iloc[0]:,} users (Home ko chhodke)" if len(pages) else ""
top_prog = programs.index[0] if len(programs) else "-"
top_prog_sub = f"{programs.iloc[0]:,} registrations" if len(programs) else ""
best_src = sources.index[0] if len(sources) else "-"
best_src_sub = f"{sources.iloc[0] / sources.sum() * 100:.1f}% of traffic" if len(sources) else ""
eng_total = int(socf["engagement"].sum())
eng_rate = socf["engagement"].sum() / socf["reach"].sum() * 100 if len(socf) and socf["reach"].sum() else 0
 
r1 = st.columns(4)
kpi(r1[0], "Total Visitors", f"{webf['users'].sum():,}", f"{webf['sessions'].sum():,} sessions")
kpi(r1[1], "Total Enquiries", f"{len(enqf):,}",
    f"{(known(enqf, 'status')['status'] == 'Converted').mean() * 100:.1f}% converted" if len(known(enqf, 'status')) else "")
kpi(r1[2], "Total Registrations", f"{len(regf):,}",
    f"{(regf['program_type'] == 'Workshop').sum():,} workshop | {(regf['program_type'] == 'Course').sum():,} course")
kpi(r1[3], "Social Media Engagement", f"{eng_total:,}", f"{eng_rate:.2f}% of reach")
r2 = st.columns(3)
kpi(r2[0], "Top Performing Page", top_page, top_page_sub)
kpi(r2[1], "Top Course / Workshop", top_prog, top_prog_sub)
kpi(r2[2], "Best Traffic Source", best_src, best_src_sub)
 
# ------------------------------------------------------------------ tabs
tabs = st.tabs(["Overview", "Website", "Enquiries", "Registrations", "Social Media", "Campaigns"])
 
# ---- Overview
with tabs[0]:
    st.subheader("Monthly Trends")
    mu = with_month_label(webf.groupby("month", as_index=False)["users"].sum())
    me = with_month_label(enqf.groupby("month").size().reset_index(name="enquiries"))
    mr = with_month_label(regf.groupby("month").size().reset_index(name="registrations"))
    c1, c2, c3 = st.columns(3)
    with c1:
        chart(px.line(mu, x="Month", y="users", markers=True, title="Website Users",
                      color_discrete_sequence=[NAVY]), 320)
    with c2:
        chart(px.bar(me, x="Month", y="enquiries", title="Enquiries",
                     color_discrete_sequence=[ORANGE], text="enquiries"), 320)
    with c3:
        chart(px.bar(mr, x="Month", y="registrations", title="Registrations",
                     color_discrete_sequence=[GREEN], text="registrations"), 320)
 
    perf = pd.DataFrame({
        "Website users": webf.groupby("month")["users"].sum(),
        "Enquiries": enqf.groupby("month").size(),
        "Registrations": regf.groupby("month").size(),
        "Social engagement": socf.groupby("month")["engagement"].sum(),
    }).dropna()
    if len(perf) >= 2:
        idx = (perf / perf.iloc[0] * 100).reset_index()
        idx["Month"] = idx["month"].map(mlabel)
        base = mlabel(perf.index[0])
        fig = px.line(idx.melt(id_vars=["month", "Month"], var_name="Metric", value_name="Index"),
                      x="Month", y="Index", color="Metric", markers=True,
                      title=f"Monthly Performance Comparison ({base} = 100)",
                      color_discrete_sequence=PALETTE)
        fig.add_hline(y=100, line_dash="dash", line_color="black", line_width=1)
        chart(fig, 400)
    else:
        st.info("Performance comparison ke liye kam se kam 2 months select karo.")
 
# ---- Website
with tabs[1]:
    a, b = st.columns(2)
    with a:
        s = sources.reset_index()
        s["share"] = (s["users"] / s["users"].sum() * 100).round(1).astype(str) + "%"
        chart(px.bar(s, x="source", y="users", text="share", title="Users by Traffic Source",
                     color_discrete_sequence=[NAVY], labels={"source": "Traffic source", "users": "Users"}))
    with b:
        p = known(webf, "page").groupby("page")["users"].sum().sort_values().reset_index()
        p["color"] = p["page"].map(lambda x: "IT Services" if x == "IT Services" else "Other pages")
        chart(px.bar(p, x="users", y="page", orientation="h", color="color", text="users",
                     title="Users by Page",
                     color_discrete_map={"IT Services": ORANGE, "Other pages": NAVY},
                     labels={"users": "Users", "page": "Page"}))
    st.markdown("#### Monthly traffic")
    mt = with_month_label(webf.groupby("month", as_index=False)[["users", "sessions"]].sum())
    chart(px.line(mt.melt(id_vars=["month", "Month"], var_name="Metric", value_name="Count"),
                  x="Month", y="Count", color="Metric", markers=True,
                  color_discrete_sequence=[NAVY, ORANGE]), 340)
    st.markdown("#### IT Services page performance")
    it = webf[webf["page"] == "IT Services"]
    k1, k2, k3 = st.columns(3)
    k1.metric("IT Services users", f"{it['users'].sum():,}")
    k2.metric("Share of all page traffic", f"{it['users'].sum() / max(webf['users'].sum(), 1) * 100:.1f}%")
    k3.metric("Avg bounce rate", f"{it['bounce_rate_pct'].mean():.1f}%" if len(it) else "-")
    itm = with_month_label(it.groupby("month", as_index=False)["users"].sum())
    its = known(it, "source").groupby("source")["users"].sum().sort_values(ascending=False).reset_index()
    x1, x2 = st.columns(2)
    with x1:
        chart(px.bar(itm, x="Month", y="users", title="IT Services: users by month",
                     color_discrete_sequence=[ORANGE], text="users"), 320)
    with x2:
        chart(px.bar(its, x="source", y="users", title="IT Services: users by source",
                     color_discrete_sequence=[NAVY], text="users",
                     labels={"source": "Source", "users": "Users"}), 320)
 
# ---- Enquiries
with tabs[2]:
    a, b = st.columns(2)
    cnt = known(enqf, "source")["source"].value_counts().reset_index()
    cnt.columns = ["source", "enquiries"]
    valid = known(enqf, "status")
    conv = (known(valid, "source").groupby("source")["status"]
            .apply(lambda s: (s == "Converted").mean() * 100).round(1).reset_index(name="conversion"))
    cs = cnt.merge(conv, on="source", how="left")
    with a:
        chart(px.bar(cs, x="source", y="enquiries", text="enquiries", title="Enquiries by Source",
                     color_discrete_sequence=[NAVY], labels={"source": "Source", "enquiries": "Enquiries"}))
    with b:
        chart(px.bar(cs.sort_values("conversion", ascending=False), x="source", y="conversion",
                     text="conversion", title="Conversion Rate by Source (%)",
                     color_discrete_sequence=[ORANGE], labels={"source": "Source", "conversion": "Conversion %"}))
        st.caption("Chhote sample (kam enquiries) wale sources ka rate sirf indication hai.")
    c, d = st.columns(2)
    with c:
        et = known(enqf, "enquiry_type")["enquiry_type"].value_counts().sort_values().reset_index()
        et.columns = ["type", "enquiries"]
        chart(px.bar(et, x="enquiries", y="type", orientation="h", text="enquiries",
                     title="Enquiries by Type", color_discrete_sequence=[NAVY],
                     labels={"type": "Enquiry type", "enquiries": "Enquiries"}))
    with d:
        e2 = enqf[(enqf["source"] != "Unknown") & (enqf["enquiry_type"] != "Unknown")]
        if len(e2):
            ct = pd.crosstab(e2["source"], e2["enquiry_type"])
            chart(px.imshow(ct, text_auto=True, aspect="auto", color_continuous_scale="Blues",
                            title="Source vs Enquiry Type",
                            labels=dict(x="Enquiry type", y="Source", color="Enquiries")))
 
# ---- Registrations
with tabs[3]:
    a, b = st.columns(2)
    pr = (known(regf, "program").groupby(["program", "program_type"]).size()
          .reset_index(name="registrations").sort_values("registrations"))
    with a:
        chart(px.bar(pr, x="registrations", y="program", color="program_type", orientation="h",
                     text="registrations", title="Registrations by Course / Workshop",
                     color_discrete_map={"Course": NAVY, "Workshop": ORANGE},
                     labels={"program": "Program", "registrations": "Registrations", "program_type": "Type"}))
    with b:
        mt2 = with_month_label(regf.groupby(["month", "program_type"]).size().reset_index(name="registrations"))
        chart(px.bar(mt2, x="Month", y="registrations", color="program_type", text="registrations",
                     title="Monthly Registrations (Course vs Workshop)",
                     color_discrete_map={"Course": NAVY, "Workshop": ORANGE},
                     labels={"registrations": "Registrations", "program_type": "Type"}))
    c, d = st.columns(2)
    with c:
        md = known(regf, "mode").groupby(["program_type", "mode"]).size().reset_index(name="registrations")
        chart(px.bar(md, x="program_type", y="registrations", color="mode", barmode="group", text="registrations",
                     title="Online vs Offline",
                     color_discrete_map={"Online": NAVY, "Offline": ORANGE},
                     labels={"program_type": "Program type", "registrations": "Registrations", "mode": "Mode"}))
    with d:
        ws = known(regf[regf["program_type"] == "Workshop"], "source")["source"].value_counts().reset_index()
        ws.columns = ["source", "registrations"]
        chart(px.bar(ws, x="source", y="registrations", text="registrations",
                     title="Workshop Registrations by Source", color_discrete_sequence=[ORANGE],
                     labels={"source": "Source", "registrations": "Registrations"}))
 
# ---- Social media
with tabs[4]:
    if socf.empty:
        st.info("Selected months ke liye social data nahi hai.")
    else:
        sp = (known(socf, "platform").groupby("platform")
              .agg(reach=("reach", "sum"), engagement=("engagement", "sum"), rate=("engagement_rate", "mean"))
              .round(2).reset_index())
        a, b = st.columns(2)
        with a:
            chart(px.bar(sp, x="platform", y="engagement", text="engagement",
                         title="Total Engagement by Platform (likes + comments + shares)",
                         color_discrete_sequence=[NAVY], labels={"platform": "Platform", "engagement": "Engagement"}))
        with b:
            chart(px.bar(sp, x="platform", y="rate", text="rate", title="Average Engagement Rate (%)",
                         color_discrete_sequence=[ORANGE], labels={"platform": "Platform", "rate": "Engagement rate %"}))
            st.caption("Platforms ke engagement rate mein farak chhota hai; volume mein Instagram aage hai.")
        c, d = st.columns(2)
        with c:
            pt = (known(socf, "post_type").groupby("post_type")
                  .agg(avg_reach=("reach", "mean"), avg_engagement=("engagement", "mean"))
                  .round(1).reset_index().sort_values("avg_reach"))
            chart(px.bar(pt.melt(id_vars="post_type", var_name="Metric", value_name="Average"),
                         x="Average", y="post_type", color="Metric", barmode="group", orientation="h",
                         title="Post Type: Avg Reach vs Avg Engagement",
                         color_discrete_sequence=[NAVY, ORANGE], labels={"post_type": "Post type"}))
        with d:
            tp = (socf.groupby("topic")["engagement"].mean().round(1).sort_values().reset_index())
            chart(px.bar(tp, x="engagement", y="topic", orientation="h", text="engagement",
                         title="Topic: Avg Engagement per Post", color_discrete_sequence=[GREEN],
                         labels={"topic": "Topic", "engagement": "Avg engagement"}))
        fg = known(socf, "platform").groupby(["month", "platform"], as_index=False)["followers"].max()
        fg["Month"] = fg["month"].map(mlabel)
        chart(px.line(fg, x="Month", y="followers", color="platform", markers=True,
                      title="Followers Growth", color_discrete_sequence=PALETTE,
                      labels={"followers": "Followers", "platform": "Platform"}), 360)
        st.markdown("#### Top 5 posts by engagement")
        top5 = socf.nlargest(5, "engagement")[["date", "platform", "post_type", "topic", "reach", "engagement"]].copy()
        top5["date"] = top5["date"].dt.strftime("%d-%m-%Y")
        st.dataframe(top5, hide_index=True)
 
# ---- Campaigns
with tabs[5]:
    st.caption("Campaign data ke liye sidebar filters apply nahi hote.")
    cp = (camp.groupby("platform")[["spend_inr", "clicks", "leads"]].sum().reset_index())
    cp["cost_per_lead"] = (cp["spend_inr"] / cp["leads"]).round(2)
    cp = cp.sort_values("cost_per_lead")
    a, b = st.columns(2)
    with a:
        chart(px.bar(cp, x="platform", y="cost_per_lead", text="cost_per_lead",
                     title="Cost per Lead by Ad Platform (INR)", color_discrete_sequence=[NAVY],
                     labels={"platform": "Ad platform", "cost_per_lead": "Cost per lead (INR)"}))
    with b:
        chart(px.bar(cp.melt(id_vars="platform", value_vars=["spend_inr", "leads"], var_name="Metric", value_name="Value"),
                     x="platform", y="Value", color="Metric", barmode="group",
                     title="Spend (INR) vs Leads", color_discrete_sequence=[ORANGE, GREEN],
                     labels={"platform": "Ad platform"}))
    st.markdown("#### All campaigns")
    tbl = camp.sort_values("cost_per_lead")[["campaign_name", "platform", "spend_inr", "impressions", "clicks",
                                              "leads", "ctr", "lead_rate", "cost_per_lead"]].round(2)
    tbl.columns = ["Campaign", "Platform", "Spend (INR)", "Impressions", "Clicks", "Leads",
                   "CTR %", "Lead rate %", "Cost per lead (INR)"]
    st.dataframe(tbl, hide_index=True)
    st.caption("Campaign leads ad-platform ke leads hain; website enquiries alag dataset hai.")
 
# ------------------------------------------------------------------ footer
st.divider()
st.caption(f"India Tech Group  |  {TAGLINE}  |  {WEBSITE}  |  Sample dataset for internship project")
 








