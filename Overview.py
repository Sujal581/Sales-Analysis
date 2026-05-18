import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

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

page_header("System Overview", "High-level sales performance summary across all dimensions", "📡")

total_profit = filtered_df["Profit"].sum()
avg_profit_margin = filtered_df["Profit_Margin"].mean() * 100
total_sales = filtered_df["Sales"].sum()
total_cost = filtered_df["Cost"].sum()
total_order = filtered_df["Order_ID"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)
kpi_card(col1, "Total Sales",        format_currency(total_sales),  icon="💰", color=COLORS["cyan"])
kpi_card(col2, "Total Profit",       format_currency(total_profit), icon="📈", color=COLORS["green"])
kpi_card(col3, "Profit Margin",      f"{avg_profit_margin:.1f}%",   icon="🎯", color=COLORS["purple"])
kpi_card(col4, "Total Cost",         format_currency(total_cost),   icon="💸", color=COLORS["amber"])
kpi_card(col5, "Total Orders",       format_value(total_order),     icon="📦", color=COLORS["blue"])

st.markdown("---")
section_header("Monthly Sales Trend")

sales_monthly = (
    filtered_df.groupby(filtered_df["Order_Date"].dt.to_period("M"))["Sales"]
    .sum().reset_index()
)
sales_monthly["Order_Date"] = sales_monthly["Order_Date"].astype(str)
fig1 = px.area(sales_monthly, x="Order_Date", y="Sales")
fig1.update_layout(**plotly_futuristic_layout("Monthly Sales Trend"))
fig1.update_traces(line=dict(color=COLORS["cyan"], width=2.5), fillcolor="rgba(0,245,255,0.06)")
st.plotly_chart(fig1, width="stretch")

section_header("Breakdown Views")
col1, col2 = st.columns(2)
with col1:
    region = filtered_df.groupby("Region")["Sales"].sum().reset_index()
    chart_label("Sales by Region")
    fig2 = px.pie(region, values="Sales", names="Region",
                  color_discrete_sequence=COLOR_SEQ)
    fig2.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig2, width="stretch")

    sales_channel = filtered_df.groupby("Sales_Channel")["Sales"].sum().reset_index()
    chart_label("Sales by Channel")
    fig4 = px.bar(sales_channel, x="Sales_Channel", y="Sales", color="Sales_Channel",
                  color_discrete_sequence=COLOR_SEQ)
    fig4.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig4, width="stretch")

with col2:
    product = (filtered_df.groupby("Product")["Sales"].sum()
               .reset_index().sort_values("Sales", ascending=False))
    chart_label("Sales by Product")
    fig3 = px.bar(product, x="Product", y="Sales", color="Sales",
                  color_continuous_scale=["#0066ff", "#00F5FF", "#8B5CF6"])
    fig3.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig3, width="stretch")

    payment_mode = filtered_df.groupby("Payment_Mode")["Sales"].sum().reset_index()
    chart_label("Sales by Payment Mode")
    fig5 = px.pie(payment_mode, values="Sales", names="Payment_Mode", hole=0.5,
                  color_discrete_sequence=COLOR_SEQ)
    fig5.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig5, width="stretch")

st.markdown("---")
section_header("Key Signals")
col1, col2 = st.columns(2)
with col1:
    insight("Online channel dominates revenue — digital purchasing preference is clear. Increasing digital marketing spend could yield outsized returns.", label="Channel Signal", kind="positive")
    insight("The East region leads in total sales volume. Replicating the regional strategy in underperforming zones is a high-leverage opportunity.", label="Regional Signal")
with col2:
    insight("Credit card is the dominant payment mode. Payment-linked promotions can amplify conversion rates.", label="Payment Signal", kind="warning")
    insight("Office Chair drives the highest product revenue. Bundling accessories could unlock adjacent demand.", label="Product Signal", kind="purple")

footer()
