import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

page_header("Profit Analysis", "Margin deep-dive, dimension breakdown, top performers", "📈")

filtered_df["Profit"] = filtered_df["Sales"] - filtered_df["Cost"]
total_profit   = filtered_df["Profit"].sum()
total_sales    = filtered_df["Sales"].sum()
total_cost     = filtered_df["Cost"].sum()
total_order    = filtered_df["Order_ID"].nunique()
avg_margin     = filtered_df["Profit_Margin"].mean() * 100
gp_ratio       = (total_profit / total_sales * 100) if total_sales else 0

col1, col2, col3 = st.columns(3)
kpi_card(col1, "Total Profit",       format_currency(total_profit), icon="💰", color=COLORS["green"])
kpi_card(col2, "Total Sales",        format_currency(total_sales),  icon="📊", color=COLORS["cyan"])
kpi_card(col3, "Total Cost",         format_currency(total_cost),   icon="💸", color=COLORS["amber"])

col4, col5, col6 = st.columns(3)
kpi_card(col4, "Total Orders",       format_value(total_order),     icon="📦", color=COLORS["blue"])
kpi_card(col5, "Avg Profit Margin",  f"{avg_margin:.1f}%",          icon="🎯", color=COLORS["purple"])
kpi_card(col6, "Gross Profit Ratio", f"{gp_ratio:.1f}%",            icon="📉", color=COLORS["pink"])

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["By Dimension", "Margin Deep Dive", "Top Performers"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        chart_label("Profit by Region")
        rp = filtered_df.groupby("Region")["Profit"].sum().reset_index()
        fig1 = px.bar(rp, x="Region", y="Profit", color="Profit",
                      color_continuous_scale=["#EF4444", "#3B82F6", "#10B981"])
        fig1.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig1, width="stretch")

    with col2:
        chart_label("Profit by Product")
        pp = (filtered_df.groupby("Product")["Profit"].sum()
              .reset_index().sort_values("Profit", ascending=False))
        fig2 = px.bar(pp, x="Product", y="Profit", color="Product",
                      color_discrete_sequence=COLOR_SEQ)
        fig2.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig2, width="stretch")

    col3, col4 = st.columns(2)
    with col3:
        chart_label("Profit by Sales Channel")
        cp = filtered_df.groupby("Sales_Channel")["Profit"].sum().reset_index()
        fig3 = px.bar(cp, x="Sales_Channel", y="Profit", color="Sales_Channel",
                      color_discrete_sequence=COLOR_SEQ)
        fig3.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig3, width="stretch")

    with col4:
        chart_label("Profit by Payment Mode")
        pmp = filtered_df.groupby("Payment_Mode")["Profit"].sum().reset_index()
        fig4 = px.bar(pmp, x="Payment_Mode", y="Profit", color="Payment_Mode",
                      color_discrete_sequence=COLOR_SEQ)
        fig4.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig4, width="stretch")

with tab2:
    product_margin = (
        filtered_df.groupby("Product")
        .agg(Profit_Margin=("Profit_Margin", "mean"),
             Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )
    product_margin["Profit_Margin"] = (product_margin["Profit_Margin"] * 100).round(2)

    chart_label("Sales vs Profit Margin", "Bubble size = profit volume")
    fig_s = px.scatter(product_margin, x="Sales", y="Profit_Margin",
                       size="Profit", color="Product", hover_name="Product",
                       color_discrete_sequence=COLOR_SEQ, size_max=50)
    fig_s.update_layout(**plotly_futuristic_layout(height=420))
    st.plotly_chart(fig_s, width="stretch")

    chart_label("Monthly Profit Margin %")
    mm = (filtered_df.groupby(filtered_df["Order_Date"].dt.to_period("M"))
          .agg(Profit=("Profit", "sum"), Sales=("Sales", "sum")).reset_index())
    mm["Order_Date"] = mm["Order_Date"].astype(str)
    mm["Margin"] = (mm["Profit"] / mm["Sales"] * 100).fillna(0)
    fig_mm = px.line(mm, x="Order_Date", y="Margin", markers=True)
    fig_mm.update_layout(**plotly_futuristic_layout())
    fig_mm.update_traces(line=dict(color=COLORS["green"], width=2.5), marker=dict(color=COLORS["green"], size=7))
    st.plotly_chart(fig_mm, width="stretch")

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        section_header("Top 10 Products by Sales")
        tp = (filtered_df.groupby("Product")["Sales"].sum()
              .sort_values(ascending=False).head(10).reset_index())
        tp.columns = ["Product", "Total Sales"]
        tp["Total Sales"] = tp["Total Sales"].apply(format_currency)
        from utils.styles import df_table
        df_table(tp, show_index=False)

    with col2:
        section_header("Top 10 Products by Profit")
        tp2 = (filtered_df.groupby("Product")["Profit"].sum()
               .sort_values(ascending=False).head(10).reset_index())
        tp2.columns = ["Product", "Total Profit"]
        tp2["Total Profit"] = tp2["Total Profit"].apply(format_currency)
        from utils.styles import df_table
        df_table(tp2, show_index=False)

    chart_label("Regional Profit with Margin %", "Bar height = profit, label = margin")
    rb = (filtered_df.groupby("Region")
          .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index())
    rb["Margin"] = (rb["Profit"] / rb["Sales"] * 100).fillna(0).round(2)
    fig_rb = go.Figure(go.Bar(
        x=rb["Region"], y=rb["Profit"],
        marker=dict(color=COLOR_SEQ[:len(rb)]),
        text=rb["Margin"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
        textfont=dict(color=COLORS["cyan"], family="Inter", size=11),
    ))
    fig_rb.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_rb, width="stretch")

st.markdown("---")
section_header("Key Signals")
col1, col2 = st.columns(2)
with col1:
    insight("High-margin products aren't always the highest revenue drivers — the scatter view reveals strategic product mix opportunities.", label="Margin Signal", kind="positive")
    insight("Regions with strong sales but compressed margins point to pricing or cost structure issues worth addressing.", label="Region Signal", kind="warning")
with col2:
    insight("Monthly margin volatility suggests seasonal cost pressures. Locking in supplier terms during low-cost periods stabilises margins.", label="Trend Signal")
    insight("Online channel carries structurally higher margins due to lower distribution overhead — a strategic advantage worth protecting.", label="Channel Signal", kind="purple")

footer()
