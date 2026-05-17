import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Overview import clean
from config import df
from stles import apply_futuristic_style, df_table, insight, plotly_futuristic_layout

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


#-Calculate profit and insights----------------------------------------
st.title("📈 Profit Analysis")

filtered_df['Profit'] = filtered_df['Sales'] - filtered_df['Cost']

total_profit = filtered_df['Profit'].sum()
total_sales = filtered_df['Sales'].sum()
total_cost = filtered_df['Cost'].sum()
total_order = filtered_df['Order_ID'].nunique()
total_payment_modes = filtered_df['Payment_Mode'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Profit", f"${total_profit:,.2f}")    
col2.metric("Total Sales", f"${total_sales:,.2f}")
col3.metric("Total Cost", f"${total_cost:,.2f}")

col4, col5 = st.columns(2)
col4.metric("Total Orders", f"{total_order:,}")
col5.metric("Payment Modes", f"{total_payment_modes}")


fig1 = px.line(filtered_df.groupby('Region')['Profit'].sum().reset_index(), x='Region', y='Profit', title="Profit by Region")
fig1.update_layout(**plotly_futuristic_layout("Profit by Region"))    


fig2 = px.bar(filtered_df.groupby('Product')['Profit'].sum().reset_index(), x='Product', y='Profit', title="Profit by Product", color='Product', color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3)
fig2.update_layout(**plotly_futuristic_layout("Profit by Product"))

fig3 = px.bar(filtered_df.groupby('Sales_Channel')['Profit'].sum().reset_index(), x='Sales_Channel', y='Profit', title="Profit by Sales Channel", color='Sales_Channel', color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3)
fig3.update_layout(**plotly_futuristic_layout("Profit by Sales Channel"))


fig4 = px.bar(filtered_df.groupby('Payment_Mode')['Profit'].sum().reset_index(), x='Payment_Mode', y='Profit', title="Profit by Payment Mode", color='Payment_Mode', color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3)
fig4.update_layout(**plotly_futuristic_layout("Profit by Payment Mode"))


col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)


st.markdown("### Top 10 Product")
top_product = (filtered_df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10).reset_index())
df_table(top_product.rename(columns={'Sales': 'Total Sales'}))


insight("The profit analysis reveals that certain regions and products are significantly more profitable than others. By focusing on these high-performing areas, we can optimize our sales strategy and maximize overall profitability.",
        label="Profit Analysis Insight",
        kind="success")
insight("The sales channels and payment modes that contribute the most to profit can be identified, allowing us to allocate resources more effectively and enhance customer experience in those areas.",
        label="Sales Channel and Payment Mode Insight",
        kind="success")
insight("The top-performing products in terms of sales can be further analyzed to understand customer preferences and market trends, enabling us to tailor our product offerings and marketing strategies accordingly.",
        label="Top Product Insight",
        kind="success")
