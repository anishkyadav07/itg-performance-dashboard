 India Tech Group: Website & Digital Marketing Data Analysis Dashboard

**Learn, Grow & Succeed** | [www.indiatechgroup.com](https://www.indiatechgroup.com)

| | |
|---|---|
| **Intern** | Anishk Yadav |
| **Organisation** | India Tech Group |
| **Project duration** | 15 days (3 credits out of 30) |
| **Data period** | 01 April 2026 to 30 September 2026 |
| **Tools** | Python, Pandas, NumPy, Matplotlib, Plotly, Jupyter Notebook, Streamlit |

---

## 1. Project Overview

This project analyses India Tech Group's website, enquiry, course/workshop registration, social media and digital marketing campaign data. The goal is to find patterns, trends and high-performing areas, and to turn them into practical recommendations that improve India Tech Group's online presence, marketing activity and customer engagement.

The project covers the full data science workflow: data collection, cleaning, exploratory data analysis (EDA), visualisation, an interactive dashboard, business insights and recommendations.

> **Note on data:** The datasets used here are **sample (synthetic) data** created for this project using India Tech Group's services, courses and workshops. They are not real India Tech Group analytics. The method, code and dashboard work unchanged on real exports (Google Analytics, Search Console, social media insights, registration records).

---

## 2. Datasets

| Dataset | Raw file | Cleaned file | Rows (raw -> clean) | Description |
|---|---|---|---|---|
| Website traffic | `website_traffic_raw.csv` | `website_traffic_clean.csv` | 5,599 -> 5,490 | Daily users and sessions by page and traffic source |
| Enquiries | `enquiries_raw.csv` | `enquiries_clean.csv` | 721 -> 707 | Enquiries by source, type and status |
| Registrations | `registrations_raw.csv` | `registrations_clean.csv` | 974 -> 955 | Course and workshop registrations (online/offline) |
| Social media | `social_media_raw.csv` | `social_media_clean.csv` | 297 -> 292 | Post-level reach, impressions, likes, comments, shares |
| Campaigns | `campaigns_raw.csv` | `campaigns_clean.csv` | 14 -> 14 | Paid campaign spend, clicks and leads |

**Source:** Sample dataset prepared for project purposes (`generate_itg_dataset.py`, fixed random seed so results are reproducible).
**Date range:** 01-04-2026 to 30-09-2026 for all datasets.

### Key columns

| File | Columns |
|---|---|
| Website traffic | `date`, `source`, `page`, `users`, `sessions`, `bounce_rate_pct`, `avg_session_duration_sec` |
| Enquiries | `enquiry_id`, `date`, `source`, `enquiry_type`, `status` |
| Registrations | `registration_id`, `date`, `program`, `program_type`, `mode`, `source` |
| Social media | `post_id`, `date`, `platform`, `post_type`, `topic`, `reach`, `impressions`, `likes`, `comments`, `shares`, `followers` |
| Campaigns | `campaign_id`, `campaign_name`, `platform`, `start_date`, `end_date`, `spend_inr`, `impressions`, `clicks`, `leads` |

---

## 3. Data Cleaning

The raw files contain deliberate data quality problems, and each one was handled as follows:

| Problem | Treatment |
|---|---|
| Duplicate records (147 in total) | Removed (by record ID where available, otherwise exact duplicate rows) |
| Mixed date formats (`YYYY-MM-DD`, `DD/MM/YYYY`, `DD-MM-YYYY`) | Parsed with explicit formats into one standard date; a `month` column was added |
| Inconsistent categories (`google`, `GOOGLE`, `Google Search`, `Insta`, `FB`, `Referal`, extra spaces) | Mapped to one standard name per category |
| Negative values (users, sessions, reach, likes, clicks) | Treated as sign-entry errors and converted to absolute values |
| Missing numeric values | Filled with the median of the same page/platform (overall median as fallback) |
| Missing categories | Labelled `Unknown` and excluded from rankings |
| Column names | Standardised to lowercase with underscores |

---

## 4. Key Findings

All figures come from the cleaned sample dataset.

1. **Traffic peaked in August.** Monthly users grew from 13,303 (Apr) to 23,272 (Aug), an increase of about 75%, then fell 8.3% in September.
2. **Google dominates traffic.** Google brings 62.1% of all users (66,064), followed by Direct (14.8%) and Instagram (9.7%). Referral is only 1.7%.
3. **IT Services is the most visited service page** with 14,812 users, followed by Web Development (12,373) and the AI & ML Workshop page (12,056). Careers is lowest (3,187).
4. **LinkedIn punches above its traffic share.** It is 6.6% of traffic but 21.9% of enquiries, and leads in IT Services and App Development enquiries.
5. **Enquiries peaked in August** at 155 (up from 86 in April). Course Admission is the most common enquiry type (157). Overall conversion is 20.8%.
6. **Two programs drive 41% of registrations.** AI & ChatGPT Workshop (208) and Python Programming (186) together account for 394 of 955 registrations.
7. **Workshops spike in August.** Workshop registrations rose from 64 (Jul) to 115 (Aug), while course registrations stayed flat.
8. **Instagram is the best source for workshops.** It brought 131 of 422 workshop registrations, ahead of Google (87).
9. **Instagram leads social media on volume, not rate.** It has about half of total reach and engagement, but engagement rate is similar across platforms (6.1% to 6.4%). Reels have the highest average reach; Carousels have the highest engagement rate.
10. **Google Ads is the cheapest source of leads.** Cost per lead: Google 16.58 INR, Instagram 28.23, LinkedIn 54.03, Facebook 64.86, YouTube 102.56.

---

## 5. Recommendations (summary)

- Reduce dependence on Google by building referral and alumni programs and growing Instagram, LinkedIn and YouTube.
- Start Google Ads for admission season earlier (June/July) instead of waiting for August.
- Use LinkedIn for IT Services and App/Web Development, and add clear calls-to-action on the IT Services page.
- Make the AI & ChatGPT Workshop the main funnel and cross-sell Python and Data Science courses after it.
- Focus workshop promotion on Instagram.
- Run retargeting campaigns to counter the September decline.
- Add stronger calls-to-action on Home and service pages; improve low-traffic pages (Careers, Contact Us).
- Use Reels for reach and Carousels for engagement; present IT Services content as short reels and success stories.
- Cut or test-limit spend on high-cost channels (YouTube Ads, Facebook Ads).
- Add UTM tags and a mandatory "How did you hear about us?" field to improve tracking.

---

## 6. Dashboard

An interactive dashboard built with Streamlit.

**KPI cards:** Total Visitors, Total Enquiries, Total Registrations, Social Media Engagement, Top Performing Page, Top Course/Workshop, Best Traffic Source.

**Tabs:** Overview (monthly trends and performance comparison), Website, Enquiries, Registrations, Social Media, Campaigns.

**Filters:** Month, traffic/lead source, program type.

**Notes:**
- "Top Performing Page" excludes the Home page, because Home is the landing page and always ranks first.
- Campaign figures are not affected by the sidebar filters.

---

## 7. Project Structure

```
itg-performance-dashboard/
├── dashboard.py                  # Streamlit dashboard
├── itg_logo.png                  # India Tech Group logo
├── cleaned/                      # 5 cleaned CSV files (read by the dashboard)
├── raw/                          # 5 raw CSV files
├── project.ipynb                 # cleaning, EDA and visualisation
├── generate_itg_dataset.py       # sample dataset generator
├── charts/                       # exported PNG charts
├── screenshots/                  # dashboard screenshots
├── requirements.txt
└── README.md
```

---

## 8. How to Run

**1. Install the libraries**

```
python -m pip install pandas numpy matplotlib seaborn plotly streamlit jupyter
```

**2. Generate the sample data (optional)**

```
python generate_itg_dataset.py
```

**3. Run the notebook**

Open `project.ipynb` in Jupyter or VS Code. Set the `DATA` path at the top of the notebook to the folder containing the raw CSV files (the cleaning step creates the `cleaned` folder inside it). Run the cells from top to bottom: the cleaning cell must run before the EDA cell.

**4. Run the dashboard**

Keep `dashboard.py`, the `cleaned` folder and `itg_logo.png` together in the same folder (as in the structure above), then run from that folder:

```
python -m streamlit run dashboard.py
```

No path needs to be changed. If `itg_logo.png` is missing, the dashboard shows the text "ITG" instead of the logo.

The dashboard opens at `http://localhost:8501`.

---

## 9. Limitations

- The data is synthetic, so findings illustrate the method and should not be read as real India Tech Group performance.
- Sources with small samples (for example Referral and YouTube enquiries) give indicative, not conclusive, conversion rates.
- Campaign leads (ad-platform leads) and website enquiries are separate datasets and are not directly comparable.
- Differences in social media engagement rate between platforms are small.

---

## 10. Optional Extension

A simple forecast of next month's website traffic (moving average or linear regression) can be added to the notebook as a basic data science extension. It is not part of the core requirements.

---

**India Tech Group** | Learn, Grow & Succeed | [www.indiatechgroup.com](https://www.indiatechgroup.com)
