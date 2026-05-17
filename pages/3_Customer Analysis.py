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

#-Calculation and visualizations will go here----------------------------------------
st.title("👨Customer Analysis")

# Total unique customers
total_customers = filtered_df['Customer_ID'].nunique()


customer_orders = filtered_df['Customer_ID'].value_counts()
repeat_customers = (customer_orders > 1).sum()
new_customers = total_customers - repeat_customers
customer_retention_rate = (repeat_customers / total_customers) * 100 if total_customers > 0 else 0
repeat_customers_rate = (repeat_customers / total_customers) * 100 if total_customers > 0 else 0
avg_orders_per_customer = customer_orders.mean() if total_customers > 0 else 0  

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", total_customers)
col2.metric("Repeat Customers", repeat_customers)
col3.metric("New Customers", new_customers)

col1, col2, col3 = st.columns(3)
col1.metric("Customer Retention Rate", f"{customer_retention_rate:.2f}%")
col2.metric("Repeat Customers Rate", f"{repeat_customers_rate:.2f}%")
col3.metric("Avg Orders per Customer", f"{avg_orders_per_customer:.2f}")

top_customers = filtered_df.groupby('Customer_ID')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
repeat_customers_df= filtered_df.groupby('Customer_ID')['Order_ID'].nunique().sort_values(ascending=False).head(10).reset_index()
customer_segmentation = filtered_df.groupby('Customer_ID')['Sales'].sum().reset_index()
num_bins = min(customer_segmentation['Sales'].nunique(), 4)

labels = ['Low', 'Medium', 'High', 'VIP'][:num_bins]

customer_segmentation['Segment'] = pd.qcut(
    customer_segmentation['Sales'],
    q=num_bins,
    labels=labels,
    duplicates='drop'
)
customer_spending = filtered_df.groupby('Customer_ID')['Sales'].sum().reset_index()

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Top 10 Customers by Sales")
    df_table(top_customers, "Top 10 Customers by Sales")
with col2:
    st.markdown("### Top 10 Repeat Customers")
    df_table(repeat_customers_df, "Top 10 Customers by Number of Orders")

st.markdown("### Customer Segmentation")
df_table(customer_segmentation['Segment'].value_counts().reset_index().rename(columns={'index': 'Segment', 'Segment': 'Count'}), "Customer Segmentation")


fig1 = px.bar(customer_spending.sort_values('Sales', ascending=False).head(10), x='Customer_ID', y='Sales', title="Top 10 Customers by Sales", color='Customer_ID', color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3)
fig1.update_layout(**plotly_futuristic_layout("Top 10 Customers by Sales"))


fig2 = px.bar(repeat_customers_df.sort_values('Order_ID', ascending=False).head(10), x='Customer_ID', y='Order_ID', title="Top 10 Repeat Customers", color='Customer_ID', color_discrete_sequence=px.colors.qualitative.Set2 + px.colors.qualitative.Set3)
fig2.update_layout(**plotly_futuristic_layout("Top 10 Repeat Customers"))

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.pie(
    customer_segmentation['Segment']
    .value_counts()
    .reset_index(),

    values='count',
    names='Segment',

    title="Customer Segmentation",

    color_discrete_sequence=px.colors.qualitative.Vivid
)
fig3.update_layout(**plotly_futuristic_layout("Customer Segmentation"))
st.plotly_chart(fig3, use_container_width=True)


#-Insights----------------------------------------
insight(f"The top customers by sales and repeat purchases highlight key segments of the customer base that are driving significant revenue. Focusing on these customers with personalized marketing and loyalty programs could further enhance retention and increase sales.",
        label="Top Customers Insight",
        kind="success")
insight(f"The customer retention rate is {customer_retention_rate:.2f}%, indicating that a significant portion of customers are returning for repeat purchases. This suggests strong customer loyalty and satisfaction.",
        label="Customer Retention Insight",
        kind="success")
insight(f"The average number of orders per customer is {avg_orders_per_customer:.2f}, which indicates that on average, customers are making multiple purchases. This could be a sign of effective marketing strategies and product appeal.",
        label="Customer Engagement Insight",    
        kind="success")
insight(f"The customer segmentation analysis reveals distinct groups based on spending patterns. Identifying and targeting these segments with tailored marketing strategies can enhance customer engagement and drive sales growth.",
        label="Customer Segmentation Insight",
        kind="warning")
insight(f"By analyzing the top customers and their purchasing behavior, we can identify opportunities for upselling and cross-selling, which can further increase revenue and strengthen customer relationships.",
        label="Upselling and Cross-selling Insight",    
        kind="info")

