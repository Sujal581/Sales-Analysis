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

df['Return_Status'] = (
    df['Return_Status']
    .astype(str)
    .str.strip()
    .str.replace("Unkown Status", "Unknown Status")
)

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

#-Calculate metrics----------------------------------------
st.title("📈 Return Analysis")

total_returns = filtered_df[filtered_df['Return_Status'] == 'Yes'].shape[0]
total_unknown_returns = filtered_df[filtered_df['Return_Status'] == 'Unknown Status'].shape[0]
total_damaged_return = filtered_df[filtered_df['Return_Status'] == 'Damaged'].shape[0]
total_not_damaged_returns = filtered_df[filtered_df['Return_Status'] == 'No'].shape[0]
return_rate = (total_returns / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Returns", f"{total_returns}")
col2.metric("Return Rate", f"{return_rate:.2f}%")
col3.metric("Unknown Returns", f"{total_unknown_returns}")
col4.metric("Damaged Returns", f"{total_damaged_return}")
col5.metric("Non-Damaged Returns", f"{total_not_damaged_returns}")

fig1 = px.pie(filtered_df,names='Return_Status',title='Return Status Distribution',color_discrete_sequence=px.colors.qualitative.Plotly)
fig1.update_layout(**plotly_futuristic_layout("Return Status Distribution"))


fig2 = px.bar(filtered_df.groupby('Product')['Return_Status'].value_counts().unstack().fillna(0).reset_index(),x='Product',y='Yes',
    title='Returns by Product',
    color='Product',
    color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3
)
fig2.update_layout(**plotly_futuristic_layout("Returns by Product"))


fig3 = px.bar(filtered_df.groupby('Region')['Return_Status'].value_counts().unstack().fillna(0).reset_index(),x='Region',y='Yes',
    title='Returns by Region',  
    color='Region',
    color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3
)
fig3.update_layout(**plotly_futuristic_layout("Returns by Region")) 

fig4 = px.line(filtered_df.groupby([filtered_df['Order_Date'].dt.to_period('M'), 'Return_Status']).size().reset_index(name='Count').assign(Order_Date=lambda x: x['Order_Date'].astype(str)), x='Order_Date', y='Count', color='Return_Status', title='Returns Over Time', markers=True, color_discrete_sequence=px.colors.qualitative.Vivid)
fig4.update_layout(**plotly_futuristic_layout("Returns Over Time"))

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

#-Insights----------------------------------------
insight("The overall return rate is {:.2f}%, with {} total returns.".format(return_rate, total_returns))
insight(
    "The distribution of return statuses shows that {:.2f}% of orders have unknown return reasons and {:.2f}% are marked as damaged.".format(
        (total_unknown_returns / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0,
        (total_damaged_return / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    )
)

insight("Certain products and regions have higher return rates, indicating potential quality or customer satisfaction issues that need to be addressed.")
insight("The trend of returns over time can help identify seasonal patterns or the impact of specific events on return rates, allowing for proactive measures to reduce returns during peak periods.")
insight("Analyzing the reasons for returns, especially for products with high return rates, can provide valuable insights into product quality, customer expectations, and areas for improvement in the sales process.", kind="warning")
