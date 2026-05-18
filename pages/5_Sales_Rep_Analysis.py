import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

page_header("Sales Rep Intelligence", "Leaderboard, product mix, efficiency matrix & trend", "🏆")

total_reps      = filtered_df["Sales_Rep"].nunique()
top_rep         = filtered_df.groupby("Sales_Rep")["Sales"].sum().idxmax() if not filtered_df.empty else "N/A"
top_rep_sales   = filtered_df.groupby("Sales_Rep")["Sales"].sum().max()   if not filtered_df.empty else 0
avg_rep_sales   = filtered_df.groupby("Sales_Rep")["Sales"].sum().mean()  if not filtered_df.empty else 0
top_rep_orders  = filtered_df.groupby("Sales_Rep")["Order_ID"].nunique().max() if not filtered_df.empty else 0

col1, col2, col3, col4 = st.columns(4)
kpi_card(col1, "Active Reps",      str(total_reps),                icon="👤", color=COLORS["cyan"])
kpi_card(col2, "Top Performer",    top_rep,                        icon="🏆", color=COLORS["amber"])
kpi_card(col3, "Top Rep Sales",    format_currency(top_rep_sales), icon="💰", color=COLORS["green"])
kpi_card(col4, "Avg Rep Sales",    format_currency(avg_rep_sales), icon="📊", color=COLORS["blue"])

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Performance Board", "Product & Region Mix", "Efficiency"])

with tab1:
    rep_summary = (
        filtered_df.groupby("Sales_Rep")
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"),
             Orders=("Order_ID", "nunique"), Avg_Margin=("Profit_Margin", "mean"))
        .reset_index()
    )
    rep_summary["Avg_Margin"] = (rep_summary["Avg_Margin"] * 100).round(2)
    rep_summary = rep_summary.sort_values("Total_Sales", ascending=False)

    chart_label("Revenue vs Profit (Color) by Rep", "Bar height = revenue, color = profit")
    fig_rep = px.bar(rep_summary, x="Sales_Rep", y="Total_Sales", color="Total_Profit",
                     color_continuous_scale=["#EF4444", "#3B82F6", "#10B981"],
                     text="Orders")
    fig_rep.update_layout(**plotly_futuristic_layout())
    fig_rep.update_traces(textposition="outside", textfont=dict(color=COLORS["cyan"], family="Inter", size=11))
    st.plotly_chart(fig_rep, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        chart_label("Orders per Rep")
        fig_o = px.bar(rep_summary, x="Sales_Rep", y="Orders", color="Sales_Rep",
                       color_discrete_sequence=COLOR_SEQ)
        fig_o.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_o, width="stretch")

    with col2:
        chart_label("Avg Profit Margin % by Rep")
        fig_m = px.bar(rep_summary, x="Sales_Rep", y="Avg_Margin", color="Avg_Margin",
                       color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"])
        fig_m.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_m, width="stretch")

    section_header("Performance Leaderboard")
    lb = rep_summary.copy()
    lb["Total_Sales"]   = lb["Total_Sales"].apply(format_currency)
    lb["Total_Profit"]  = lb["Total_Profit"].apply(format_currency)
    lb.columns = ["Sales Rep", "Total Sales", "Total Profit", "Orders", "Avg Margin %"]
    df_table(lb, show_index=False)

with tab2:
    chart_label("Sales Rep × Product Mix", "Stacked by product")
    rp = filtered_df.groupby(["Sales_Rep", "Product"])["Sales"].sum().reset_index()
    fig_rp = px.bar(rp, x="Sales_Rep", y="Sales", color="Product",
                    barmode="stack", color_discrete_sequence=COLOR_SEQ)
    fig_rp.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_rp, width="stretch")

    chart_label("Sales Rep × Region Performance", "Grouped by region")
    rr = filtered_df.groupby(["Sales_Rep", "Region"])["Sales"].sum().reset_index()
    fig_rr = px.bar(rr, x="Sales_Rep", y="Sales", color="Region",
                    barmode="group", color_discrete_sequence=COLOR_SEQ)
    fig_rr.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_rr, width="stretch")

with tab3:
    rep_eff = (
        filtered_df.groupby("Sales_Rep")
        .agg(Sales=("Sales", "sum"), Orders=("Order_ID", "nunique"), Profit=("Profit", "sum"))
        .reset_index()
    )
    rep_eff["Revenue_per_Order"] = rep_eff["Sales"]  / rep_eff["Orders"]
    rep_eff["Profit_per_Order"]  = rep_eff["Profit"] / rep_eff["Orders"]

    chart_label("Revenue per Order vs Profit per Order", "Bubble size = total order volume")
    fig_eff = px.scatter(rep_eff, x="Revenue_per_Order", y="Profit_per_Order",
                         size="Orders", color="Sales_Rep", text="Sales_Rep",
                         color_discrete_sequence=COLOR_SEQ, size_max=50)
    fig_eff.update_traces(textposition="top center",
                          textfont=dict(color=COLORS["cyan"], family="Inter", size=10))
    fig_eff.update_layout(**plotly_futuristic_layout(height=420))
    st.plotly_chart(fig_eff, width="stretch")

    chart_label("Monthly Sales Trend by Rep")
    monthly_rep = (
        filtered_df.groupby([filtered_df["Order_Date"].dt.to_period("M"), "Sales_Rep"])["Sales"]
        .sum().reset_index()
    )
    monthly_rep["Order_Date"] = monthly_rep["Order_Date"].astype(str)
    fig_trend = px.line(monthly_rep, x="Order_Date", y="Sales", color="Sales_Rep",
                        markers=True, color_discrete_sequence=COLOR_SEQ)
    fig_trend.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_trend, width="stretch")

st.markdown("---")
section_header("Key Signals")
col1, col2 = st.columns(2)
with col1:
    insight(f"{top_rep} leads with {format_currency(top_rep_sales)}. Studying their product mix and region focus surfaces best practices for the broader team.", label="Top Performer", kind="positive")
    insight("Reps with high revenue but low margin may be over-discounting to close deals. A margin floor policy protects profitability.", label="Margin Risk", kind="warning")
with col2:
    insight("Revenue per order vs profit per order reveals deal quality — volume alone doesn't tell the full story.", label="Efficiency Signal")
    insight("Product mix concentration by rep suggests specialisation is emerging. Structured cross-training reduces single-product dependency.", label="Mix Signal", kind="purple")

footer()
