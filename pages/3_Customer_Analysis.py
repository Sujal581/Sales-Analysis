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

page_header("Customer Analysis", "Segmentation, retention, behaviour & lifetime value", "👥")

total_customers = filtered_df["Customer_ID"].nunique()
customer_orders = filtered_df["Customer_ID"].value_counts()
repeat_customers = (customer_orders > 1).sum()
new_customers = total_customers - repeat_customers
retention_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
avg_orders = customer_orders.mean() if total_customers > 0 else 0
avg_revenue = (filtered_df["Sales"].sum() / total_customers) if total_customers > 0 else 0

col1, col2, col3 = st.columns(3)
kpi_card(col1, "Total Customers",   format_value(total_customers),  icon="👥", color=COLORS["cyan"])
kpi_card(col2, "Repeat Customers",  format_value(repeat_customers), icon="🔄", color=COLORS["green"])
kpi_card(col3, "New Customers",     format_value(new_customers),    icon="✨", color=COLORS["blue"])

col4, col5, col6 = st.columns(3)
kpi_card(col4, "Retention Rate",    f"{retention_rate:.1f}%",       icon="🎯", color=COLORS["purple"])
kpi_card(col5, "Avg Orders/Cust",   f"{avg_orders:.2f}",            icon="📦", color=COLORS["amber"])
kpi_card(col6, "Avg Revenue/Cust",  format_currency(avg_revenue),   icon="💰", color=COLORS["pink"])

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Top Customers", "Segmentation", "Behaviour"])

with tab1:
    top_customers = (filtered_df.groupby("Customer_ID")["Sales"].sum()
                     .sort_values(ascending=False).head(10).reset_index())
    repeat_df = (filtered_df.groupby("Customer_ID")["Order_ID"].nunique()
                 .sort_values(ascending=False).head(10).reset_index())

    col1, col2 = st.columns(2)
    with col1:
        section_header("Top 10 by Revenue")
        td = top_customers.copy()
        td["Sales"] = td["Sales"].apply(format_currency)
        td.columns = ["Customer ID", "Total Revenue"]
        df_table(td, show_index=False)

    with col2:
        section_header("Top 10 by Order Volume")
        rd = repeat_df.copy()
        rd.columns = ["Customer ID", "Order Count"]
        df_table(rd, show_index=False)

    chart_label("Top 10 Customers — Revenue Bar")
    fig1 = px.bar(top_customers.sort_values("Sales", ascending=True),
                  x="Sales", y="Customer_ID", orientation="h", color="Sales",
                  color_continuous_scale=["#1e3a5f", "#3B82F6", "#00F5FF"])
    fig1.update_layout(**plotly_futuristic_layout())
    st.plotly_chart(fig1, width="stretch")

with tab2:
    customer_spending = filtered_df.groupby("Customer_ID")["Sales"].sum().reset_index()
    num_bins = min(customer_spending["Sales"].nunique(), 4)
    labels = ["Low", "Medium", "High", "VIP"][:num_bins]
    customer_spending["Segment"] = pd.qcut(
        customer_spending["Sales"], q=num_bins, labels=labels, duplicates="drop"
    )
    seg_counts = customer_spending["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]

    col1, col2 = st.columns(2)
    with col1:
        chart_label("Customer Segments — Distribution")
        fig_seg = px.pie(seg_counts, values="Count", names="Segment", hole=0.45,
                         color_discrete_sequence=[COLORS["blue"], COLORS["cyan"], COLORS["purple"], COLORS["amber"]])
        fig_seg.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_seg, width="stretch")

    with col2:
        chart_label("Revenue by Customer Segment")
        seg_rev = customer_spending.groupby("Segment", observed=True)["Sales"].sum().reset_index()
        fig_sr = px.bar(seg_rev, x="Segment", y="Sales", color="Segment",
                        color_discrete_sequence=[COLORS["blue"], COLORS["cyan"], COLORS["purple"], COLORS["amber"]])
        fig_sr.update_layout(**plotly_futuristic_layout())
        st.plotly_chart(fig_sr, width="stretch")

    section_header("Segment Summary Table")
    seg_counts["Revenue Share"] = (seg_counts["Count"] / seg_counts["Count"].sum() * 100).round(2).astype(str) + "%"
    df_table(seg_counts, show_index=False)

with tab3:
    chart_label("Customer × Product Purchase Intensity", "Heat density of top 20 orders")
    cust_prod = (filtered_df.groupby(["Customer_ID", "Product"])["Sales"]
                 .sum().reset_index().sort_values("Sales", ascending=False).head(30))
    fig_heat = px.density_heatmap(cust_prod, x="Customer_ID", y="Product", z="Sales",
                                  color_continuous_scale=["#0d1117", "#3B82F6", "#00F5FF", "#8B5CF6"])
    fig_heat.update_layout(**plotly_futuristic_layout(height=420))
    st.plotly_chart(fig_heat, width="stretch")

    chart_label("Monthly Active Customers")
    mc = (filtered_df.groupby(filtered_df["Order_Date"].dt.to_period("M"))["Customer_ID"]
          .nunique().reset_index())
    mc.columns = ["Month", "Unique Customers"]
    mc["Month"] = mc["Month"].astype(str)
    fig_mc = px.area(mc, x="Month", y="Unique Customers")
    fig_mc.update_layout(**plotly_futuristic_layout())
    fig_mc.update_traces(line=dict(color=COLORS["purple"], width=2.5), fillcolor="rgba(139,92,246,0.07)")
    st.plotly_chart(fig_mc, width="stretch")

st.markdown("---")
section_header("Key Signals")
col1, col2 = st.columns(2)
with col1:
    insight(f"Retention rate of {retention_rate:.1f}% is solid. A formalised loyalty programme can push it higher and reduce acquisition costs.", label="Retention Signal", kind="positive" if retention_rate > 40 else "warning")
    insight("VIP and High segment customers drive disproportionate revenue — targeted account management has the highest ROI here.", label="Segment Signal", kind="purple")
with col2:
    insight(f"Average revenue per customer is {format_currency(avg_revenue)} across {avg_orders:.1f} orders. Cross-sell sequences can lift both metrics.", label="LTV Signal")
    insight("Customer × Product heatmap reveals untapped cross-sell corridors between frequent buyers and adjacent product categories.", label="Cross-sell Signal", kind="warning")

footer()
