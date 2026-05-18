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

page_header("Product Intelligence", "Portfolio treemap, pricing trends, discount vs margin, regional mix", "📦")

total_products   = filtered_df["Product"].nunique()
top_product      = filtered_df.groupby("Product")["Sales"].sum().idxmax() if not filtered_df.empty else "N/A"
top_prod_sales   = filtered_df.groupby("Product")["Sales"].sum().max()    if not filtered_df.empty else 0
avg_unit_price   = filtered_df["Unit_Price"].mean()                        if not filtered_df.empty else 0
avg_discount_pct = filtered_df["Discount"].mean() * 100                   if not filtered_df.empty else 0

col1, col2, col3, col4, col5 = st.columns(5)
kpi_card(col1, "Total Products",    str(total_products),              icon="📦", color=COLORS["cyan"])
kpi_card(col2, "Top Product",       top_product,                      icon="⭐", color=COLORS["amber"])
kpi_card(col3, "Top Product Sales", format_currency(top_prod_sales),  icon="💰", color=COLORS["green"])
kpi_card(col4, "Avg Unit Price",    format_currency(avg_unit_price),  icon="🏷️", color=COLORS["blue"])
kpi_card(col5, "Avg Discount",      f"{avg_discount_pct:.1f}%",       icon="🎁", color=COLORS["purple"])

st.markdown("---")

product_summary = (
    filtered_df.groupby("Product")
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
         Units=("Units", "sum"), Orders=("Order_ID", "nunique"),
         Avg_Price=("Unit_Price", "mean"), Avg_Discount=("Discount", "mean"))
    .reset_index()
)
product_summary["Margin_Pct"]    = (product_summary["Profit"] / product_summary["Sales"] * 100).fillna(0).round(2)
product_summary["Avg_Discount"]  = (product_summary["Avg_Discount"] * 100).round(1)
product_summary = product_summary.sort_values("Sales", ascending=False)

tab1, tab2, tab3, tab4 = st.tabs(["Portfolio Overview", "Pricing & Discount", "Regional Mix", "Performance Matrix"])

with tab1:
    chart_label("Product Portfolio Treemap", "Area = revenue, colour = margin %")
    fig_tree = px.treemap(product_summary, path=["Product"], values="Sales",
                          color="Margin_Pct",
                          color_continuous_scale=["#EF4444", "#3B82F6", "#10B981"])
    fig_tree.update_layout(**plotly_futuristic_layout(height=420))
    st.plotly_chart(fig_tree, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        chart_label("Product Revenue")
        fig_s = px.bar(product_summary, x="Product", y="Sales", color="Sales",
                       color_continuous_scale=["#1e3a5f", "#3B82F6", "#00F5FF"])
        fig_s.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_s, width="stretch")

    with col2:
        chart_label("Units Sold by Product")
        fig_u = px.bar(product_summary, x="Product", y="Units", color="Units",
                       color_continuous_scale=["#1e3a5f", "#10B981", "#F59E0B"])
        fig_u.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_u, width="stretch")

with tab2:
    chart_label("Avg Discount % vs Profit Margin", "Bubble = revenue volume")
    fig_disc = px.scatter(product_summary, x="Avg_Discount", y="Margin_Pct", size="Sales",
                          color="Product", text="Product",
                          color_discrete_sequence=COLOR_SEQ, size_max=50)
    fig_disc.update_traces(textposition="top center",
                           textfont=dict(color=COLORS["cyan"], family="Inter", size=9))
    fig_disc.update_layout(**plotly_futuristic_layout(height=420))
    st.plotly_chart(fig_disc, width="stretch")

    top5 = product_summary.head(5)["Product"].tolist()
    price_trend = (
        filtered_df.groupby([filtered_df["Order_Date"].dt.to_period("M"), "Product"])["Unit_Price"]
        .mean().reset_index()
    )
    price_trend["Order_Date"] = price_trend["Order_Date"].astype(str)
    chart_label("Price Trend — Top 5 Products")
    fig_pt = px.line(price_trend[price_trend["Product"].isin(top5)],
                     x="Order_Date", y="Unit_Price", color="Product", markers=True,
                     color_discrete_sequence=COLOR_SEQ)
    fig_pt.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_pt, width="stretch")

with tab3:
    chart_label("Product Sales by Region", "Stacked bar")
    prod_region = filtered_df.groupby(["Product", "Region"])["Sales"].sum().reset_index()
    fig_pr = px.bar(prod_region, x="Product", y="Sales", color="Region",
                    barmode="stack", color_discrete_sequence=COLOR_SEQ)
    fig_pr.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_pr, width="stretch")

    chart_label("Region → Product Revenue Hierarchy", "Sunburst drill-down")
    fig_sun = px.sunburst(prod_region, path=["Region", "Product"], values="Sales",
                          color="Sales", color_continuous_scale=["#0d1117", "#3B82F6", "#00F5FF"])
    fig_sun.update_layout(**plotly_futuristic_layout(height=450))
    st.plotly_chart(fig_sun, width="stretch")

with tab4:
    section_header("Full Product Performance Matrix")
    matrix = product_summary.copy()
    matrix["Sales"]      = matrix["Sales"].apply(format_currency)
    matrix["Profit"]     = matrix["Profit"].apply(format_currency)
    matrix["Avg_Price"]  = matrix["Avg_Price"].apply(format_currency)
    matrix.columns = ["Product", "Sales", "Profit", "Units", "Orders", "Avg Price", "Avg Disc %", "Margin %"]
    df_table(matrix, show_index=False)

    chart_label("Monthly Revenue — Top 5 Products")
    monthly_prod = (
        filtered_df.groupby([filtered_df["Order_Date"].dt.to_period("M"), "Product"])["Sales"]
        .sum().reset_index()
    )
    monthly_prod["Order_Date"] = monthly_prod["Order_Date"].astype(str)
    fig_mp = px.line(monthly_prod[monthly_prod["Product"].isin(top5)],
                     x="Order_Date", y="Sales", color="Product", markers=True,
                     color_discrete_sequence=COLOR_SEQ)
    fig_mp.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_mp, width="stretch")

st.markdown("---")
section_header("Key Signals")
col1, col2 = st.columns(2)
with col1:
    insight(f"{top_product} leads the portfolio. Adjacency analysis reveals which products customers buy alongside it — prime bundle candidates.", label="Portfolio Signal", kind="positive")
    insight("The discount vs margin scatter highlights products where heavy discounting erodes profitability without proportionate volume gains.", label="Discount Risk", kind="error")
with col2:
    insight("Regional product mix varies significantly. Localised strategies in high-performing regions can be used as a playbook for expansion.", label="Regional Signal")
    insight("Price trend stability across top products signals strong brand value. Any downward drift should trigger a pricing review.", label="Pricing Signal", kind="warning")

footer()
