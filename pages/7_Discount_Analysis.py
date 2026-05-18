import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.styles import (
    apply_futuristic_style, page_header, section_header, chart_label,
    kpi_card, sidebar_brand, insight, footer, df_table, plotly_futuristic_layout,
    COLOR_SEQ, COLORS,
)
from utils.data import load_raw, clean, format_currency, format_value, sidebar_filters

st.set_page_config(page_icon="📡", page_title="Sales Intelligence", layout="wide")
apply_futuristic_style()
sidebar_brand()

df = clean(load_raw())
filtered_df = sidebar_filters(df)

page_header("Discount Intelligence", "Distribution, impact on performance & optimisation", "🎁")

avg_discount       = filtered_df["Discount"].mean() * 100
max_discount       = filtered_df["Discount"].max() * 100
high_disc_orders   = (filtered_df["Discount"] >= 0.3).sum()
zero_disc_orders   = (filtered_df["Discount"] == 0).sum()

col1, col2, col3, col4 = st.columns(4)
kpi_card(col1, "Avg Discount",        f"{avg_discount:.1f}%",           icon="🎁", color=COLORS["cyan"])
kpi_card(col2, "Max Discount Given",  f"{max_discount:.0f}%",           icon="⚠️", color=COLORS["red"])
kpi_card(col3, "High Disc Orders ≥30%", format_value(high_disc_orders), icon="📉", color=COLORS["amber"])
kpi_card(col4, "Zero Discount Orders",  format_value(zero_disc_orders), icon="✅", color=COLORS["green"])

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Discount Distribution", "Impact on Performance", "Optimisation View"])

with tab1:
    filtered_df["Discount_Pct"] = (filtered_df["Discount"] * 100).round(0).astype(int)

    chart_label("Discount % Distribution", "Frequency histogram")
    fig_hist = px.histogram(filtered_df, x="Discount_Pct", nbins=20,
                            color_discrete_sequence=[COLORS["cyan"]])
    fig_hist.update_layout(**plotly_futuristic_layout())
    fig_hist.update_traces(marker=dict(color=COLORS["cyan"], opacity=0.8,
                                       line=dict(color=COLORS["purple"], width=1)))
    st.plotly_chart(fig_hist, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        chart_label("Avg Discount % by Product")
        dp = (filtered_df.groupby("Product")["Discount"].mean().reset_index())
        dp["Discount"] = (dp["Discount"] * 100).round(2)
        dp = dp.sort_values("Discount", ascending=False)
        fig_dp = px.bar(dp, x="Product", y="Discount", color="Discount",
                        color_continuous_scale=["#3B82F6", "#F59E0B", "#EF4444"])
        fig_dp.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_dp, width="stretch")

    with col2:
        chart_label("Avg Discount % by Region")
        dr = (filtered_df.groupby("Region")["Discount"].mean().reset_index())
        dr["Discount"] = (dr["Discount"] * 100).round(2)
        fig_dr = px.bar(dr, x="Region", y="Discount", color="Discount",
                        color_continuous_scale=["#3B82F6", "#F59E0B", "#EF4444"])
        fig_dr.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_dr, width="stretch")

with tab2:
    discount_bins = pd.cut(
        filtered_df["Discount"],
        bins=[0, 0.05, 0.15, 0.25, 0.50, 1.0],
        labels=["0–5%", "5–15%", "15–25%", "25–50%", "50%+"],
        include_lowest=True,
    )
    filtered_df = filtered_df.copy()
    filtered_df["Discount_Band"] = discount_bins

    band_perf = (
        filtered_df.groupby("Discount_Band", observed=True)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
             Orders=("Order_ID", "nunique"))
        .reset_index()
    )
    band_perf["Margin_Pct"] = (band_perf["Profit"] / band_perf["Sales"] * 100).fillna(0).round(2)

    band_colors = [COLORS["green"], COLORS["cyan"], COLORS["blue"], COLORS["amber"], COLORS["red"]]

    col1, col2 = st.columns(2)
    with col1:
        chart_label("Revenue by Discount Band")
        fig_bs = px.bar(band_perf, x="Discount_Band", y="Sales", color="Discount_Band",
                        color_discrete_sequence=band_colors)
        fig_bs.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_bs, width="stretch")

    with col2:
        chart_label("Profit Margin % by Discount Band")
        fig_bm = px.bar(band_perf, x="Discount_Band", y="Margin_Pct", color="Discount_Band",
                        color_discrete_sequence=band_colors)
        fig_bm.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_bm, width="stretch")

    chart_label("Order Volume by Discount Band")
    fig_bo = px.bar(band_perf, x="Discount_Band", y="Orders", color="Discount_Band",
                    color_discrete_sequence=band_colors)
    fig_bo.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_bo, width="stretch")

with tab3:
    rep_disc = (
        filtered_df.groupby("Sales_Rep")
        .agg(Avg_Discount=("Discount", "mean"), Total_Sales=("Sales", "sum"),
             Profit_Margin=("Profit_Margin", "mean"))
        .reset_index()
    )
    rep_disc["Avg_Discount"]   = (rep_disc["Avg_Discount"]   * 100).round(2)
    rep_disc["Profit_Margin"]  = (rep_disc["Profit_Margin"]  * 100).round(2)

    chart_label("Rep Avg Discount vs Profit Margin", "Bubble = total sales volume")
    fig_rd = px.scatter(rep_disc, x="Avg_Discount", y="Profit_Margin", size="Total_Sales",
                        color="Sales_Rep", text="Sales_Rep",
                        color_discrete_sequence=COLOR_SEQ, size_max=50)
    fig_rd.update_traces(textposition="top center",
                         textfont=dict(color=COLORS["cyan"], family="Inter", size=10))
    fig_rd.update_layout(**plotly_futuristic_layout(height=420))
    st.plotly_chart(fig_rd, width="stretch")

    section_header("Discount Band Performance Summary")
    bd = band_perf.copy()
    bd["Sales"]   = bd["Sales"].apply(format_currency)
    bd["Profit"]  = bd["Profit"].apply(format_currency)
    bd.columns = ["Discount Band", "Revenue", "Profit", "Orders", "Margin %"]
    df_table(bd, show_index=False)

st.markdown("---")
section_header("Key Signals")
col1, col2 = st.columns(2)
with col1:
    insight(f"Average discount of {avg_discount:.1f}% across orders. Tiered discount authorisation levels can preserve margin without losing volume.", label="Discount Policy", kind="warning")
    insight("Products receiving the highest discounts should be cross-checked against return rates — excessive discounting may attract low-intent buyers.", label="Discount Risk", kind="error")
with col2:
    insight("The 5–15% discount band typically maximises revenue without a disproportionate margin hit — the optimal sweet spot for most categories.", label="Sweet Spot", kind="positive")
    insight("Reps with consistently high discount averages warrant coaching — structured conversations around deal quality vs. deal volume can shift behaviour.", label="Rep Coaching", kind="purple")

footer()
