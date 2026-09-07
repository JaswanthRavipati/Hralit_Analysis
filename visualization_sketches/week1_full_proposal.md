# Publication, Funding, and Experimental Data in Support of Human Reference Atlas Construction and Usage

**Authors**: Athkia, Tejas Sarma, Sarrthak, Jonathan Browning, Jaswanth
**Affiliation**: Indiana University, Luddy School of Informatics, Computing, and Engineering (E538/E438)

> **Fig. 1.** *(Visual abstract placeholder — final version should include a graphic showing: HRAlit data → Analyses (trends, networks, predictions) → Interactive Visualizations → Insights for HRA construction)*

---

## 1. INTRODUCTION AND PRIOR WORK — *@Athkia*

The Human Reference Atlas (HRA) is a multi-consortia effort to map all 37 trillion cells in the healthy human body. Over five releases since 2020, the HRA has produced 295 cumulative digital objects; **HRA v1.4** — the version used in this project — comprises **136 digital objects** spanning 31 organs with 4,279 anatomical structures, 1,210 cell types, and 2,089 biomarkers. The **HRAlit database** (Kong & Börner, 2024) compiles 22 tables with ~20.9 million records, linking these v1.4 digital objects to 583,117 experts, 7.1 million PubMed publications, 896,680 funded projects, and 1,816 experimental datasets.

While HRAlit is a powerful data resource, it currently lacks interactive visual interfaces that would enable stakeholders to explore publication trends, analyze international collaboration patterns (especially between the USA and China), understand grant-linkage patterns, identify key experts, and forecast likely future research trends. Our project addresses this gap by building **interactive visualizations with predictive analytics** that mine the HRAlit database for actionable insights in support of systematic HRA construction.

### Research Questions

1. How have publication and funding trends for HRA-relevant organs evolved over the past 20 years, and what can we predict for the next 5 years?
2. How does international research collaboration — particularly between the USA and China — manifest in co-authorship networks, and how has it changed over time?
3. Which funders are most frequently associated with internationally collaborative research for specific countries?
4. Who are the key experts (hub nodes) in organ-specific co-authorship networks, and how do collaboration patterns evolve across time periods?
5. What patterns in past publication/funding data can inform future HRA data acquisition priorities?

### Success Criteria

| Research Question | Evaluation Approach |
|---|---|
| RQ1 — Trend forecasting | Target: MAPE around 15% or lower on held-out 2021–2023 data when trained on 2003–2020 |
| RQ2 — USA–China collaboration | Year-over-year trend validated against external bibliometric reports (e.g., NSF S&E Indicators) |
| RQ3 — Top funders by country | Rankings cross-checked against NIH RePORTER and NSFC public records for plausibility |
| RQ4 — Network centrality | Evaluate whether central authors substantially overlap with known HRA creators/reviewers for that organ |
| RQ5 — Pattern recognition | Stakeholder task-completion test: assess whether sample questions are answerable via the dashboard within a reasonable time |

### Prior Work

**Within the HRA ecosystem**: The HRA Exploration User Interface (EUI) provides 3D body-map browsing of spatially registered tissue data. The ASCT+B Reporter visualizes anatomical structure–cell type–biomarker hierarchies. The HRA Organ Gallery enables VR-based organ exploration. Vitessce supports multi-modal single-cell data visualization within HuBMAP. However, **none of these tools address publication metadata, funding analysis, expert networks, or predictive trends**.

**Bibliometric visualization**: VOSviewer (van Eck & Waltman, 2010) constructs co-authorship and keyword co-occurrence networks from publication databases. CiteSpace (Chen, 2006) focuses on temporal evolution of bibliometric networks and emerging trends. Both are general-purpose and lack HRA-specific integration with experimental data or ontologies.

**Funding visualization**: NIH World RePORTER tracks global biomedical research investments via interactive maps. The NIH Funding Drug Innovation Dashboard links NIH funding to publications. SCIMaP (UPenn) visualizes economic impacts of federal health research funding geographically.

**Gap**: No existing tool provides an integrated visual interface connecting HRA-specific publication, funding, expert, and experimental-data dimensions with **predictive analytics and international collaboration analysis**. This is precisely what our project delivers.

---

### 1.1 Stakeholder Groups — *@Tejas*

The HRAlit database serves multiple distinct stakeholder groups with varying roles, expertise levels, and visualization needs. We identify **six primary groups**:

#### 1. HRA Construction Team (Atlas Builders)
**Who**: ~158 experts (101 creators, 99 reviewers) who author and review HRA digital objects — ASCT+B tables, FTU illustrations, OMAPs, and 3D reference organs. Domain experts in anatomy, cell biology, and pathology across 20+ consortia.

**Interaction with data**: Need to identify which organs lack sufficient publication evidence, find potential new creators/reviewers with relevant expertise, and assess ontology term coverage. They use HRAlit to decide what digital objects to build next and who to recruit.

**Example question**: *"Which organs have the fewest ASCT+B-linked publications, and who are the top-publishing authors in those areas that haven't yet been recruited?"*

#### 2. Funding Agencies & Program Officers
**Who**: Officials at NIH (HuBMAP, SenNet, KPMP programs), NSF, DFG, Wellcome Trust, and other organizations overseeing grant portfolios.

**Interaction with data**: Evaluate funding distribution across organs, track ROI in terms of publications/datasets per grant, identify strategic gaps, and understand which funders are most likely to cooperate with specific countries.

**Example question**: *"How does NIH kidney funding compare to liver funding in resulting publications, and which international funders most frequently co-fund with the US?"*

#### 3. Biomedical Researchers & Domain Scientists
**Who**: The broader scientific community — 583,117 authors in HRAlit — whose work touches anatomy, cell biology, genomics, or organ-specific clinical research.

**Interaction with data**: Find collaborators (especially international), discover datasets for their organ of interest, identify highly-cited publications, and understand emerging research trends.

**Example question**: *"Who are the most prolific authors publishing on pancreatic cell types, and which experimental datasets are available?"*

#### 4. Ontology Engineers & Biocurators
**Who**: Specialists maintaining biomedical ontologies — Uberon, Cell Ontology (CL), FMA, HGNC. They standardize biological terms for cross-database interoperability.

**Interaction with data**: 2,619 HRA terms have temporary IDs (HRA-TEMP) without standard ontology entries. Engineers need to prioritize which terms to formalize based on publication frequency and dataset usage.

**Example question**: *"Which organ has the most HRA-TEMP terms, and how often do publications reference those terms?"*

#### 5. Data Portal Administrators & Curators
**Who**: Teams operating HuBMAP, CZ CELLxGENE, GTEx, KPMP, and GUDMAP platforms that ingest and serve tissue data.

**Interaction with data**: Assess dataset coverage by organ, track donor demographics, evaluate assay type representation, and see how portal datasets link to publications.

**Example question**: *"What is the age/sex distribution of kidney donors, and how many datasets have linked publications?"*

#### 6. Science Policy Makers & Institutional Administrators
**Who**: University research officers, government science advisors, and strategic planners making decisions about research direction and investment.

**Interaction with data**: Need macro-level overviews — geographic expertise distribution, national funding trends, international collaboration trajectories, and institutional benchmarking.

**Example question**: *"Which countries and institutions contribute most to HRA research, and how has USA–China collaboration changed over the past decade?"*

| # | Stakeholder Group | Primary Role | Expertise Level | Key Data Tables |
|---|---|---|---|---|
| 1 | HRA Construction Team | Build & review atlas | Expert | `creator`, `reviewer`, `digital_objects`, `asctb_publication` |
| 2 | Funding Agencies | Allocate grants, assess ROI | Intermediate | `funding`, `funder_cleaned`, `pub_funding_funder` |
| 3 | Biomedical Researchers | Produce publications & data | Variable | `publication`, `author`, `publication_author` |
| 4 | Ontology Engineers | Maintain term standards | Expert | `anatomical_structures`, `cell_types`, `biomarkers` |
| 5 | Data Portal Admins | Manage data platforms | Intermediate | `dataset`, `donor`, `other_publication` |
| 6 | Policy Makers | Strategic oversight | Low | `institution`, `author_institution`, `funder_cleaned` |

---

### 1.2 Stakeholder Needs — *@Sarrthak*

| Stakeholder Group | Key Needs |
|---|---|
| **HRA Construction Team** | Identify expert candidates; assess which ASCT+B rows lack evidence; see which organs have richest experimental data |
| **Funding Agencies** | Visualize funding distribution across organs; spot underfunded areas; identify top funders for international cooperation; predict future funding trends |
| **Biomedical Researchers** | Discover leading experts; find organ-specific datasets and publications; identify international collaborators; see emerging research trends |
| **Ontology Engineers** | See HRA-TEMP vs. standard ontology coverage by organ; prioritize ontology extension requests |
| **Data Portal Admins** | Understand dataset coverage by organ/source; track donor demographics; assess data growth |
| **Policy Makers** | High-level dashboards for investment landscape; geographic expertise distribution; USA–China collaboration trends; growth forecasts |

**Cross-cutting needs**: Filtering by organ, time period, and country; drill-down from overview to detail; trend prediction for the next 5 years; export capabilities; responsive, browser-based interfaces.

---

## 2. DATA ACQUISITION — *@Jonathan Browning*

### 2.1 Data Sources

The HRAlit dataset was downloaded from Figshare ([DOI: 10.6084/m9.figshare.24580669.v2](https://doi.org/10.6084/m9.figshare.24580669.v2)):

- **1 compressed SQL file** (`hralit.sql.gz`, ~605 MB) — full database dump
- **22 CSV files** (some gzipped) — one per table, ~612 MB compressed

| Source | Data Type | Access |
|---|---|---|
| HRA v1.4 (HuBMAP) | Digital objects, ASCT+B tables, creators, reviewers | CCF-HRA releases |
| PubMed | 7.1M publications, authors, funding | Literature search (31 organ names) |
| OpenAlex | Cleaned institution & funder names | API matching (ORCID/author ID) |
| HuBMAP Portal | Experimental datasets, donors | Portal API |
| CZ CELLxGENE | Single-cell datasets + publications | Portal download |
| GTEx | Tissue expression data + donors | Manual download |
| CellMarker | Cell marker publications (validation) | Portal download |

### 2.2 Data Description, Quality and Coverage — *@Jaswanth*

**Structure**: 22 tables — 16 entity + 6 junction tables linking publications to authors, organs, funders, institutions.

**Scale**: ~20.9M records. Largest: `hralit_publication_subject` (7.9M), `hralit_publication` (7.1M), `hralit_pub_funding_funder` (2.6M), `hralit_publication_author` (1.08M).

**Quality**: Author data limited to ORCID holders (~583K); institution/funder names cleaned via OpenAlex (partial coverage, both raw and cleaned provided); publications limited to PubMed-indexed papers; temporal range ~1898–Sep 2023.

**Coverage**: All 31 HRA organs represented with significant variation — brain, kidney, and heart dominate in publication and dataset counts. Country information available via `hralit_institution` (country_code) and `hralit_funder_cleaned` (country_code), enabling the USA–China cooperation analysis requested by the client.

---

## 3. DATA ANALYSIS

We will perform analyses in two phases — **retrospective** (past 20 years) followed by **predictive** (next 5 years), as directed by the client.

### Phase 1: Retrospective Analysis (2003–2023)
1. **Publication trend analysis**: Growth curves per organ over 20 years; doubling time; year-over-year breakdowns
2. **Funding landscape**: Aggregate grant-linkage frequency by organ, funder, and country; identify top funders; detect underfunded organs. *Note: HRAlit does not contain dollar amounts — all funding analyses measure frequency of grant mentions and funder–publication co-links, not monetary values.*
3. **USA–China cooperation analysis**: Count co-authored publications between US and Chinese institutions per year; compare to other bilateral pairs (US–UK, US–Germany). We define an **international collaboration** as a publication with authors affiliated with institutions from at least two different countries. *Data limitations: author coverage is restricted to ORCID holders (~583K of potentially millions); publications are PubMed-only (excluding conference papers and non-English journals); authors with multiple institutional affiliations may appear in more than one country.*
4. **Co-authorship network analysis**: Build organ-specific networks; identify key hub nodes (most connected authors); compute centrality metrics; analyze how networks evolve across 5-year windows (2003–2007, 2008–2012, 2013–2017, 2018–2023)
5. **University–funder relationship analysis**: Cross-tabulate institutions with funders; identify which funders most frequently support research at specific institutions
6. **Top 5 funders by country cooperation**: For each major country, rank funders by frequency of appearing in co-funded international publications
7. **Dataset & donor analysis**: Dataset counts by organ, source, assay type; donor demographics

### Phase 2: Predictive Analysis (2024–2028)
8. **Trend forecasting**: Use time-series methods (ARIMA, Facebook Prophet, or exponential smoothing) to project publication counts and funding involvement per organ for the next 5 years with confidence intervals
9. **Author growth prediction**: Forecast the number of active authors per organ based on historical growth patterns
10. **ML-based pattern recognition** *(recommended by client)*: Train a regression or classification model to identify which organ–funder–country combinations are most likely to see growth, based on historical feature patterns

### LLM Usage
We will use Large Language Models to assist with: exploratory SQL query generation over the 20.9M-record database; summarizing publication titles for topic clustering; generating natural-language insights from analytical results; and accelerating literature review for related work.

---

## 4. VISUALIZATIONS

We propose **8 visualizations** directly aligned with the client's requirements — **5 committed** deliverables and **3 stretch goals**. Each targets specific stakeholder needs and analysis goals. Numbering follows earlier visualization IDs; committed vs. stretch priority is defined by grouping, not numeric order.

### Committed Visualizations

#### 4.1 Interactive Organ Dashboard (Landing Page)
- **Type**: Multi-panel dashboard with organ selector
- **Stakeholders**: All groups
- **Description**: Selecting an organ shows KPI cards (publications, experts, datasets, funding projects) with sparklines. Serves as the entry point to all other views.

#### 4.2 Publication & Funding Trend Lines with 5-Year Prediction
- **Type**: Line chart with forecasting band
- **Stakeholders**: Funding Agencies, Policy Makers, HRA Team
- **Description**: Past 20 years of publication and funding counts per organ as solid lines, plus dashed forecast lines for 2024–2028 with shaded 95% confidence intervals. Users can toggle between organs. Generated using ARIMA/Prophet models.

#### 4.3 USA–China Collaboration Over Time
- **Type**: Grouped bar chart + trend line
- **Stakeholders**: Policy Makers, Funding Agencies
- **Description**: Year-by-year count of co-authored publications between US and Chinese institutions, with comparison lines for US–UK and US–Germany. Shows how international cooperation has evolved and where it's heading.

#### 4.4 Temporal Co-authorship Network (Key Nodes)
- **Type**: Force-directed network with time slider
- **Stakeholders**: Researchers, HRA Team
- **Description**: Interactive network graph showing co-authorship clusters for a selected organ. A **time slider** divides data into 5-year windows (2003–2007, 2008–2012, 2013–2017, 2018–2023) to visualize how collaboration patterns and key hub nodes change over time. Node size = publication count; color = institution/country. To maintain readability and performance, networks are limited to the **top 200–500 authors per organ** (ranked by publication count).

#### 4.6 Top Funders by Country Cooperation
- **Type**: Grouped horizontal bar chart / heatmap
- **Stakeholders**: Funding Agencies, Policy Makers
- **Description**: For each major country (USA, China, UK, Germany, Japan), shows the top 5 funders whose grants most frequently appear in internationally co-authored publications. Reveals which funders drive cross-border collaboration.

### Stretch Goals

#### 4.5 Grant-Linkage Sankey — Funder → Organ → Outputs
- **Type**: Sankey / alluvial diagram
- **Stakeholders**: Funding Agencies, Policy Makers
- **Description**: Traces grant-linkage frequency from funder → organ → research outcomes (publications, datasets). Band width represents the number of co-linked publications, not dollar amounts. Shows which funders are most frequently associated with which organs and output types.

#### 4.7 Geo Map — Global Expertise & Funding Distribution
- **Type**: Choropleth + proportional symbol map
- **Stakeholders**: Policy Makers, Researchers
- **Description**: World map showing institution locations (sized by author count) and funder origins. Filterable by organ. Highlights geographic concentrations and gaps, with special emphasis on the USA–China research axis.

#### 4.8 University–Funder Relationship Heatmap
- **Type**: Matrix heatmap
- **Stakeholders**: Funding Agencies, Researchers
- **Description**: Rows = top institutions, columns = top funders. Cell intensity = number of co-linked publications. Reveals which university–funder pairings are strongest and where new partnerships could form.

---

## 5. USAGE AND CRITIQUE OF AI TOOLS

### LLM Usage
- **Data exploration**: Using LLMs to generate and iterate on SQL queries across 22 tables with 20.9M records, significantly accelerating exploratory analysis
- **Topic clustering**: Applying LLMs to summarize/cluster publication titles by research theme within organs
- **Insight generation**: Producing natural-language summaries of analytical findings for stakeholder reports
- **Code assistance**: Accelerating D3.js/Python visualization development

### ML Models (Recommended by Client)
- **Time-series forecasting**: ARIMA or Prophet models for 5-year publication/funding predictions
- **Pattern recognition**: Regression models to identify organ–funder–country combinations likely to grow

### Critique
- LLMs may hallucinate domain-specific biomedical terminology or misinterpret ontology IRIs
- ML predictions are bounded by the assumption that historical trends continue; external shocks (pandemics, policy changes) cannot be forecasted
- Author deduplication across ORCID-based and non-ORCID records remains a limitation

---

## 6. INTERPRETATION OF RESULTS

*(To be completed after analyses are run.)*

Results will be interpreted in terms of the five research questions and six stakeholder groups. Key deliverables will include:
- Identification of underfunded organs with strong publication momentum (opportunities)
- Expert recommendations for new HRA digital object authors/reviewers
- Forecast of which organs will see the most research growth by 2028
- Assessment of USA–China collaboration trajectory and its implications for HRA
- Ranked list of top funders for international cooperation by country

---

## ACKNOWLEDGEMENTS

We thank Yongxin (Kiki) Kong (Project Sponsor) and Prof. Katy Börner for providing the HRAlit dataset and guidance.

## REFERENCES

1. Kong, Y., Börner, K. Publication, funding, and experimental data in support of Human Reference Atlas construction and usage. *Sci Data* **11**, 574 (2024). https://doi.org/10.1038/s41597-024-03416-8
2. Börner, K. *Atlas of Knowledge: Anyone Can Map.* MIT Press, 2015.
3. Börner, K., Bueckle, A., Ginda, M. "Data visualization literacy." *PNAS*, 116(6): 1857–1864, 2018.
4. Börner, K., et al. "Anatomical structures, cell types and biomarkers of the HRA." *Nat Cell Biol* 23, 1117–1128 (2021).
5. Börner, K., et al. "HuBMAP: 3D Human Reference Atlas construction and usage." *Nat Methods* (2024).
6. van Eck, N.J., Waltman, L. "VOSviewer, a computer program for bibliometric mapping." *Scientometrics* 84, 523–538 (2010).
7. Chen, C. "CiteSpace II: Detecting and Visualizing Emerging Trends." *JASIST* 57(3), 359–377 (2006).
8. NIH World RePORTER. https://worldreport.nih.gov

---

## SECTION 1.1 — STAKEHOLDER GROUPS (Tejas's Submission-Ready Version)

> The polished stakeholder groups content above in Section 1.1 is **ready for direct inclusion** in the report. It identifies 6 groups with role descriptions, interaction patterns, example questions, and a summary table — all grounded in actual HRAlit table names and client meeting requirements (especially USA–China cooperation and prediction needs for Policy Makers and Funding Agencies).
