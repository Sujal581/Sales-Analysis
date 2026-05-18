import streamlit as st

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #070B14 0%, #0d1117 50%, #070B14 100%) !important;
    color: #f1f5f9 !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }


.block-container {
    padding: 1.5rem 2.5rem 3rem 2.5rem !important;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #0b1120 100%) !important;
    border-right: 1px solid rgba(0,245,255,0.15) !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem !important;
}

[data-testid="stSidebarNav"] a {
    border-radius: 8px !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    margin: 2px 0 !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(0,245,255,0.08) !important;
    color: #00F5FF !important;
    border-color: rgba(0,245,255,0.2) !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(0,245,255,0.1) !important;
    color: #00F5FF !important;
    border-left: 3px solid #00F5FF !important;
    box-shadow: 0 0 12px rgba(0,245,255,0.15) !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown div { color: #64748b !important; font-size: 0.82rem !important; }

[data-testid="stSidebar"] hr {
    border-color: rgba(0,245,255,0.1) !important;
    margin: 0.75rem 0 !important;
}

[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
}

h1 {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem !important;
}

h2 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
    letter-spacing: 0.02em;
}

h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}

p, li { color: #94a3b8; line-height: 1.7; }

.nc-kpi-card {
    background: linear-gradient(145deg, rgba(17,24,39,0.9), rgba(11,17,32,0.9));
    border-left: 3px solid;
    border-top: 1px solid rgba(255,255,255,0.05);
    border-right: 1px solid rgba(255,255,255,0.03);
    border-bottom: 1px solid rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
    position: relative;
    overflow: hidden;
}

.nc-kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), transparent);
}

.nc-kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.5), 0 0 20px rgba(0,245,255,0.05);
}

.nc-kpi-icon { font-size: 1.1rem; margin-bottom: 0.4rem; }
.nc-kpi-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.nc-kpi-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1;
}
.nc-kpi-delta { font-size: 0.75rem; color: #475569; margin-top: 0.35rem; }

.nc-section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 1.75rem 0 0.75rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0,245,255,0.1);
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.nc-chart-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #cbd5e1;
    margin-bottom: 0.2rem;
    letter-spacing: 0.03em;
}

.nc-chart-sub { font-size: 0.75rem; color: #475569; margin-bottom: 0.5rem; }

.nc-insight {
    border-left: 3px solid;
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
    line-height: 1.65;
    color: #cbd5e1;
    backdrop-filter: blur(4px);
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(17,24,39,0.9), rgba(11,17,32,0.9)) !important;
    border: 1px solid rgba(0,245,255,0.1) !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    transition: transform 0.2s ease !important;
}

[data-testid="stMetric"]:hover { transform: translateY(-2px) !important; }

[data-testid="stMetricLabel"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: #475569 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
}

.stButton > button {
    background: rgba(17,24,39,0.8) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(0,245,255,0.2) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1.1rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: rgba(0,245,255,0.08) !important;
    border-color: #00F5FF !important;
    color: #00F5FF !important;
    box-shadow: 0 0 12px rgba(0,245,255,0.2) !important;
}

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background: rgba(17,24,39,0.8) !important;
    border: 1px solid rgba(0,245,255,0.15) !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    font-size: 0.85rem !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,245,255,0.1) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

[data-testid="stExpander"] {
    background: rgba(17,24,39,0.8) !important;
    border: 1px solid rgba(0,245,255,0.1) !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary { color: #cbd5e1 !important; font-weight: 500 !important; }

.stTabs [data-baseweb="tab-list"] {
    background: rgba(11,17,32,0.9);
    border-radius: 10px;
    padding: 3px;
    gap: 3px;
    border: 1px solid rgba(0,245,255,0.1);
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    border-radius: 8px !important;
    padding: 0.35rem 0.9rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 0.03em !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,245,255,0.1) !important;
    color: #00F5FF !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}

hr {
    border: none !important;
    border-top: 1px solid rgba(0,245,255,0.08) !important;
    margin: 1.5rem 0 !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #070B14; }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,245,255,0.5); }

/* ── FUTURISTIC TABLE ── */
.ftable-wrap {
    width: 100%;
    overflow-x: auto;
    border-radius: 12px;
    border: 1px solid rgba(0,245,255,0.1);
    background: rgba(17,24,39,0.9);
    backdrop-filter: blur(8px);
    margin-bottom: 1rem;
}
.ftable {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-family: 'Inter', sans-serif;
    font-size: 0.83rem;
    color: #cbd5e1;
}
.ftable thead tr { background: rgba(11,17,32,0.98); }
.ftable thead th {
    color: #00F5FF !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    text-align: center !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid rgba(0,245,255,0.15) !important;
    border-right: 1px solid rgba(0,245,255,0.05) !important;
    white-space: nowrap !important;
}
.ftable thead th:last-child { border-right: none !important; }
.ftable thead th.ft-idx {
    color: rgba(0,245,255,0.35) !important;
    background: rgba(0,12,32,0.98) !important;
    border-right: 1px solid rgba(0,245,255,0.1) !important;
    min-width: 40px !important;
}
.ftable tbody tr:nth-child(odd)  { background: rgba(17,24,39,0.5); }
.ftable tbody tr:nth-child(even) { background: rgba(11,17,32,0.35); }
.ftable tbody tr:hover { background: rgba(0,245,255,0.04) !important; }
.ftable tbody td {
    text-align: center !important;
    padding: 8px 14px !important;
    border-bottom: 1px solid rgba(0,245,255,0.04) !important;
    border-right: 1px solid rgba(0,245,255,0.03) !important;
    vertical-align: middle !important;
    white-space: nowrap !important;
}
.ftable tbody td:last-child { border-right: none !important; }
.ftable tbody td.ft-idx {
    color: #475569 !important;
    font-size: 0.75rem !important;
    background: rgba(11,17,32,0.6) !important;
    border-right: 1px solid rgba(0,245,255,0.08) !important;
}
.ftable tbody tr:last-child td { border-bottom: none !important; }
</style>
"""

COLORS = {
    "blue":   "#3B82F6",
    "green":  "#10B981",
    "amber":  "#F59E0B",
    "red":    "#EF4444",
    "purple": "#8B5CF6",
    "cyan":   "#00F5FF",
    "pink":   "#EC4899",
}
COLOR_SEQ = list(COLORS.values())

PLOT_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(11,17,32,0.0)",
    plot_bgcolor="rgba(11,17,32,0.0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8", size=12),
    xaxis=dict(gridcolor="rgba(0,245,255,0.06)", zeroline=False, linecolor="rgba(0,245,255,0.1)"),
    yaxis=dict(gridcolor="rgba(0,245,255,0.06)", zeroline=False, linecolor="rgba(0,245,255,0.1)"),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(
        bgcolor="rgba(11,17,32,0.8)",
        bordercolor="rgba(0,245,255,0.15)",
        borderwidth=1,
        font=dict(size=11),
    ),
)


# ── Core helpers ──────────────────────────────────────────────────────────────

def apply_futuristic_style():
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# alias
inject_css = apply_futuristic_style


def sidebar_brand(title: str = "Sales Intelligence", subtitle: str = "Analytics Platform"):
    st.sidebar.markdown(f"""
        <div style="padding:0.5rem 0 1.25rem 0;">
            <div style="font-family:'Orbitron',sans-serif;font-size:1rem;font-weight:700;
                        background:linear-gradient(135deg,#00F5FF,#8B5CF6);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;">{title}</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:0.72rem;color:#475569;
                        margin-top:3px;letter-spacing:0.1em;text-transform:uppercase;">
                {subtitle}
            </div>
        </div>
        <hr style="border:none;border-top:1px solid rgba(0,245,255,0.1);margin:0 0 0.75rem 0;">
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    label = f"{icon} {title}" if icon else title
    sub_html = (
        f"<p style='color:#475569;font-size:0.875rem;margin:0;font-family:Rajdhani,sans-serif;"
        f"letter-spacing:0.04em;'>{subtitle}</p>"
        if subtitle else ""
    )
    st.markdown(f"""
        <div style="margin-bottom:1.5rem;padding-bottom:1rem;
                    border-bottom:1px solid rgba(0,245,255,0.1);">
            <h1 style="margin-bottom:0.2rem!important;
                       background:linear-gradient(135deg,#f1f5f9,#94a3b8);
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                       background-clip:text;">{label}</h1>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    st.markdown(f'<div class="nc-section-header">{title}</div>', unsafe_allow_html=True)


def chart_label(title: str, sub: str = ""):
    st.markdown(
        f'<div class="nc-chart-label">{title}</div>'
        + (f'<div class="nc-chart-sub">{sub}</div>' if sub else ""),
        unsafe_allow_html=True,
    )


def kpi_card(col, title: str, value: str, delta: str = "", icon: str = "", color: str = "#00F5FF"):
    with col:
        delta_html = f'<div class="nc-kpi-delta">{delta}</div>' if delta else ""
        st.markdown(f"""
            <div class="nc-kpi-card" style="border-color:{color};
                 box-shadow:0 4px 20px rgba(0,0,0,0.4),0 0 15px {color}18;">
                <div class="nc-kpi-icon">{icon}</div>
                <div class="nc-kpi-label">{title}</div>
                <div class="nc-kpi-value" style="color:{color};">{value}</div>
                {delta_html}
            </div>
        """, unsafe_allow_html=True)


def footer():
    st.markdown("""
        <div style="margin-top:3rem;padding-top:1.25rem;
                    border-top:1px solid rgba(0,245,255,0.08);
                    display:flex;justify-content:space-between;align-items:center;">
            <div style="font-size:0.72rem;color:#334155;font-family:'Rajdhani',sans-serif;
                        letter-spacing:0.06em;">
                SALES INTELLIGENCE PLATFORM · BUILT WITH STREAMLIT
            </div>
            <div style="font-size:0.72rem;color:#334155;font-family:'Rajdhani',sans-serif;">
                © 2025
            </div>
        </div>
    """, unsafe_allow_html=True)


# ── Insight card ──────────────────────────────────────────────────────────────

def insight_card(text: str, kind: str = "info"):
    palettes = {
        "success": ("#10B981", "rgba(16,185,129,0.08)"),
        "warning": ("#F59E0B", "rgba(245,158,11,0.08)"),
        "error":   ("#EF4444", "rgba(239,68,68,0.08)"),
        "info":    ("#3B82F6", "rgba(59,130,246,0.08)"),
        "purple":  ("#8B5CF6", "rgba(139,92,246,0.08)"),
        "cyan":    ("#00F5FF", "rgba(0,245,255,0.08)"),
    }
    bc, bg = palettes.get(kind, palettes["info"])
    st.markdown(
        f'<div class="nc-insight" style="border-color:{bc};background:{bg};">{text}</div>',
        unsafe_allow_html=True,
    )


def insight(text: str, label: str = "Insight", value: str = "", kind: str = "default"):
    """Backward-compatible wrapper — maps old kind names to new palette."""
    kind_map = {"positive": "success", "negative": "error", "default": "info", "warning": "warning", "purple": "purple"}
    mapped = kind_map.get(kind, "info")
    full_text = f"<strong>{label}</strong> — {text}"
    if value:
        full_text += f"<br><code style='font-size:0.8rem;'>{value}</code>"
    insight_card(full_text, kind=mapped)


# ── Plotly theme ──────────────────────────────────────────────────────────────

def plotly_futuristic_layout(title: str = "", height: int = 380) -> dict:
    layout = dict(**PLOT_LAYOUT)
    layout["height"] = height
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(family="Rajdhani, sans-serif", size=15, color="#e2e8f0"),
            x=0.01, pad=dict(b=8),
        )
    return layout


def apply_plot_layout(fig, height: int = 380):
    fig.update_layout(height=height, **PLOT_LAYOUT)
    return fig


def chart(fig, title: str = "", height: int = 380):
    apply_plot_layout(fig, height)
    if title:
        fig.update_layout(title=dict(
            text=title,
            font=dict(family="Rajdhani, sans-serif", size=15, color="#e2e8f0"),
            x=0.01,
        ))
    st.plotly_chart(fig, width="stretch")


# ── DataFrame HTML table ──────────────────────────────────────────────────────

def df_table(df, show_index: bool = True, max_rows: int | None = None):
    if max_rows is not None:
        df = df.head(max_rows)
    if show_index:
        header = '<th class="ft-idx"></th>' + "".join(f"<th>{col}</th>" for col in df.columns)
    else:
        header = "".join(f"<th>{col}</th>" for col in df.columns)
    rows_html = ""
    for idx, row in df.iterrows():
        if show_index:
            cells = f'<td class="ft-idx">{idx}</td>' + "".join(f"<td>{v}</td>" for v in row)
        else:
            cells = "".join(f"<td>{v}</td>" for v in row)
        rows_html += f"<tr>{cells}</tr>"
    st.markdown(f"""
    <div class="ftable-wrap">
      <table class="ftable">
        <thead><tr>{header}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)
