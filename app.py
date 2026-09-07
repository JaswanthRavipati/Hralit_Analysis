"""
HRAlit Interactive Dashboard
Streamlit web app hosting 4 interactive visualizations from the HRAlit database.
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="HRAlit Interactive Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CUSTOM CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp { background-color: #0a1628; }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b3a4b 50%, #00647d 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #2d4059;
    }
    .main-header h1 {
        color: #e0e0e0;
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
    }
    .main-header p {
        color: #7a8c9e;
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0d1b2a;
        border-radius: 8px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1b2838;
        border-radius: 6px;
        color: #7a8c9e;
        padding: 8px 20px;
        border: 1px solid #2d4059;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2d4059;
        color: #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00647d !important;
        color: white !important;
        border-color: #00b4d8 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0d1b2a;
        border-right: 1px solid #2d4059;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #00b4d8;
        font-size: 1.1rem;
        border-bottom: 1px solid #2d4059;
        padding-bottom: 0.5rem;
    }
    
    /* Stat cards */
    .stat-card {
        background: linear-gradient(135deg, #1b2838, #1b3a4b);
        border: 1px solid #2d4059;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .stat-card h3 { color: #00b4d8; margin: 0; font-size: 1.8rem; }
    .stat-card p { color: #7a8c9e; margin: 0; font-size: 0.85rem; }
    
    /* Hide streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Make widget labels white */
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stCheckbox label, .stRadio label {
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA LOADING (cached)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATA = '/Users/tejassarma/Downloads/Client_Project/Client_Project_Info_Viz_Dataset'

@st.cache_data(show_spinner="Loading HRAlit data (~30s first time)...")
def load_all_data():
    """Load and process all HRAlit tables. Cached after first run."""
    # Core tables
    pub = pd.read_csv(f'{DATA}/hralit_publication.csv.gz', compression='gzip', usecols=['pmid', 'pubyear'])
    pub = pub.dropna(subset=['pubyear'])
    pub['pubyear'] = pub['pubyear'].astype(int)
    
    pub_organ = pd.read_csv(f'{DATA}/hralit_publication_subject.csv.gz', compression='gzip')
    pff = pd.read_csv(f'{DATA}/hralit_pub_funding_funder.csv.gz', compression='gzip',
                      usecols=['pmid', 'funder_name_pubmed'])
    pa = pd.read_csv(f'{DATA}/hralit_publication_author.csv.gz', compression='gzip',
                     usecols=['pmid', 'author_id'])
    ai = pd.read_csv(f'{DATA}/hralit_author_institution.csv.gz', compression='gzip',
                     usecols=['author_id', 'soa_institution_id'])
    inst = pd.read_csv(f'{DATA}/hralit_institution.csv',
                       usecols=['soa_institution_id', 'institution_name', 'country_code'])
    datasets = pd.read_csv(f'{DATA}/hralit_dataset.csv', usecols=['dataset_id', 'organ'])
    
    # --- FUNDER GROUPING ---
    funder_groups = {}
    for n in ['NHLBI NIH HHS', 'NCI NIH HHS', 'NIDDK NIH HHS', 'NINDS NIH HHS',
              'NIGMS NIH HHS', 'NICHD NIH HHS', 'NIA NIH HHS', 'NIAID NIH HHS',
              'NIMH NIH HHS', 'NEI NIH HHS', 'NCRR NIH HHS', 'NIEHS NIH HHS',
              'NIBIB NIH HHS', 'Intramural NIH HHS']:
        funder_groups[n] = 'NIH'
    funder_groups.update({
        'Medical Research Council': 'MRC', 'Wellcome Trust': 'Wellcome',
        'Deutsche Forschungsgemeinschaft': 'DFG', 'Howard Hughes Medical Institute': 'HHMI',
        'Canadian Institutes of Health Research': 'CIHR', 'British Heart Foundation': 'BHF',
    })
    for n in pff[pff['funder_name_pubmed'].str.contains('National Natural Science Foundation of China', case=False, na=False)]['funder_name_pubmed'].unique():
        funder_groups[n] = 'NSFC'
    for n in pff[pff['funder_name_pubmed'].str.contains('Japan Society|JSPS', case=False, na=False)]['funder_name_pubmed'].unique():
        funder_groups[n] = 'JSPS'
    for n in pff[pff['funder_name_pubmed'].str.contains('^NSF$|National Science Foundation', case=False, na=False)]['funder_name_pubmed'].unique():
        funder_groups[n] = 'NSF'
    
    pff['funder_clean'] = pff['funder_name_pubmed'].map(funder_groups)
    pff_clean = pff.dropna(subset=['funder_clean'])
    
    # --- JOINS ---
    # For trends: pub + organ + year
    pub_organ_year = pub_organ.merge(pub, on='pmid', how='inner')
    pub_organ_year = pub_organ_year[pub_organ_year['pubyear'] >= 1950]
    
    # For sankey: funder + organ + year
    pff_with_year = pff_clean.merge(pub[['pmid', 'pubyear']], on='pmid', how='inner')
    funder_organ = pff_with_year.merge(pub_organ, on='pmid', how='inner')
    
    # For heatmap: pub + author + institution + country + funder
    pa_inst = pa.merge(ai, on='author_id', how='inner')
    pa_inst = pa_inst.merge(inst, on='soa_institution_id', how='inner')
    pub_inst = pa_inst[['pmid', 'institution_name', 'country_code']].drop_duplicates()
    pub_2000 = pub[pub['pubyear'] >= 2000]
    pub_inst = pub_inst.merge(pub_2000[['pmid', 'pubyear']], on='pmid', how='inner')
    pub_fund = pff_clean[['pmid', 'funder_clean']].drop_duplicates()
    inst_funder = pub_inst.merge(pub_fund, on='pmid', how='inner')
    
    # For geo: pub + author + institution + country + year
    merged_geo = pa.merge(ai, on='author_id', how='inner')
    merged_geo = merged_geo.merge(inst[['soa_institution_id', 'country_code']], on='soa_institution_id', how='inner')
    merged_geo = merged_geo.merge(pub[['pmid', 'pubyear']], on='pmid', how='inner')
    merged_organ_geo = merged_geo.merge(pub_organ, on='pmid', how='inner')
    
    # Funding pmids for geo
    funding_pmids = pff.groupby('pmid')['funder_name_pubmed'].nunique().reset_index()
    funding_pmids.columns = ['pmid', 'n_funders']
    
    # Sorted lists
    all_organs_trends = pub_organ_year.groupby('organ')['pmid'].nunique().sort_values(ascending=False).index.tolist()
    all_funders = funder_organ.groupby('funder_clean')['pmid'].nunique().sort_values(ascending=False).index.tolist()
    all_organs_sankey = funder_organ.groupby('organ')['pmid'].nunique().sort_values(ascending=False).index.tolist()
    all_countries = inst_funder.groupby('country_code')['pmid'].nunique().sort_values(ascending=False).index.tolist()
    all_funders_heat = inst_funder.groupby('funder_clean')['pmid'].nunique().sort_values(ascending=False).index.tolist()
    all_organs_geo = merged_organ_geo.groupby('organ')['pmid'].nunique().sort_values(ascending=False).index.tolist()
    
    # Precompute trends
    organ_yearly = {}
    year_range = range(1950, 2022)
    for organ in all_organs_trends:
        yearly = pub_organ_year[pub_organ_year['organ'] == organ].groupby('pubyear')['pmid'].nunique()
        organ_yearly[organ] = {y: yearly.get(y, 0) for y in year_range}
    
    # Dataset counts
    ds_by_organ = datasets.groupby('organ').size().reset_index(name='dataset_count')
    ds_by_organ['organ_clean'] = ds_by_organ['organ'].str.replace(r'\s*\(.*\)', '', regex=True).str.strip().str.lower()
    
    # Load world map
    try:
        world = None
        import geopandas as gpd
        shp_path = f'{DATA}/ne_countries/ne_110m_admin_0_countries.shp'
        import os
        if os.path.exists(shp_path):
            world = gpd.read_file(shp_path)
    except Exception:
        world = None
    
    return {
        'pub_organ_year': pub_organ_year,
        'funder_organ': funder_organ,
        'inst_funder': inst_funder,
        'merged_geo': merged_geo,
        'merged_organ_geo': merged_organ_geo,
        'funding_pmids': funding_pmids,
        'ds_by_organ': ds_by_organ,
        'world': world,
        'organ_yearly': organ_yearly,
        'all_organs_trends': all_organs_trends,
        'all_funders': all_funders,
        'all_organs_sankey': all_organs_sankey,
        'all_countries': all_countries,
        'all_funders_heat': all_funders_heat,
        'all_organs_geo': all_organs_geo,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONSTANTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DARK_BG = '#0d1b2a'
FUNDER_COLORS = {
    'NIH': '#ff6b6b', 'Wellcome': '#6bcb77', 'MRC': '#4ecdc4',
    'DFG': '#ffd93d', 'HHMI': '#a78bfa', 'CIHR': '#f97316',
    'BHF': '#ec4899', 'NSFC': '#facc15', 'JSPS': '#22d3ee', 'NSF': '#818cf8',
    'MRC (UK)': '#4ecdc4', 'Wellcome Trust': '#6bcb77',
}
ORGAN_COLORS = {
    'brain': '#60a5fa', 'heart': '#ef4444', 'kidney': '#34d399',
    'liver': '#f59e0b', 'lung': '#8b5cf6', 'eye': '#06b6d4',
    'skin': '#fb923c', 'large intestine': '#a3e635',
    'pancreas': '#22d3ee', 'bone marrow': '#e879f9',
}
COUNTRY_NAMES = {
    'US': 'United States', 'CN': 'China', 'GB': 'United Kingdom',
    'JP': 'Japan', 'DE': 'Germany', 'IT': 'Italy', 'KR': 'South Korea',
    'AU': 'Australia', 'CA': 'Canada', 'FR': 'France', 'ES': 'Spain',
    'NL': 'Netherlands', 'IN': 'India', 'BR': 'Brazil', 'CH': 'Switzerland',
    'SE': 'Sweden', 'DK': 'Denmark', 'BE': 'Belgium',
}
COUNTRY_POS = {
    'US': (-98, 39), 'CN': (104, 35), 'GB': (-1, 53), 'JP': (138, 36),
    'DE': (10, 51), 'IT': (12, 42), 'KR': (128, 36), 'AU': (134, -25),
    'CA': (-106, 56), 'FR': (2, 47), 'ES': (-4, 40), 'NL': (5, 52),
    'IN': (79, 22), 'BR': (-51, -10), 'CH': (8, 47), 'SE': (15, 62),
    'DK': (10, 56), 'BE': (4, 51), 'AT': (14, 47), 'NO': (9, 62),
    'FI': (26, 64), 'IL': (35, 31), 'SG': (104, 1), 'TW': (121, 24),
    'HK': (114, 22), 'MX': (-102, 23), 'RU': (37, 55), 'TR': (35, 39),
    'PL': (20, 52), 'GR': (22, 39), 'PT': (-8, 39), 'IE': (-8, 53),
    'ZA': (25, -29), 'NZ': (172, -42),
}

MPL_STYLE = {
    'figure.facecolor': DARK_BG, 'axes.facecolor': DARK_BG,
    'axes.edgecolor': '#2d4059', 'text.color': '#e0e0e0',
    'xtick.color': '#7a8c9e', 'ytick.color': '#7a8c9e',
    'grid.color': '#1b3a4b', 'grid.alpha': 0.3,
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: SANKEY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_sankey(data):
    st.sidebar.markdown("### 🔗 Sankey Filters")
    
    sel_funders = st.sidebar.multiselect(
        "Funders", data['all_funders'], default=data['all_funders'][:6],
        key='sankey_funders'
    )
    sel_organs = st.sidebar.multiselect(
        "Organs", data['all_organs_sankey'], default=data['all_organs_sankey'][:6],
        key='sankey_organs'
    )
    yr = st.sidebar.slider("Year Range", 1950, 2021, (2000, 2021), key='sankey_yr')
    
    if not sel_funders or not sel_organs:
        st.warning("Select at least one funder and one organ.")
        return
    
    funder_organ = data['funder_organ']
    ds_by_organ = data['ds_by_organ']
    
    mask = (funder_organ['funder_clean'].isin(sel_funders)) & \
           (funder_organ['organ'].isin(sel_organs)) & \
           (funder_organ['pubyear'] >= yr[0]) & \
           (funder_organ['pubyear'] <= yr[1])
    filtered = funder_organ[mask]
    
    if len(filtered) == 0:
        st.warning("No data for selected filters.")
        return
    
    flow_fo = filtered.groupby(['funder_clean', 'organ'])['pmid'].nunique().reset_index()
    flow_fo.columns = ['funder', 'organ', 'pub_count']
    funder_totals = flow_fo.groupby('funder')['pub_count'].sum().sort_values(ascending=False)
    organ_totals = flow_fo.groupby('organ')['pub_count'].sum().sort_values(ascending=False)
    funders_sorted = funder_totals.index.tolist()
    organs_sorted = organ_totals.index.tolist()
    
    organ_outputs = []
    for organ in organs_sorted:
        pub_c = organ_totals.get(organ, 0)
        ds_match = ds_by_organ[ds_by_organ['organ_clean'].str.contains(organ.split()[0], case=False, na=False)]
        ds_c = ds_match['dataset_count'].sum() if len(ds_match) > 0 else 0
        organ_outputs.append({'organ': organ, 'Publications': pub_c, 'Datasets': max(ds_c, 1)})
    flow_oo = pd.DataFrame(organ_outputs)
    output_totals = {'Publications': flow_oo['Publications'].sum(), 'Datasets': flow_oo['Datasets'].sum()}
    total_output = sum(output_totals.values())
    
    plt.rcParams.update(MPL_STYLE)
    fig, ax = plt.subplots(1, 1, figsize=(16, max(8, len(organs_sorted) * 0.8)))
    
    x_f, x_o, x_out = 0.08, 0.45, 0.82
    col_w = 0.04
    gap = 0.015
    total_flow = funder_totals.sum()
    
    def compute_positions(sorted_items, totals, total_sum):
        heights, positions = {}, {}
        y = 0.95
        for item in sorted_items:
            h = max((totals[item] / total_sum) * 0.75, 0.02)
            heights[item] = h
            positions[item] = y
            y -= h + gap
        return heights, positions
    
    f_h, f_y = compute_positions(funders_sorted, funder_totals, total_flow)
    o_h, o_y = compute_positions(organs_sorted, organ_totals, total_flow)
    
    out_h, out_y = {}, {}
    y = 0.80
    for name in ['Publications', 'Datasets']:
        h = max((output_totals[name] / total_output) * 0.5, 0.04)
        out_h[name] = h
        out_y[name] = y
        y -= h + gap * 3
    
    # Draw bars
    for f in funders_sorted:
        color = FUNDER_COLORS.get(f, '#888')
        rect = plt.Rectangle((x_f, f_y[f] - f_h[f]), col_w, f_h[f], facecolor=color, alpha=0.9,
                              edgecolor='white', linewidth=0.5, transform=ax.transAxes, zorder=5)
        ax.add_patch(rect)
        ax.text(x_f - 0.01, f_y[f] - f_h[f]/2, f, transform=ax.transAxes, fontsize=8,
                ha='right', va='center', color='white', fontweight='bold',
                path_effects=[pe.withStroke(linewidth=1, foreground='black')])
    
    for o in organs_sorted:
        color = ORGAN_COLORS.get(o, '#888')
        rect = plt.Rectangle((x_o, o_y[o] - o_h[o]), col_w, o_h[o], facecolor=color, alpha=0.9,
                              edgecolor='white', linewidth=0.5, transform=ax.transAxes, zorder=5)
        ax.add_patch(rect)
        ax.text(x_o + col_w/2, o_y[o] - o_h[o]/2, o.title(), transform=ax.transAxes, fontsize=7,
                ha='center', va='center', color='white', fontweight='bold',
                path_effects=[pe.withStroke(linewidth=2, foreground='black')])
    
    for name in ['Publications', 'Datasets']:
        color = '#00b4d8' if name == 'Publications' else '#e9c46a'
        rect = plt.Rectangle((x_out, out_y[name] - out_h[name]), col_w, out_h[name], facecolor=color, alpha=0.9,
                              edgecolor='white', linewidth=0.5, transform=ax.transAxes, zorder=5)
        ax.add_patch(rect)
        ax.text(x_out + col_w + 0.01, out_y[name] - out_h[name]/2, f'{name}\n({output_totals[name]:,})',
                transform=ax.transAxes, fontsize=9, ha='left', va='center', color='white', fontweight='bold')
    
    # Draw flows: Funder → Organ
    f_cursor = {f: f_y[f] for f in funders_sorted}
    o_cursor_l = {o: o_y[o] for o in organs_sorted}
    for _, row in flow_fo.sort_values('pub_count', ascending=False).iterrows():
        f, o, count = row['funder'], row['organ'], row['pub_count']
        if f not in f_h or o not in o_h:
            continue
        bh_f = (count / funder_totals[f]) * f_h[f]
        bh_o = (count / organ_totals[o]) * o_h[o]
        y1t, y2t = f_cursor[f], o_cursor_l[o]
        y1b, y2b = y1t - bh_f, y2t - bh_o
        f_cursor[f] = y1b
        o_cursor_l[o] = y2b
        color = FUNDER_COLORS.get(f, '#888')
        t = np.linspace(0, 1, 50)
        x_pts = (x_f + col_w) + t * (x_o - x_f - col_w)
        y_top = y1t + t**2 * (3 - 2*t) * (y2t - y1t)
        y_bot = y1b + t**2 * (3 - 2*t) * (y2b - y1b)
        ax.fill_between(x_pts, y_bot, y_top, alpha=0.2, color=color, transform=ax.transAxes, zorder=2)
    
    # Draw flows: Organ → Output
    o_cursor_r = {o: o_y[o] for o in organs_sorted}
    out_cursor = {n: out_y[n] for n in ['Publications', 'Datasets']}
    for _, row in flow_oo.iterrows():
        o = row['organ']
        if o not in o_h:
            continue
        color = ORGAN_COLORS.get(o, '#888')
        ot = organ_totals.get(o, 1)
        for name in ['Publications', 'Datasets']:
            count = row[name]
            if count <= 0:
                continue
            bh_o = (count / ot) * o_h[o]
            bh_out = (count / output_totals[name]) * out_h[name]
            y1t, y2t = o_cursor_r[o], out_cursor[name]
            y1b, y2b = y1t - bh_o, y2t - bh_out
            o_cursor_r[o] = y1b
            out_cursor[name] = y2b
            t = np.linspace(0, 1, 50)
            x_pts = (x_o + col_w) + t * (x_out - x_o - col_w)
            y_top = y1t + t**2 * (3 - 2*t) * (y2t - y1t)
            y_bot = y1b + t**2 * (3 - 2*t) * (y2b - y1b)
            ax.fill_between(x_pts, y_bot, y_top, alpha=0.15, color=color, transform=ax.transAxes, zorder=2)
    
    ax.text(x_f + col_w/2, 0.99, 'FUNDERS', transform=ax.transAxes, fontsize=11, ha='center', fontweight='bold', color='#00b4d8')
    ax.text(x_o + col_w/2, 0.99, 'ORGANS', transform=ax.transAxes, fontsize=11, ha='center', fontweight='bold', color='#00b4d8')
    ax.text(x_out + col_w/2, 0.99, 'OUTPUTS', transform=ax.transAxes, fontsize=11, ha='center', fontweight='bold', color='#00b4d8')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    fig.suptitle(f'Grant-Linkage Sankey ({yr[0]}–{yr[1]})', fontsize=15, fontweight='bold', color='white', y=0.99)
    
    st.pyplot(fig)
    plt.close(fig)
    
    # Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Funded Publications", f"{int(filtered['pmid'].nunique()):,}")
    c2.metric("Funders", len(funders_sorted))
    c3.metric("Organs", len(organs_sorted))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: TRENDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_trends(data):
    st.sidebar.markdown("### 📈 Trend Filters")
    
    presets = st.sidebar.radio("Quick Select", ["Top 5", "Top 10", "All", "Custom"],
                               key='trend_preset', horizontal=True)
    
    all_organs = data['all_organs_trends']
    if presets == "Top 5":
        default_organs = all_organs[:5]
    elif presets == "Top 10":
        default_organs = all_organs[:10]
    elif presets == "All":
        default_organs = all_organs
    else:
        default_organs = all_organs[:5]
    
    sel_organs = st.sidebar.multiselect(
        "Selected Organs", all_organs, default=default_organs, key='trend_organs'
    )
    
    yr = st.sidebar.slider("Year Range", 1950, 2021, (1950, 2021), key='trend_yr')
    show_forecast = st.sidebar.checkbox("Show Forecast", value=True, key='trend_fc')
    forecast_yrs = st.sidebar.slider("Forecast Years", 1, 10, 5, key='trend_fc_yr') if show_forecast else 0
    
    if not sel_organs:
        st.warning("Select at least one organ.")
        return
    
    organ_yearly = data['organ_yearly']
    
    plt.rcParams.update(MPL_STYLE)
    fig, ax = plt.subplots(1, 1, figsize=(14, 7))
    
    yr_range = range(max(yr[0], 1950), min(yr[1] + 1, 2022))
    forecast_range = range(yr[1] + 1, yr[1] + 1 + forecast_yrs) if show_forecast else []
    
    cmap_tab = plt.cm.get_cmap('tab20', len(all_organs))
    
    for organ in sel_organs:
        if organ not in organ_yearly:
            continue
        color = ORGAN_COLORS.get(organ, cmap_tab(all_organs.index(organ) if organ in all_organs else 0))
        
        years = list(yr_range)
        counts = [organ_yearly[organ].get(y, 0) for y in yr_range]
        ax.plot(years, counts, '-', color=color, linewidth=2.5, label=organ.title(),
                path_effects=[pe.withStroke(linewidth=4, foreground=DARK_BG)])
        
        if show_forecast and len(forecast_range) > 0:
            train_start = max(yr[0], yr[1] - 19)
            train_years = list(range(train_start, yr[1] + 1))
            train_counts = [organ_yearly[organ].get(y, 0) for y in train_years]
            
            X = np.array(train_years).reshape(-1, 1)
            y_arr = np.array(train_counts)
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y_arr)
            
            X_fut = np.array(list(forecast_range)).reshape(-1, 1)
            y_pred = np.maximum(model.predict(poly.transform(X_fut)), 0)
            residuals = y_arr - model.predict(X_poly)
            ci = 1.96 * np.std(residuals) * np.linspace(1, 2.5, len(forecast_range))
            
            ax.plot([years[-1], list(forecast_range)[0]], [counts[-1], y_pred[0]], '--', color=color, linewidth=1.5, alpha=0.7)
            ax.plot(list(forecast_range), y_pred, '--', color=color, linewidth=1.5, alpha=0.8)
            ax.fill_between(list(forecast_range), np.maximum(y_pred - ci, 0), y_pred + ci, color=color, alpha=0.12)
    
    if show_forecast:
        ax.axvline(x=yr[1] + 0.5, color='#7a8c9e', linewidth=1.5, linestyle=':', alpha=0.7)
        ax.text(yr[1] + 0.5, ax.get_ylim()[1] * 0.95, '  Today', fontsize=10, color='#7a8c9e', fontstyle='italic', va='top')
    
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Publication Count', fontsize=12, fontweight='bold')
    ax.set_ylim(bottom=0)
    ax.grid(True)
    
    n_organs = len(sel_organs)
    ncol = 2 if n_organs > 8 else 1
    ax.legend(loc='upper left', fontsize=8 if n_organs > 8 else 9, framealpha=0.3,
              edgecolor='#2d4059', facecolor=DARK_BG, labelcolor='#e0e0e0', ncol=ncol)
    
    title = f'Publication Trends: {", ".join(o.title() for o in sel_organs[:3])}'
    if n_organs > 3:
        title += f' + {n_organs - 3} more'
    fig.suptitle(title, fontsize=15, fontweight='bold', color='white', y=0.98)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: HEATMAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_heatmap(data):
    st.sidebar.markdown("### 🗺️ Heatmap Filters")
    
    all_countries = data['all_countries']
    country_options = {f"{COUNTRY_NAMES.get(cc, cc)} ({cc})": cc for cc in all_countries[:20]}
    
    sel_country_label = st.sidebar.selectbox("Country", list(country_options.keys()), key='heat_country')
    sel_country = country_options[sel_country_label]
    
    n_inst = st.sidebar.slider("Top N Institutions", 3, 20, 10, key='heat_n')
    yr = st.sidebar.slider("Year Range", 2000, 2021, (2000, 2021), key='heat_yr')
    
    sel_funders = st.sidebar.multiselect(
        "Funders", data['all_funders_heat'], default=data['all_funders_heat'], key='heat_funders'
    )
    
    inst_funder = data['inst_funder']
    
    mask = (inst_funder['country_code'] == sel_country) & \
           (inst_funder['pubyear'] >= yr[0]) & \
           (inst_funder['pubyear'] <= yr[1])
    if sel_funders:
        mask = mask & (inst_funder['funder_clean'].isin(sel_funders))
    
    filtered = inst_funder[mask]
    
    if len(filtered) == 0:
        st.warning(f"No data for {COUNTRY_NAMES.get(sel_country, sel_country)} in {yr[0]}–{yr[1]}")
        return
    
    top_insts = filtered.groupby('institution_name')['pmid'].nunique().sort_values(ascending=False).head(n_inst).index.tolist()
    avail_funders = sel_funders if sel_funders else filtered.groupby('funder_clean')['pmid'].nunique().sort_values(ascending=False).index.tolist()
    
    mat = filtered[filtered['institution_name'].isin(top_insts)].groupby(
        ['institution_name', 'funder_clean'])['pmid'].nunique().unstack(fill_value=0)
    mat = mat.reindex(index=top_insts, columns=avail_funders).fillna(0)
    mat = mat.loc[:, mat.sum() > 0]
    
    if mat.empty:
        st.warning("No co-linked publications found")
        return
    
    plt.rcParams.update(MPL_STYLE)
    fig, ax = plt.subplots(1, 1, figsize=(max(10, len(mat.columns) * 1.5), max(6, len(mat) * 0.7)))
    
    cmap = LinearSegmentedColormap.from_list('custom',
        [DARK_BG, '#1b3a4b', '#00647d', '#00b4d8', '#48cae4', '#e9c46a', '#f4a261', '#e76f51'], N=256)
    
    d = mat.values.astype(float)
    im = ax.imshow(d, cmap=cmap, aspect='auto', interpolation='nearest', vmin=0, vmax=max(d.max(), 1))
    
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            val = int(d[i, j])
            if val > 0:
                tc = 'black' if val > d.max() * 0.55 else 'white'
                ax.text(j, i, f'{val:,}', ha='center', va='center', fontsize=8, fontweight='bold', color=tc)
    
    short_names = [n[:35] + '...' if len(n) > 35 else n for n in mat.index]
    ax.set_yticks(range(len(short_names)))
    ax.set_yticklabels(short_names, fontsize=9)
    ax.set_xticks(range(len(mat.columns)))
    ax.set_xticklabels(mat.columns, fontsize=10, fontweight='bold', rotation=30, ha='right')
    
    for i in range(d.shape[0] + 1):
        ax.axhline(i - 0.5, color='#2d4059', linewidth=0.3)
    for j in range(d.shape[1] + 1):
        ax.axvline(j - 0.5, color='#2d4059', linewidth=0.3)
    
    cbar = plt.colorbar(im, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label('Co-linked Publications', fontsize=10, color='#e0e0e0')
    cbar.ax.tick_params(colors='#7a8c9e', labelsize=9)
    
    country_name = COUNTRY_NAMES.get(sel_country, sel_country)
    total_pubs = int(filtered['pmid'].nunique())
    ax.set_title(f'{country_name} — Top {len(mat)} Institutions × Funders ({yr[0]}–{yr[1]})\n'
                 f'{total_pubs:,} funded publications', fontsize=13, fontweight='bold', pad=15)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Funded Publications", f"{total_pubs:,}")
    c2.metric("Institutions Shown", len(mat))
    c3.metric("Active Funders", len(mat.columns))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4: GEO MAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_geo(data):
    st.sidebar.markdown("### 🌍 Map Filters")
    
    all_organs = data['all_organs_geo']
    sel_organ = st.sidebar.selectbox("Organ", ['All'] + all_organs, key='geo_organ')
    yr = st.sidebar.slider("Year Range", 1950, 2023, (2018, 2023), key='geo_yr')
    top_n_edges = st.sidebar.slider("Top N Collaboration Edges", 5, 100, 30, step=5, key='geo_edges')
    min_authors = st.sidebar.slider("Min Authors to Show", 1, 500, 50, step=10, key='geo_min')
    show_labels = st.sidebar.checkbox("Show Country Labels", value=True, key='geo_labels')
    
    # Quick periods
    st.sidebar.markdown("**Quick Periods:**")
    period_cols = st.sidebar.columns(3)
    periods = [('2003–07', 2003, 2007), ('2008–12', 2008, 2012), ('2013–17', 2013, 2017)]
    # We can't dynamically change sliders easily, so just note them
    
    merged_geo = data['merged_geo']
    merged_organ_geo = data['merged_organ_geo']
    funding_pmids = data['funding_pmids']
    world = data['world']
    
    # Filter data
    if sel_organ != 'All':
        df = merged_organ_geo[merged_organ_geo['organ'] == sel_organ]
    else:
        df = merged_geo
    
    df = df[(df['pubyear'] >= yr[0]) & (df['pubyear'] <= yr[1])]
    
    if len(df) == 0:
        st.warning(f"No data for {sel_organ} in {yr[0]}–{yr[1]}")
        return
    
    author_counts = df.groupby('country_code')['author_id'].nunique()
    
    pub_countries = df.groupby('pmid')['country_code'].apply(set)
    collab_pairs = Counter()
    intl_count = 0
    for countries in pub_countries:
        # Remove NaN values
        countries = {c for c in countries if isinstance(c, str)}
        if len(countries) > 1:
            intl_count += 1
            sorted_c = sorted(countries)
            for i in range(len(sorted_c)):
                for j in range(i + 1, len(sorted_c)):
                    collab_pairs[(sorted_c[i], sorted_c[j])] += 1
    
    fund_data = df.merge(funding_pmids, on='pmid', how='left')
    funding_by_country = fund_data.dropna(subset=['n_funders']).groupby('country_code')['n_funders'].mean()
    total_pubs = df['pmid'].nunique()
    
    plt.rcParams.update(MPL_STYLE)
    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    
    if world is not None:
        world.plot(ax=ax, color='#1b2838', edgecolor='#2d4059', linewidth=0.3)
    else:
        ax.set_facecolor('#0d1b2a')
    
    top_edges = sorted(collab_pairs.items(), key=lambda x: -x[1])[:top_n_edges]
    max_edge = top_edges[0][1] if top_edges else 1
    
    for (c1, c2), count in top_edges:
        if c1 not in COUNTRY_POS or c2 not in COUNTRY_POS:
            continue
        x1, y1 = COUNTRY_POS[c1]
        x2, y2 = COUNTRY_POS[c2]
        lw = 0.5 + (count / max_edge) * 4
        alpha = 0.2 + (count / max_edge) * 0.5
        ax.plot([x1, x2], [y1, y2], '-', color='#00b4d8', linewidth=lw, alpha=alpha, zorder=2)
    
    max_count = author_counts.max() if len(author_counts) > 0 else 1
    cmap_fund = LinearSegmentedColormap.from_list('fund', ['#34d399', '#f59e0b', '#ef4444'], N=256)
    max_fund = funding_by_country.max() if len(funding_by_country) > 0 else 1
    
    for cc, count in author_counts.items():
        if cc not in COUNTRY_POS or count < min_authors:
            continue
        x, y = COUNTRY_POS[cc]
        size = 30 + (count / max_count) * 600
        fund_val = funding_by_country.get(cc, 0)
        color = cmap_fund(fund_val / max_fund) if max_fund > 0 else '#34d399'
        ax.scatter(x, y, s=size, c=[color], alpha=0.85, edgecolors='white', linewidth=0.5, zorder=4)
        
        if show_labels and count >= max_count * 0.05:
            label = COUNTRY_NAMES.get(cc, cc)
            ax.text(x, y + 3, label, ha='center', va='bottom', fontsize=7, color='white',
                    fontweight='bold', path_effects=[pe.withStroke(linewidth=2, foreground=DARK_BG)], zorder=5)
    
    ax.set_xlim(-180, 180)
    ax.set_ylim(-60, 85)
    ax.set_xticks([]); ax.set_yticks([])
    
    organ_label = sel_organ.title() if sel_organ != 'All' else 'All Organs'
    ax.set_title(f'{organ_label} — {yr[0]}–{yr[1]}\n'
                 f'{total_pubs:,} publications  •  {intl_count:,} international collaborations  •  '
                 f'{len(author_counts)} countries',
                 fontsize=13, fontweight='bold', color='white', pad=12)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Publications", f"{total_pubs:,}")
    c2.metric("International Collaborations", f"{intl_count:,}")
    c3.metric("Countries", len(author_counts))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN APP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧬 HRAlit Interactive Dashboard</h1>
        <p>Exploring publication, funding, and collaboration patterns in the Human Reference Atlas literature database</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    data = load_all_data()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔗 Grant-Linkage Sankey",
        "📈 Publication Trends",
        "🗺️ Institution–Funder Heatmap",
        "🌍 Global Collaboration Map",
    ])
    
    with tab1:
        st.markdown("#### Funder → Organ → Output Flow")
        st.caption("Band width represents the number of co-linked publications. Use sidebar filters to explore.")
        render_sankey(data)
    
    with tab2:
        st.markdown("#### Publication Count Trends with Forecast")
        st.caption("Historical trends from 1950–2021 with polynomial regression forecast. 2022–2023 excluded (incomplete data).")
        render_trends(data)
    
    with tab3:
        st.markdown("#### Top Institutions × Funders by Country")
        st.caption("Cell values = co-linked publication count. Select a country to see its funding landscape.")
        render_heatmap(data)
    
    with tab4:
        st.markdown("#### International Co-Publication Network")
        st.caption("Bubble size = author count, color = funding intensity. Edges = international collaborations.")
        render_geo(data)
    
    # Footer
    st.markdown("---")
    st.caption("Data: HRAlit Database (Kong & Börner, 2024) • Built with Streamlit & Matplotlib")


if __name__ == '__main__':
    main()
