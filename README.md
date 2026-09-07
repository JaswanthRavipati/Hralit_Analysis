# 🧬 HRAlit Analysis

> **Interactive visualization and analysis of the Human Reference Atlas (HRA) literature database — uncovering publication trends, funding flows, global collaborations, and institutional research networks.**

[![Live Dashboard](https://img.shields.io/badge/🚀_Live_Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://hralitanalysis-ayt6ruxgmdwtbhneph6sdr.streamlit.app/)

---

## Problem

The **Human Reference Atlas (HRA)** is a comprehensive, open, 3D atlas of the human body at the cellular level. Thousands of research publications contribute to the HRA across organs, institutions, and countries — but there is no unified way to understand:

- **Which organs** are receiving the most research attention, and how is that changing?
- **Which funders** (NIH, Wellcome, NSFC, etc.) are driving this research, and through which institutions?
- **How do countries and institutions collaborate** on HRA-relevant research?
- **What will future publication trends look like** for key organs?

This project provides **5 interactive visualizations** deployed as a live Streamlit dashboard to answer these questions, enabling HRA stakeholders (researchers, funders, policy makers) to make data-driven decisions about resource allocation and collaboration priorities.

---

## Visualizations

| # | Visualization | What It Shows |
|---|--------------|---------------|
| 1 | **Grant-Linkage Sankey** | Funding flows from major funders through organs to research outputs (publications & datasets) |
| 2 | **Publication Trends & Forecast** | Organ-wise publication counts (1950–2023) with animated year-by-year build-up and 5-year polynomial regression forecast with uncertainty bands |
| 3 | **Institution–Funder Heatmap** | Which institutions in a selected country are funded by which agencies, with cell intensity = co-linked publication counts |
| 4 | **Global Collaboration Map** | International co-publication networks on a world map with bubble size = author counts, color = funding intensity |
| 5 | **Institution Collaborations** | Interactive Plotly bipartite network — hover over any edge to see the exact co-publication count between two institutions across countries |

---

## Key Insights

- **Lung research surged 41%** (2015–2021), likely driven by COVID-19, while brain research plateaued at 14% growth despite being the 2nd largest field.
- **Liver** is the most-published organ at ~1.2M publications, with **brain** (~1.05M) and **heart** (~940K) following.
- At the current exponential growth rate, HRA-relevant publications could **nearly double within 5–7 years**, requiring proportional scaling of atlas curation efforts.
- The polynomial regression forecast achieves an approximate **MAPE of 4.4%** across the top 5 organs.

---

## Project Structure

```
HRAlit-Analysis/
│
├── app.py                              # Standalone Streamlit dashboard (4 tabs, matplotlib)
├── requirements.txt                    # Python dependencies
│
├── hf_deploy_v4/                       # 🚀 Latest deployed version (Hugging Face Space)
│   ├── app.py                          # Dashboard app with Plotly institution collabs
│   ├── requirements.txt               # Runtime dependencies (streamlit, plotly, etc.)
│   ├── preaggregate_inst_collabs.py    # Script to build institution collaboration CSV
│   ├── README.md                       # HF Space metadata
│   └── data/                           # Pre-aggregated datasets for the dashboard
│       ├── sankey_funder_organ_year.csv
│       ├── trends_organ_year.csv
│       ├── heatmap_inst_funder.csv
│       ├── geo_authors.csv
│       ├── geo_collaborations.csv
│       ├── geo_funding_intensity.csv
│       ├── geo_pubs.csv
│       ├── inst_collaborations.csv     # 252K rows — full co-authorship data
│       ├── dataset_counts.csv
│       └── world_boundaries.json
│
├── Visualization Python Files/          # Standalone interactive scripts (ipywidgets)
│   ├── viz_4_1_geo_interactive.py
│   ├── viz_4_2_sankey_interactive.py
│   ├── viz_4_3_trends_interactive.py
│   ├── viz_4_4_heatmap_interactive.py
│   └── viz_4_5_inst_collab_interactive.py
│
├── Visualization_Notebooks/             # Jupyter notebooks (same as above, .ipynb format)
│   ├── viz_4_1_geo_interactive.ipynb
│   ├── viz_4_2_sankey_interactive.ipynb
│   ├── viz_4_3_trends_interactive.ipynb
│   ├── viz_4_4_heatmap_interactive.ipynb
│   └── viz_4_5_inst_collab_interactive.ipynb
│
├── Client_Project_Info_Viz_Dataset/     # Raw HRAlit database tables
│   ├── hralit_institution.csv
│   ├── hralit_organ.csv
│   ├── hralit_funder_cleaned.csv
│   ├── hralit_author.csv.gz
│   ├── hralit_author_institution.csv.gz
│   ├── hralit_funding.csv.gz
│   ├── hralit_publication.csv.gz        # (gitignored — >100MB)
│   └── ...                              # Additional tables
│
└── visualization_sketches/              # Early-stage design mockups
    ├── 4_1_organ_dashboard.png
    ├── 4_2_trend_prediction.png
    └── ...
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Dashboard** | Streamlit |
| **Visualizations** | Matplotlib, Plotly |
| **Forecasting** | Polynomial Regression (scikit-learn) |
| **Data Processing** | Pandas, NumPy |
| **Notebooks** | Jupyter + ipywidgets |
| **Deployment** | Hugging Face Spaces |

---

## Getting Started

### Run the Dashboard Locally

```bash
# Clone the repo
git clone https://github.com/JaswanthRavipati/Hralit_Analysis.git
cd HRAlit-Analysis/hf_deploy_v4

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

### Run the Notebooks

```bash
cd HRAlit-Analysis
pip install jupyter ipywidgets plotly matplotlib pandas numpy scikit-learn

# Launch Jupyter
jupyter notebook Visualization_Notebooks/
```

> **Note:** The notebooks load raw data from `Client_Project_Info_Viz_Dataset/`. Some compressed files (`.csv.gz`) exceed GitHub's 100MB limit and are gitignored — contact the authors for the full dataset.

---

## Data Source

All data is sourced from the **HRAlit Database** (Kong & Börner, 2024) — a curated collection of publications, funding records, author affiliations, and institutional metadata related to the Human Reference Atlas.

- **Publications:** ~384K records (1950–2023)
- **Organs:** 6 primary organs tracked (brain, liver, heart, kidney, lung, skin)
- **Funders:** 11 major agencies (NIH, MRC, NSFC, Wellcome, DFG, HHMI, CIHR, BHF, JSPS, NSF, and more)
- **Institutions:** Global coverage across 25+ countries

---

## Future Work

- **ARIMA / time-series models** for more robust publication forecasting that captures sequential patterns and handles external shocks
- **Additional organ coverage** as the HRA database expands
- **Author-level collaboration networks** for finer-grained analysis

---

## Authors

Developed as part of the Indiana University Information Visualization course (E538/E438).

---

## License

This project is for academic and research purposes. The underlying HRAlit data is subject to its original licensing terms.
