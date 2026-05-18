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

page_header("Sales Analysis", "Geographic, channel & temporal sales breakdown", "💸")

total_sales  = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_cost   = filtered_df["Cost"].sum()
total_order  = filtered_df["Order_ID"].nunique()
total_states = filtered_df["State"].nunique()
avg_margin   = filtered_df["Profit_Margin"].mean() * 100

col1, col2, col3 = st.columns(3)
kpi_card(col1, "Total Sales",   format_currency(total_sales),  icon="💰", color=COLORS["cyan"])
kpi_card(col2, "Total Profit",  format_currency(total_profit), icon="📈", color=COLORS["green"])
kpi_card(col3, "Total Cost",    format_currency(total_cost),   icon="💸", color=COLORS["amber"])

col4, col5, col6 = st.columns(3)
kpi_card(col4, "Total Orders",  format_value(total_order),     icon="📦", color=COLORS["blue"])
kpi_card(col5, "States Covered", str(total_states),             icon="🗺️", color=COLORS["purple"])
kpi_card(col6, "Avg Margin",    f"{avg_margin:.1f}%",           icon="🎯", color=COLORS["pink"])

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Geographic", "Channel & Payment", "Trend Analysis"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        chart_label("Sales by Region", "Total revenue per region")
        region = (filtered_df.groupby("Region")["Sales"].sum()
                  .reset_index().sort_values("Sales", ascending=True))
        fig1 = px.bar(region, x="Sales", y="Region", orientation="h", color="Sales",
                      color_continuous_scale=["#1e3a5f", "#3B82F6", "#00F5FF"])
        fig1.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig1, width="stretch")

    with col2:
        chart_label("Top 10 States", "Highest revenue states")
        state_sales = (filtered_df.groupby("State")["Sales"].sum()
                       .reset_index().sort_values("Sales", ascending=False).head(10))
        fig2 = px.bar(state_sales, x="State", y="Sales", color="Sales",
                      color_continuous_scale=["#1e3a5f", "#8B5CF6", "#00F5FF"])
        fig2.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig2, width="stretch")

    chart_label("Region → Product Breakdown", "Sunburst drill-down")
    region_product = filtered_df.groupby(["Region", "Product"])["Sales"].sum().reset_index()
    fig_rp = px.sunburst(region_product, path=["Region", "Product"], values="Sales",
                         color="Sales", color_continuous_scale=["#0d1117", "#3B82F6", "#00F5FF"])
    fig_rp.update_layout(**plotly_futuristic_layout(height=450))
    st.plotly_chart(fig_rp, width="stretch")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        chart_label("Sales by Channel")
        sales_channels = filtered_df.groupby("Sales_Channel")["Sales"].sum().reset_index()
        fig3 = px.pie(sales_channels, values="Sales", names="Sales_Channel",
                      color_discrete_sequence=COLOR_SEQ)
        fig3.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig3, width="stretch")

    with col2:
        chart_label("Sales by Payment Mode")
        payment_modes = filtered_df.groupby("Payment_Mode")["Sales"].sum().reset_index()
        fig4 = px.pie(payment_modes, values="Sales", names="Payment_Mode", hole=0.5,
                      color_discrete_sequence=COLOR_SEQ)
        fig4.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig4, width="stretch")

    chart_label("Channel × Payment Mode Mix", "Grouped bar comparison")
    channel_payment = (filtered_df.groupby(["Sales_Channel", "Payment_Mode"])["Sales"]
                       .sum().reset_index())
    fig_cp = px.bar(channel_payment, x="Sales_Channel", y="Sales", color="Payment_Mode",
                    barmode="group", color_discrete_sequence=COLOR_SEQ)
    fig_cp.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_cp, width="stretch")

with tab3:
    chart_label("Monthly Sales Area", "Revenue over time")
    monthly = (filtered_df.groupby(filtered_df["Order_Date"].dt.to_period("M"))["Sales"]
               .sum().reset_index())
    monthly["Order_Date"] = monthly["Order_Date"].astype(str)
    fig_m = px.area(monthly, x="Order_Date", y="Sales")
    fig_m.update_layout(**plotly_futuristic_layout())
    fig_m.update_traces(line=dict(color=COLORS["cyan"], width=2.5), fillcolor="rgba(0,245,255,0.06)")
    st.plotly_chart(fig_m, width="stretch")

    chart_label("Quarterly Performance", "Sales by year and quarter")
    quarterly = filtered_df.groupby(["Year", "Quarter"])["Sales"].sum().reset_index()
    quarterly["Period"] = quarterly["Year"].astype(str) + " " + quarterly["Quarter"]
    fig_q = px.bar(quarterly, x="Period", y="Sales", color="Quarter",
                   color_discrete_sequence=COLOR_SEQ)
    fig_q.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig_q, width="stretch")

st.markdown("---")
section_header("Key Signals")
col1, col2 = st.columns(2)
with col1:
    insight("Regional concentration in East signals opportunity to expand west and south with targeted campaigns.", label="Geographic Signal", kind="positive")
    insight("Digital channels are consistently outperforming offline — sustained shift in buyer behaviour.", label="Channel Signal")
with col2:
    insight("Credit card and UPI lead payments. Channel-specific promotions on dominant modes reduce checkout friction.", label="Payment Signal", kind="warning")
    insight("Quarterly trend patterns reveal seasonal peaks useful for demand planning and inventory positioning.", label="Trend Signal", kind="purple")

footer()
