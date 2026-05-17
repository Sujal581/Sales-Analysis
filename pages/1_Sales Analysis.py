import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Overview import clean
from config import df
from stles import apply_futuristic_style, insight, plotly_futuristic_layout

st.set_page_config(page_icon="📈", page_title="Sales Analysis",layout="wide")

apply_futuristic_style()

if df is not None:
    df = clean(df)
else:
    st.error("Failed to load data. Please check the data source.")

st.sidebar.title("Sales Analysis")

#-Filters----------------------------------------
defaults = {
    "region": "All",
    "product": "All",
    "sales_channel": "All",
    "payment_mode": "All",
    "state": "All"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

regions = (["All"] + sorted(df['Region'].dropna().unique().tolist()))
products = (["All"] + sorted(df['Product'].dropna().unique().tolist()))
sales_channels = (["All"] + sorted(df['Sales_Channel'].dropna().unique().tolist()))	
payment_modes = (["All"] + sorted(df['Payment_Mode'].dropna().unique().tolist()))
state = (["All"] + sorted(df['State'].dropna().unique().tolist()))

st.sidebar.selectbox("🗺️Select Region", regions, key="region")
st.sidebar.selectbox("📦Select Product", products, key="product")
st.sidebar.selectbox("🚚Select Sales Channel", sales_channels, key="sales_channel")
st.sidebar.selectbox("💳Select Payment Mode", payment_modes, key="payment_mode")
st.sidebar.selectbox("📍Select State", state, key="state")

filtered_df = df.copy()
if st.session_state.region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == st.session_state.region] 
if st.session_state.product != "All":
    filtered_df = filtered_df[filtered_df['Product'] == st.session_state.product]
if st.session_state.sales_channel != "All":
    filtered_df = filtered_df[filtered_df['Sales_Channel'] == st.session_state.sales_channel]       
if st.session_state.payment_mode != "All":
    filtered_df = filtered_df[filtered_df['Payment_Mode'] == st.session_state.payment_mode]
if st.session_state.state != "All":
    filtered_df = filtered_df[filtered_df['State'] == st.session_state.state]

#-Reset filters----------------------------------------
if "region" not in st.session_state:
    st.session_state.region = "All" 

if "product" not in st.session_state:
    st.session_state.product = "All"

if "sales_channel" not in st.session_state:
    st.session_state.sales_channel = "All"

if "payment_mode" not in st.session_state:
    st.session_state.payment_mode = "All"

if "state" not in st.session_state:
    st.session_state.state = "All"

if st.sidebar.button("Reset Filters"):

    for key in [
        "region",
        "product",
        "sales_channel",
        "payment_mode",
        "state",
    ]:
        del st.session_state[key]   
    st.rerun()

#-Calculations and Visualizations----------------------------------------
st.title("💸Sales Analysis Dashboard")

total_profit = filtered_df['Profit'].sum()
total_sales = filtered_df['Sales'].sum()
total_cost = filtered_df['Cost'].sum()
total_order = filtered_df['Order_ID'].nunique()
total_states = filtered_df['State'].nunique()
total_payment_modes = filtered_df['Payment_Mode'].nunique()
avg_profit_margin = filtered_df['Profit_Margin'].mean() * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Profit", f"${total_profit:,.2f}")
col2.metric("Total Sales", f"${total_sales:,.2f}")
col3.metric("Total Cost", f"${total_cost:,.2f}")

col4, col5, col6, col7 = st.columns(4)
col4.metric("Total Orders", f"{total_order}")
col5.metric("Total States", f"{total_states}")
col6.metric("Payment Modes", f"{total_payment_modes}")
col7.metric("Avg Profit Margin", f"{avg_profit_margin:.2f}%")

region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig1 = px.bar(region, x='Region', y='Sales', color='Region', color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3)
fig1.update_layout(**plotly_futuristic_layout("Sales by Region and Product"))

state_sales = filtered_df.groupby('State')['Sales'].sum().reset_index()
fig2 = px.bar(state_sales, x='State', y='Sales', color='State', color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3)   
fig2.update_layout(**plotly_futuristic_layout("Sales by State and Product"))

sales_channels = filtered_df.groupby('Sales_Channel')['Sales'].sum().reset_index()
fig3 = px.pie(sales_channels, values='Sales', names='Sales_Channel')
fig3.update_layout(**plotly_futuristic_layout("Sales by Sales Channel and Product"))    

payment_modes = filtered_df.groupby('Payment_Mode')['Sales'].sum().reset_index()
fig4 = px.pie(payment_modes, values='Sales', names='Payment_Mode', hole=0.5)
fig4.update_layout(**plotly_futuristic_layout("Sales by Payment Mode and Product"))


col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

#-Insights----------------------------------------
insight("The sales distribution across regions and states reveals that certain areas are outperforming others, indicating potential market opportunities. Analyzing the factors contributing to higher sales in these regions can help in replicating success strategies in underperforming areas.",
        label="Regional Sales Insight",
        kind="success")
insight("The preference for certain sales channels and payment modes can provide insights into customer behavior. For instance, if online sales are significantly higher than offline, it may indicate a shift towards digital purchasing, suggesting that investing in e-commerce platforms and digital marketing could further boost sales.", 
        label="Sales Channel and Payment Mode Insight",
        kind="success") 
insight("The payment mode analysis shows that certain payment methods are more popular among customers, which can inform decisions on which payment options to prioritize and promote. For example, if credit card payments are dominant, offering incentives for using this method could enhance customer satisfaction and increase sales.",
        label="Payment Mode Insight",
        kind="success")
insight("The average profit margin provides insight into the overall profitability of sales. A low profit margin may indicate the need to review pricing strategies, reduce costs, or focus on higher-margin products to improve profitability.",
        label="Profit Margin Insight",
        kind="success")
