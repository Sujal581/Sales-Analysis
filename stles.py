import streamlit as st


def apply_futuristic_style():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

    :root {
        --neon-cyan:    #00f5ff;
        --neon-purple:  #bf00ff;
        --neon-blue:    #0066ff;
        --dark-bg:      #020714;
        --glass-bg:     rgba(0, 20, 50, 0.55);
        --glass-border: rgba(0, 245, 255, 0.18);
        --text-primary: #e0f4ff;
        --text-muted:   #4a7fa5;
        --glow-sm:      0 0 8px rgba(0,245,255,0.4);
        --glow-md:      0 0 20px rgba(0,245,255,0.25), 0 0 40px rgba(0,102,255,0.15);
        --glow-lg:      0 0 30px rgba(0,245,255,0.35), 0 0 60px rgba(191,0,255,0.20);
    }

    @keyframes grid-pan {
        0%   { background-position: 0 0, 0 0, center, center; }
        100% { background-position: 80px 80px, 80px 80px, center, center; }
    }
    @keyframes scan-line {
        0%   { transform: translateY(-100%); opacity: 0.07; }
        100% { transform: translateY(100vh);  opacity: 0.00; }
    }
    @keyframes pulse-border {
        0%,100% { border-color: rgba(0,245,255,0.30); box-shadow: 0 0 12px rgba(0,245,255,0.15); }
        50%      { border-color: rgba(0,245,255,0.70); box-shadow: 0 0 24px rgba(0,245,255,0.30); }
    }
    @keyframes flicker {
        0%,19%,21%,23%,25%,54%,56%,100% { opacity: 1; }
        20%,24%,55% { opacity: 0.55; }
    }
    @keyframes slide-in-up {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes holo-shift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes metric-glow {
        0%,100% { text-shadow: 0 0 8px var(--neon-cyan), 0 0 20px var(--neon-cyan); }
        50%      { text-shadow: 0 0 16px var(--neon-cyan), 0 0 40px var(--neon-blue), 0 0 70px rgba(0,245,255,0.3); }
    }
    @keyframes corner-pulse {
        0%,100% { opacity: 0.6; }
        50%      { opacity: 1; }
    }
    @keyframes row-flash {
        0%   { background: rgba(0,245,255,0.12); }
        100% { background: transparent; }
    }

    /* ── APP BACKGROUND ── */
    .stApp {
        background-color: var(--dark-bg) !important;
        background-image:
            linear-gradient(rgba(0,245,255,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,245,255,0.025) 1px, transparent 1px),
            radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,102,255,0.16) 0%, transparent 70%),
            radial-gradient(ellipse 50% 40% at 90% 80%, rgba(191,0,255,0.10) 0%, transparent 60%);
        background-size: 80px 80px, 80px 80px, 100% 100%, 100% 100%;
        animation: grid-pan 12s linear infinite;
        font-family: 'Rajdhani', sans-serif !important;
        color: var(--text-primary) !important;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 200px;
        background: linear-gradient(transparent, rgba(0,245,255,0.035), transparent);
        animation: scan-line 8s linear infinite;
        pointer-events: none;
        z-index: 9999;
    }

    /* ── LAYOUT ── */
    .block-container {
        padding-top: 0.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
        animation: slide-in-up 0.5s ease both;
    }

    /* ── HEADER ── */
    header[data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stToolbar"]      { right: 1rem; }
    .stAppHeader                   { background: rgba(0,0,0,0) !important; }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #030c1e 0%, #050e25 100%) !important;
        border-right: 1px solid rgba(0,245,255,0.14) !important;
        box-shadow: 4px 0 30px rgba(0,245,255,0.05) !important;
    }
    section[data-testid="stSidebar"]::before {
        content: '';
        display: block;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-purple), transparent);
        background-size: 200% 200%;
        animation: holo-shift 4s ease infinite;
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Rajdhani', sans-serif !important;
        color: #b0d8f0 !important;
    }
    section[data-testid="stSidebar"] h1 {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.05rem !important;
        color: var(--neon-cyan) !important;
        letter-spacing: 0.15em !important;
        text-shadow: var(--glow-sm) !important;
        text-transform: uppercase !important;
    }

    /* ── SELECTBOX ── */
    .stSelectbox > div > div {
        background: rgba(0, 12, 30, 0.85) !important;
        border: 1px solid rgba(0,245,255,0.22) !important;
        border-radius: 8px !important;
        color: var(--neon-cyan) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.88rem !important;
        backdrop-filter: blur(12px) !important;
        transition: border-color 0.3s, box-shadow 0.3s !important;
    }
    .stSelectbox > div > div:hover,
    .stSelectbox > div > div:focus-within {
        border-color: var(--neon-cyan) !important;
        box-shadow: var(--glow-sm) !important;
    }
    .stSelectbox label {
        color: var(--text-muted) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.07em !important;
        text-transform: uppercase !important;
    }

    /* ── DROPDOWN MENUS (scoped to selectbox / multiselect only) ──
       We intentionally avoid bare [data-baseweb="popover"] and
       [data-baseweb="menu"] so the dataframe column-header context
       menu is NOT affected and renders with its default Streamlit styles.
    ── */
    .stSelectbox   [data-baseweb="popover"],
    .stMultiSelect [data-baseweb="popover"],
    .stSelectbox   [data-baseweb="menu"],
    .stMultiSelect [data-baseweb="menu"],
    [data-baseweb="select"] [role="listbox"],
    [data-testid="stSelectboxVirtualDropdown"] {
        background: #030d1f !important;
        border: 1px solid rgba(0,245,255,0.25) !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6), var(--glow-sm) !important;
        backdrop-filter: blur(20px) !important;
    }
    .stSelectbox   [data-baseweb="popover"] *,
    .stMultiSelect [data-baseweb="popover"] *,
    .stSelectbox   [data-baseweb="menu"] *,
    .stMultiSelect [data-baseweb="menu"] *,
    [data-baseweb="select"] [role="listbox"] *,
    [data-testid="stSelectboxVirtualDropdown"] * {
        background: transparent !important;
        color: #a0cfff !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.85rem !important;
    }
    .stSelectbox   [data-baseweb="menu"] [role="option"]:hover,
    .stSelectbox   [data-baseweb="menu"] [aria-selected="true"],
    .stMultiSelect [data-baseweb="menu"] [role="option"]:hover,
    .stMultiSelect [data-baseweb="menu"] [aria-selected="true"],
    [data-baseweb="select"] [role="listbox"] [aria-selected="true"] {
        background: rgba(0,245,255,0.09) !important;
        color: var(--neon-cyan) !important;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background: transparent !important;
        border: 1px solid rgba(0,245,255,0.4) !important;
        border-radius: 6px !important;
        color: var(--neon-cyan) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        padding: 0.45rem 1.1rem !important;
        transition: all 0.25s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton > button:hover {
        background: rgba(0,245,255,0.07) !important;
        border-color: var(--neon-cyan) !important;
        box-shadow: var(--glow-md) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ══════════════════════════════════════════════
       KPI METRIC CARDS  — covers all Streamlit versions
    ══════════════════════════════════════════════ */

    [data-testid="stMetric"],
    div[data-testid="stMetric"],
    [data-testid="metric-container"],
    div[data-testid="metric-container"] {
        background: rgba(0, 12, 35, 0.82) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0,245,255,0.32) !important;
        border-radius: 16px !important;
        padding: 20px 20px 16px 20px !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 0 0 18px rgba(0,245,255,0.10),
                    inset 0 1px 0 rgba(0,245,255,0.08) !important;
        animation: slide-in-up 0.5s ease both,
                   pulse-border 4s ease-in-out infinite !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }

    [data-testid="stMetric"]::before,
    div[data-testid="stMetric"]::before,
    [data-testid="metric-container"]::before,
    div[data-testid="metric-container"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important; left: 0 !important;
        width: 28px !important; height: 28px !important;
        border-top: 2px solid var(--neon-cyan) !important;
        border-left: 2px solid var(--neon-cyan) !important;
        border-radius: 14px 0 0 0 !important;
        animation: corner-pulse 3s ease-in-out infinite !important;
        pointer-events: none !important;
    }

    [data-testid="stMetric"]::after,
    div[data-testid="stMetric"]::after,
    [data-testid="metric-container"]::after,
    div[data-testid="metric-container"]::after {
        content: '' !important;
        position: absolute !important;
        bottom: 0 !important; right: 0 !important;
        width: 28px !important; height: 28px !important;
        border-bottom: 2px solid var(--neon-purple) !important;
        border-right: 2px solid var(--neon-purple) !important;
        border-radius: 0 0 14px 0 !important;
        animation: corner-pulse 3s ease-in-out infinite reverse !important;
        pointer-events: none !important;
    }

    [data-testid="stMetric"]:hover,
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px) scale(1.015) !important;
        box-shadow: var(--glow-lg) !important;
        border-color: rgba(0,245,255,0.60) !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] > div,
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] span,
    [data-testid="metric-container"] label,
    [data-testid="stMetric"] label {
        color: #5a9fc0 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.62rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] > div,
    [data-testid="stMetricValue"] p {
        color: var(--neon-cyan) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.80rem !important;
        font-weight: 900 !important;
        letter-spacing: 0.03em !important;
        line-height: 1.15 !important;
        text-shadow: none !important;
        animation: none !important;
        overflow-wrap: anywhere !important;
        white-space: normal !important;
    }

    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] > div,
    [data-testid="stMetricDelta"] p {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.78rem !important;
        margin-top: 4px !important;
    }

    /* ── TYPOGRAPHY ── */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.75rem !important;
        font-weight: 900 !important;
        color: var(--neon-cyan) !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        text-shadow: 0 0 12px var(--neon-cyan), 0 0 30px rgba(0,245,255,0.30) !important;
        animation: flicker 8s linear infinite !important;
        border-bottom: 1px solid rgba(0,245,255,0.10) !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 1.4rem !important;
    }
    h2 {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #a0cfff !important;
        letter-spacing: 0.07em !important;
        text-transform: uppercase !important;
        text-shadow: 0 0 8px rgba(0,153,255,0.35) !important;
    }
    h3 {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #8ab4d8 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }
    p, span { font-family: 'Rajdhani', sans-serif; }
    .stMarkdown p {
        color: #a0cfff !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
    }

    /* ── PLOTLY CHART CONTAINERS ── */
    [data-testid="stPlotlyChart"] {
        background: rgba(3, 10, 25, 0.80) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(0,245,255,0.16) !important;
        border-radius: 16px !important;
        padding: 6px !important;
        transition: box-shadow 0.3s ease, border-color 0.3s ease !important;
        animation: slide-in-up 0.6s ease both !important;
        overflow: hidden !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    [data-testid="stPlotlyChart"]:hover {
        border-color: rgba(0,245,255,0.38) !important;
        box-shadow: var(--glow-md) !important;
    }
    [data-testid="stPlotlyChart"] .js-plotly-plot,
    [data-testid="stPlotlyChart"] .js-plotly-plot .plot-container,
    [data-testid="stPlotlyChart"] .js-plotly-plot .svg-container {
        overflow: hidden !important;
        width: 100% !important;
    }
    [data-testid="stPlotlyChart"] .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
        border-radius: 12px !important;
    }
    [data-testid="stPlotlyChart"] .js-plotly-plot .plotly .main-svg .bg {
        fill: rgba(5, 14, 31, 0.85) !important;
    }
    [data-testid="stPlotlyChart"] .js-plotly-plot .plotly .main-svg .cartesianlayer .bg {
        fill: rgba(5, 14, 31, 0.70) !important;
    }

    /* ══════════════════════════════════════════════
       DATA FRAMES  — full futuristic theme
       Covers: st.dataframe (Arrow/canvas renderer),
               st.table (legacy HTML renderer),
               and the older stDataFrame wrapper.
    ══════════════════════════════════════════════ */

    /* ── Outer wrapper & entrance animation ── */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrameResizable"],
    .stDataFrame {
        background: rgba(2, 10, 28, 0.88) !important;
        border: 1px solid rgba(0,245,255,0.22) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        box-shadow: 0 0 24px rgba(0,245,255,0.07),
                    inset 0 1px 0 rgba(0,245,255,0.06) !important;
        animation: slide-in-up 0.5s ease both !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    [data-testid="stDataFrame"]:hover,
    [data-testid="stDataFrameResizable"]:hover {
        border-color: rgba(0,245,255,0.40) !important;
        box-shadow: var(--glow-md) !important;
    }

    /* ── Canvas / Arrow renderer (modern Streamlit ≥ 1.23) ── */

    /* The Glide Data Grid canvas element itself */
    [data-testid="stDataFrame"] canvas,
    [data-testid="stDataFrameResizable"] canvas {
        border-radius: 10px !important;
    }

    /* Toolbar row (search, download, fullscreen icons) */
    [data-testid="stDataFrame"] [data-testid="stElementToolbar"],
    [data-testid="stDataFrameResizable"] [data-testid="stElementToolbar"] {
        background: rgba(0, 8, 22, 0.92) !important;
        border-bottom: 1px solid rgba(0,245,255,0.12) !important;
        padding: 4px 10px !important;
    }
    [data-testid="stElementToolbar"] button {
        color: var(--neon-cyan) !important;
        opacity: 0.7 !important;
        transition: opacity 0.2s, box-shadow 0.2s !important;
    }
    [data-testid="stElementToolbar"] button:hover {
        opacity: 1 !important;
        box-shadow: var(--glow-sm) !important;
    }

    /* Resize handle bar at the bottom */
    [data-testid="stDataFrameResizable"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(0,245,255,0.04) !important;
    }

    /* ── Legacy HTML renderer (st.table / older st.dataframe) ── */

    /* Table shell */
    [data-testid="stDataFrame"] table,
    [data-testid="stDataFrame"] .dataframe,
    .stDataFrame table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.82rem !important;
        color: var(--text-primary) !important;
    }

    /* Header row */
    [data-testid="stDataFrame"] thead tr,
    [data-testid="stDataFrame"] .dataframe thead tr,
    .stDataFrame thead tr {
        background: rgba(0, 20, 50, 0.95) !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 2 !important;
    }

    /* Header cells */
    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] .dataframe th,
    .stDataFrame th {
        background: rgba(0, 18, 45, 0.96) !important;
        color: var(--neon-cyan) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.63rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.13em !important;
        text-transform: uppercase !important;
        text-align: center !important;
        padding: 10px 14px !important;
        border-bottom: 2px solid rgba(0,245,255,0.30) !important;
        border-right: 1px solid rgba(0,245,255,0.07) !important;
        white-space: nowrap !important;
        text-shadow: 0 0 6px rgba(0,245,255,0.35) !important;
        cursor: default !important;
        user-select: none !important;
    }
    [data-testid="stDataFrame"] th:last-child,
    .stDataFrame th:last-child {
        border-right: none !important;
    }

    /* Sort indicator (↑ ↓) on sortable headers */
    [data-testid="stDataFrame"] th[aria-sort],
    .stDataFrame th[aria-sort] {
        color: var(--neon-cyan) !important;
        border-bottom-color: var(--neon-cyan) !important;
    }
    [data-testid="stDataFrame"] th[aria-sort="ascending"]::after  { content: " ↑"; color: var(--neon-cyan); }
    [data-testid="stDataFrame"] th[aria-sort="descending"]::after { content: " ↓"; color: var(--neon-purple); }

    /* Index column header (blank top-left cell) */
    [data-testid="stDataFrame"] th:first-child,
    .stDataFrame th:first-child {
        color: rgba(0,245,255,0.40) !important;
        background: rgba(0, 12, 32, 0.98) !important;
        border-right: 1px solid rgba(0,245,255,0.15) !important;
    }

    /* Body rows — base */
    [data-testid="stDataFrame"] tbody tr,
    [data-testid="stDataFrame"] .dataframe tbody tr,
    .stDataFrame tbody tr {
        transition: background 0.18s ease !important;
    }

    /* Alternating row stripe */
    [data-testid="stDataFrame"] tbody tr:nth-child(odd),
    [data-testid="stDataFrame"] .dataframe tbody tr:nth-child(odd),
    .stDataFrame tbody tr:nth-child(odd) {
        background: rgba(0, 12, 30, 0.60) !important;
    }
    [data-testid="stDataFrame"] tbody tr:nth-child(even),
    [data-testid="stDataFrame"] .dataframe tbody tr:nth-child(even),
    .stDataFrame tbody tr:nth-child(even) {
        background: rgba(0, 8, 22, 0.42) !important;
    }

    /* Row hover highlight */
    [data-testid="stDataFrame"] tbody tr:hover,
    [data-testid="stDataFrame"] .dataframe tbody tr:hover,
    .stDataFrame tbody tr:hover {
        background: rgba(0,245,255,0.06) !important;
        box-shadow: inset 0 0 0 1px rgba(0,245,255,0.10) !important;
    }

    /* Body cells */
    [data-testid="stDataFrame"] td,
    [data-testid="stDataFrame"] .dataframe td,
    .stDataFrame td {
        color: var(--text-primary) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.82rem !important;
        padding: 8px 14px !important;
        text-align: center !important;
        border-bottom: 1px solid rgba(0,245,255,0.055) !important;
        border-right: 1px solid rgba(0,245,255,0.04) !important;
        vertical-align: middle !important;
        white-space: nowrap !important;
    }
    [data-testid="stDataFrame"] td:last-child,
    .stDataFrame td:last-child {
        border-right: none !important;
    }

    /* Index column cells */
    [data-testid="stDataFrame"] tbody td:first-child,
    .stDataFrame tbody td:first-child {
        color: var(--text-muted) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.75rem !important;
        background: rgba(0, 10, 28, 0.75) !important;
        border-right: 1px solid rgba(0,245,255,0.12) !important;
        letter-spacing: 0.04em !important;
    }

    /* Selected / focused cell */
    [data-testid="stDataFrame"] td:focus,
    [data-testid="stDataFrame"] td[aria-selected="true"],
    .stDataFrame td:focus {
        outline: 1px solid rgba(0,245,255,0.45) !important;
        background: rgba(0,245,255,0.08) !important;
        color: var(--neon-cyan) !important;
    }

    /* Scrollbar inside the DataFrame scroll container */
    [data-testid="stDataFrame"] ::-webkit-scrollbar,
    [data-testid="stDataFrameResizable"] ::-webkit-scrollbar {
        width: 5px !important;
        height: 5px !important;
    }
    [data-testid="stDataFrame"] ::-webkit-scrollbar-track,
    [data-testid="stDataFrameResizable"] ::-webkit-scrollbar-track {
        background: rgba(1, 5, 16, 0.85) !important;
        border-radius: 4px !important;
    }
    [data-testid="stDataFrame"] ::-webkit-scrollbar-thumb,
    [data-testid="stDataFrameResizable"] ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--neon-cyan), var(--neon-purple)) !important;
        border-radius: 4px !important;
    }
    [data-testid="stDataFrame"] ::-webkit-scrollbar-thumb:hover,
    [data-testid="stDataFrameResizable"] ::-webkit-scrollbar-thumb:hover {
        background: var(--neon-cyan) !important;
    }

    /* ── st.table (pure HTML <table>, no testid wrapper) ── */
    .stTable table,
    div[data-testid="stTable"] table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.82rem !important;
        background: rgba(2, 10, 28, 0.88) !important;
        border: 1px solid rgba(0,245,255,0.20) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 0 20px rgba(0,245,255,0.06) !important;
    }
    .stTable th,
    div[data-testid="stTable"] th {
        background: rgba(0, 18, 45, 0.96) !important;
        color: var(--neon-cyan) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.63rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.13em !important;
        text-transform: uppercase !important;
        text-align: center !important;
        padding: 10px 14px !important;
        border-bottom: 2px solid rgba(0,245,255,0.28) !important;
        text-shadow: 0 0 6px rgba(0,245,255,0.35) !important;
    }
    .stTable td,
    div[data-testid="stTable"] td {
        color: var(--text-primary) !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.82rem !important;
        padding: 8px 14px !important;
        text-align: center !important;
        border-bottom: 1px solid rgba(0,245,255,0.055) !important;
    }
    .stTable tbody tr:nth-child(odd),
    div[data-testid="stTable"] tbody tr:nth-child(odd) {
        background: rgba(0, 12, 30, 0.55) !important;
    }
    .stTable tbody tr:hover td,
    div[data-testid="stTable"] tbody tr:hover td {
        background: rgba(0,245,255,0.06) !important;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid rgba(0,245,255,0.13) !important;
        gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-muted) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.70rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.25s ease !important;
        padding: 10px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--neon-cyan) !important;
        border-bottom-color: var(--neon-cyan) !important;
        text-shadow: var(--glow-sm) !important;
    }

    /* ── MISC ── */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-purple), transparent) !important;
        margin: 2rem 0 !important;
        opacity: 0.45 !important;
    }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #010510; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--neon-cyan), var(--neon-purple));
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }
    footer { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* ── HIDE SIDEBAR NAV HEADER (keyboard_double icon text) ── */
    [data-testid="stSidebarNavHeader"]      { display: none !important; }
    [data-testid="stSidebarNavSeparator"]   { display: none !important; }
    [data-testid="stSidebarNav"] > div:first-child > span { display: none !important; }
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] > div > ul > li:first-child > a > span:first-child { display: none !important; }

    /* ══════════════════════════════════════════════
       INSIGHT CARDS
    ══════════════════════════════════════════════ */

    .insight-card {
        background: rgba(0, 12, 35, 0.82);
        border: 1px solid rgba(0,245,255,0.28);
        border-left: 3px solid var(--neon-cyan);
        border-radius: 12px;
        padding: 14px 18px 14px 20px;
        margin: 6px 0;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 0 14px rgba(0,245,255,0.07),
                    inset 0 1px 0 rgba(0,245,255,0.06);
        animation: slide-in-up 0.4s ease both;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .insight-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: linear-gradient(135deg,
            rgba(0,245,255,0.04) 0%,
            transparent 60%);
        pointer-events: none;
    }

    .insight-card:hover {
        border-color: rgba(0,245,255,0.55);
        border-left-color: var(--neon-cyan);
        box-shadow: 0 0 22px rgba(0,245,255,0.14);
    }

    .insight-card.positive { border-left-color: #00ff88; border-color: rgba(0,255,136,0.25); }
    .insight-card.positive:hover { border-color: rgba(0,255,136,0.55); box-shadow: 0 0 22px rgba(0,255,136,0.14); }

    .insight-card.negative { border-left-color: #ff0080; border-color: rgba(255,0,128,0.25); }
    .insight-card.negative:hover { border-color: rgba(255,0,128,0.55); box-shadow: 0 0 22px rgba(255,0,128,0.14); }

    .insight-card.warning  { border-left-color: #ffaa00; border-color: rgba(255,170,0,0.25); }
    .insight-card.warning:hover  { border-color: rgba(255,170,0,0.55); box-shadow: 0 0 22px rgba(255,170,0,0.14); }

    .insight-card.purple   { border-left-color: var(--neon-purple); border-color: rgba(191,0,255,0.25); }
    .insight-card.purple:hover   { border-color: rgba(191,0,255,0.55); box-shadow: 0 0 22px rgba(191,0,255,0.14); }

    .insight-label {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #5a9fc0;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 7px;
    }
    .insight-label .dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--neon-cyan);
        box-shadow: 0 0 6px var(--neon-cyan);
        flex-shrink: 0;
        animation: corner-pulse 2s ease-in-out infinite;
    }
    .insight-card.positive .dot { background: #00ff88; box-shadow: 0 0 6px #00ff88; }
    .insight-card.negative .dot { background: #ff0080; box-shadow: 0 0 6px #ff0080; }
    .insight-card.warning  .dot { background: #ffaa00; box-shadow: 0 0 6px #ffaa00; }
    .insight-card.purple   .dot { background: var(--neon-purple); box-shadow: 0 0 6px var(--neon-purple); }

    .insight-text {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
        color: #c8e4f5;
        line-height: 1.5;
        margin: 0;
    }
    .insight-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.82rem;
        color: var(--neon-cyan);
        margin-top: 6px;
        opacity: 0.85;
    }
    .insight-card.positive .insight-value { color: #00ff88; }
    .insight-card.negative .insight-value { color: #ff0080; }
    .insight-card.warning  .insight-value { color: #ffaa00; }
    .insight-card.purple   .insight-value { color: var(--neon-purple); }

    /* ══════════════════════════════════════════════
       FUTURISTIC HTML TABLE  (.ftable)
       Used by df_table() helper — CSS text-align
       works here because it is real HTML, not canvas.
    ══════════════════════════════════════════════ */
    .ftable-wrap {
        width: 100%;
        overflow-x: auto;
        border-radius: 14px;
        border: 1px solid rgba(0,245,255,0.22);
        background: rgba(2, 10, 28, 0.88);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 0 24px rgba(0,245,255,0.07),
                    inset 0 1px 0 rgba(0,245,255,0.06);
        animation: slide-in-up 0.5s ease both;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    .ftable-wrap:hover {
        border-color: rgba(0,245,255,0.40);
        box-shadow: var(--glow-md);
    }
    .ftable-wrap::-webkit-scrollbar { height: 5px; }
    .ftable-wrap::-webkit-scrollbar-track { background: rgba(1,5,16,0.85); border-radius: 4px; }
    .ftable-wrap::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple));
        border-radius: 4px;
    }

    .ftable {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.83rem;
        color: var(--text-primary);
    }

    /* Header */
    .ftable thead tr {
        background: rgba(0, 18, 45, 0.97);
        position: sticky;
        top: 0;
        z-index: 2;
    }
    .ftable thead th {
        color: var(--neon-cyan) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.63rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.13em !important;
        text-transform: uppercase !important;
        text-align: center !important;
        padding: 11px 16px !important;
        border-bottom: 2px solid rgba(0,245,255,0.30) !important;
        border-right: 1px solid rgba(0,245,255,0.07) !important;
        white-space: nowrap !important;
        text-shadow: 0 0 6px rgba(0,245,255,0.35) !important;
        user-select: none !important;
    }
    .ftable thead th:last-child { border-right: none !important; }

    /* Index header (top-left blank cell) */
    .ftable thead th.ft-idx {
        color: rgba(0,245,255,0.35) !important;
        background: rgba(0, 12, 32, 0.98) !important;
        border-right: 1px solid rgba(0,245,255,0.15) !important;
        min-width: 42px !important;
    }

    /* Body rows */
    .ftable tbody tr:nth-child(odd)  { background: rgba(0, 12, 30, 0.58); }
    .ftable tbody tr:nth-child(even) { background: rgba(0, 8, 22, 0.40); }
    .ftable tbody tr {
        transition: background 0.18s ease;
    }
    .ftable tbody tr:hover {
        background: rgba(0,245,255,0.06) !important;
        box-shadow: inset 0 0 0 1px rgba(0,245,255,0.10);
    }

    /* Body cells */
    .ftable tbody td {
        text-align: center !important;
        padding: 8px 16px !important;
        border-bottom: 1px solid rgba(0,245,255,0.055) !important;
        border-right: 1px solid rgba(0,245,255,0.04) !important;
        vertical-align: middle !important;
        white-space: nowrap !important;
    }
    .ftable tbody td:last-child { border-right: none !important; }

    /* Index body cell */
    .ftable tbody td.ft-idx {
        color: var(--text-muted) !important;
        font-size: 0.75rem !important;
        background: rgba(0, 10, 28, 0.72) !important;
        border-right: 1px solid rgba(0,245,255,0.12) !important;
        text-align: center !important;
        letter-spacing: 0.04em !important;
    }

    /* Last row — no bottom border bleed */
    .ftable tbody tr:last-child td { border-bottom: none !important; }

    </style>
    <script>
    (function() {
        function hideKeyboardDouble() {
            var walker = document.createTreeWalker(
                document.body, NodeFilter.SHOW_TEXT, null, false
            );
            var node;
            while ((node = walker.nextNode())) {
                if (node.textContent.indexOf('keyboard_double') !== -1) {
                    var el = node.parentElement;
                    for (var i = 0; i < 6; i++) {
                        if (!el || el === document.body) break;
                        var tag = el.tagName;
                        if (tag === 'LI' || tag === 'A' || tag === 'SPAN' ||
                            (tag === 'DIV' && el.children.length <= 3)) {
                            el.style.setProperty('display', 'none', 'important');
                            break;
                        }
                        el = el.parentElement;
                    }
                }
            }
        }
        hideKeyboardDouble();
        setTimeout(hideKeyboardDouble, 200);
        setTimeout(hideKeyboardDouble, 600);
        setTimeout(hideKeyboardDouble, 1500);
        var obs = new MutationObserver(function() { hideKeyboardDouble(); });
        obs.observe(document.body, { childList: true, subtree: true });
    })();
    </script>
    """, unsafe_allow_html=True)


# ── Plotly theme helpers ──────────────────────────────────────────────────────

NEON_PALETTE = ["#00f5ff", "#0066ff", "#bf00ff", "#00ff88", "#ff0080", "#ffaa00"]
CHART_H = 340


def plotly_futuristic_layout(title: str = "") -> dict:
    """Futuristic neon Plotly layout"""

    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(4, 12, 28, 0.85)",
        height=CHART_H,
        autosize=True,

        font=dict(
            family="Rajdhani, sans-serif",
            color="#a0cfff",
            size=13
        ),

        title=dict(
            text=title,
            font=dict(
                family="Orbitron, sans-serif",
                size=18,
                color="#00f5ff"
            ),
            x=0.02,
            pad=dict(b=14),
        ),

        xaxis=dict(
            gridcolor="rgba(0,245,255,0.055)",
            gridwidth=1,
            linecolor="rgba(0,245,255,0.13)",
            tickfont=dict(
                family="Share Tech Mono",
                color="#4a7fa5",
                size=11
            ),
            title_font=dict(
                family="Rajdhani",
                color="#4a7fa5",
                size=12
            ),
            zeroline=False,
        ),

        yaxis=dict(
            gridcolor="rgba(0,245,255,0.055)",
            gridwidth=1,
            linecolor="rgba(0,245,255,0.13)",
            tickfont=dict(
                family="Share Tech Mono",
                color="#4a7fa5",
                size=11
            ),
            title_font=dict(
                family="Rajdhani",
                color="#4a7fa5",
                size=12
            ),
            zeroline=False,
        ),

        hoverlabel=dict(
            bgcolor="rgba(2, 7, 20, 0.94)",
            bordercolor="rgba(0,245,255,0.38)",
            font=dict(
                family="Share Tech Mono",
                color="#00f5ff",
                size=12
            ),
        ),

        legend=dict(
            bgcolor="rgba(4,12,28,0.75)",
            bordercolor="rgba(0,245,255,0.18)",
            borderwidth=1,
            font=dict(
                family="Rajdhani",
                color="#7aadcc",
                size=12
            ),
        ),

        margin=dict(l=50, r=20, t=54, b=42),
    )


def apply_plotly_theme_to_figure(fig, title: str = ""):
    """Apply futuristic layout + neon trace colours to any Plotly figure."""
    fig.update_layout(**plotly_futuristic_layout(title))
    for i, trace in enumerate(fig.data):
        colour = NEON_PALETTE[i % len(NEON_PALETTE)]
        t = type(trace).__name__.lower()
        if "scatter" in t or "line" in t:
            trace.update(
                line=dict(color=colour, width=2.5),
                marker=dict(color=colour, size=6),
            )
        elif "bar" in t:
            trace.update(marker=dict(color=colour, opacity=0.85))
        elif "pie" in t or "funnel" in t:
            trace.update(
                marker=dict(colors=NEON_PALETTE),
                textfont=dict(family="Share Tech Mono", color="#e0f4ff", size=12),
            )
    return fig


# convenience aliases so any import style works
style_fig = apply_plotly_theme_to_figure


def chart(fig, title: str = ""):
    """Render a themed Plotly chart — no scroll, no overflow."""
    fig = apply_plotly_theme_to_figure(fig, title)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ── Insight card helper ───────────────────────────────────────────────────────

def insight(
    text: str,
    label: str = "Insight",
    value: str = "",
    kind: str = "default",
):
    """
    Render a futuristic insight card.

    Parameters
    ----------
    text  : Main insight sentence shown in the card body.
    label : Small uppercase tag above the text (e.g. "Insight", "Trend", "Alert").
    value : Optional secondary metric/value shown below the text in mono font.
    kind  : Visual variant — "default" | "positive" | "negative" | "warning" | "purple"

    Usage
    -----
        insight("Revenue grew 18% QoQ driven by the APAC region.",
                label="Trend", value="+18.4% QoQ", kind="positive")
    """
    variant = kind if kind in ("positive", "negative", "warning", "purple") else ""
    css_class = f"insight-card {variant}".strip()

    value_html = (
        f'<div class="insight-value">{value}</div>' if value else ""
    )

    st.markdown(
        f"""
        <div class="{css_class}">
            <div class="insight-label">
                <span class="dot"></span>{label}
            </div>
            <p class="insight-text">{text}</p>
            {value_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── DataFrame HTML table helper ───────────────────────────────────────────────

def df_table(
    df,
    show_index: bool = True,
    max_rows: int | None = None,
):
    """
    Render a pandas DataFrame as a fully-themed futuristic HTML table with
    all values perfectly center-aligned.

    Use this instead of st.dataframe() whenever you need centered text,
    because Streamlit's canvas-based renderer ignores CSS text-align.

    Parameters
    ----------
    df         : pandas DataFrame to display.
    show_index : Show the row index column (default True).
    max_rows   : Optionally cap the number of rows shown.

    Usage
    -----
        import pandas as pd
        df = pd.DataFrame({"Product": ["Chair", "Desk"], "Sales": [78000, 27000]})
        df_table(df)
    """
    if max_rows is not None:
        df = df.head(max_rows)

    # ── header ──
    if show_index:
        header = '<th class="ft-idx"></th>' + "".join(
            f"<th>{col}</th>" for col in df.columns
        )
    else:
        header = "".join(f"<th>{col}</th>" for col in df.columns)

    # ── rows ──
    rows_html = ""
    for idx, row in df.iterrows():
        if show_index:
            cells = f'<td class="ft-idx">{idx}</td>' + "".join(
                f"<td>{v}</td>" for v in row
            )
        else:
            cells = "".join(f"<td>{v}</td>" for v in row)
        rows_html += f"<tr>{cells}</tr>"

    html = f"""
    <div class="ftable-wrap">
      <table class="ftable">
        <thead><tr>{header}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
