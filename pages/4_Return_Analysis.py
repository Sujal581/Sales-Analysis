import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import (
    apply_futuristic_style, page_header, section_header, chart_label,
    kpi_card, sidebar_brand, insight, footer, plotly_futuristic_layout,
    COLOR_SEQ, COLORS,
)
from utils.data import load_raw, clean, format_currency, format_value, sidebar_filters

st.set_page_config(page_icon="📡", page_title="Sales Intelligence", layout="wide")
apply_futuristic_style()
sidebar_brand()

df = clean(load_raw())
filtered_df = sidebar_filters(df)

page_header("Return Analysis", "Return rates, damage patterns, trends & risk signals", "🔄")

total_returns   = filtered_df[filtered_df["Return_Status"] == "Yes"].shape[0]
total_unknown   = filtered_df[filtered_df["Return_Status"] == "Unknown Status"].shape[0]
total_damaged   = filtered_df[filtered_df["Return_Status"] == "Damaged"].shape[0]
total_no_return = filtered_df[filtered_df["Return_Status"] == "No"].shape[0]
return_rate     = (total_returns / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
damaged_rate    = (total_damaged / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
kpi_card(col1, "Total Returns",   format_value(total_returns),   icon="🔄", color=COLORS["red"])
kpi_card(col2, "Return Rate",     f"{return_rate:.1f}%",         icon="📊", color=COLORS["amber"])
kpi_card(col3, "Unknown Status",  format_value(total_unknown),   icon="❓", color=COLORS["blue"])
kpi_card(col4, "Damaged",         format_value(total_damaged),   icon="⚠️", color=COLORS["pink"])
kpi_card(col5, "No Return",       format_value(total_no_return), icon="✅", color=COLORS["green"])

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Distribution", "By Dimension", "Trend & Risk"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        chart_label("Return Status Distribution")
        sc = filtered_df["Return_Status"].value_counts().reset_index()
        sc.columns = ["Return_Status", "Count"]
        fig1 = px.pie(sc, values="Count", names="Return_Status",
                      color_discrete_sequence=[COLORS["green"], COLORS["red"], COLORS["amber"], COLORS["blue"], COLORS["purple"]])
        fig1.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig1, width="stretch")

    with col2:
        chart_label("Return vs Non-Return Split", "Donut view")
        fig2 = px.pie(sc, values="Count", names="Return_Status", hole=0.55,
                      color_discrete_sequence=[COLORS["green"], COLORS["red"], COLORS["amber"], COLORS["blue"], COLORS["purple"]])
        fig2.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig2, width="stretch")

    chart_label("Sales Value by Return Status")
    rv = filtered_df.groupby("Return_Status")["Sales"].sum().reset_index()
    fig_val = px.bar(rv, x="Return_Status", y="Sales", color="Return_Status",
                     color_discrete_sequence=[COLORS["green"], COLORS["red"], COLORS["amber"], COLORS["blue"], COLORS["purple"]])
    fig_val.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_val, width="stretch")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        try:
            pr = (filtered_df.groupby("Product")["Return_Status"]
                  .value_counts().unstack().fillna(0).reset_index())
            if "Yes" in pr.columns:
                chart_label("Returns by Product")
                fig3 = px.bar(pr, x="Product", y="Yes", color="Product",
                              color_discrete_sequence=COLOR_SEQ)
                fig3.update_layout(**plotly_futuristic_layout())
                st.plotly_chart(fig3, width="stretch")
        except Exception:
            st.info("Insufficient return data for product breakdown.")

    with col2:
        try:
            rr = (filtered_df.groupby("Region")["Return_Status"]
                  .value_counts().unstack().fillna(0).reset_index())
            if "Yes" in rr.columns:
                chart_label("Returns by Region")
                fig4 = px.bar(rr, x="Region", y="Yes", color="Region",
                              color_discrete_sequence=COLOR_SEQ)
                fig4.update_layout(**plotly_futuristic_layout())
                st.plotly_chart(fig4, width="stretch")
        except Exception:
            st.info("Insufficient return data for region breakdown.")

    chart_label("Return Status by Sales Channel", "Stacked bar")
    cr = (filtered_df.groupby(["Sales_Channel", "Return_Status"])["Order_ID"]
          .count().reset_index(name="Count"))
    fig_cr = px.bar(cr, x="Sales_Channel", y="Count", color="Return_Status",
                    barmode="stack",
                    color_discrete_sequence=[COLORS["green"], COLORS["red"], COLORS["amber"], COLORS["blue"], COLORS["purple"]])
    fig_cr.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_cr, width="stretch")

with tab3:
    try:
        chart_label("Returns Over Time by Status")
        mr = (filtered_df.groupby([filtered_df["Order_Date"].dt.to_period("M"), "Return_Status"])
              .size().reset_index(name="Count"))
        mr["Order_Date"] = mr["Order_Date"].astype(str)
        fig5 = px.line(mr, x="Order_Date", y="Count", color="Return_Status", markers=True,
                       color_discrete_sequence=[COLORS["green"], COLORS["red"], COLORS["amber"], COLORS["blue"], COLORS["purple"]])
        fig5.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig5, width="stretch")
    except Exception:
        st.info("Insufficient date data for trend analysis.")

    dmg = (filtered_df[filtered_df["Return_Status"] == "Damaged"]
           .groupby("Product").size().reset_index(name="Damaged Count")
           .sort_values("Damaged Count", ascending=False))
    if not dmg.empty:
        chart_label("Damaged Items by Product", "High values = packaging/logistics risk")
        fig_d = px.bar(dmg, x="Product", y="Damaged Count", color="Damaged Count",
                       color_continuous_scale=["#3B82F6", COLORS["red"]])
        fig_d.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_d, width="stretch")

st.markdown("---")
section_header("Key Signals")
col1, col2 = st.columns(2)
with col1:
    insight(f"Overall return rate is {return_rate:.1f}%. Industry benchmark is 5–10%; action needed if above threshold.", label="Return Rate Signal", kind="error" if return_rate > 10 else "positive")
    insight(f"{damaged_rate:.1f}% of orders arrive damaged. Root-cause analysis on packaging and logistics partners is the priority next step.", label="Damage Signal", kind="warning")
with col2:
    insight("Products with high return rates likely indicate quality or description mismatches — direct input for product development.", label="Product Signal")
    insight("Unknown return status records represent a data quality gap. Improving return tracking will sharpen operational decisions.", label="Data Quality Alert", kind="purple")

footer()
