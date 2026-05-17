import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from config import df
from stles import apply_futuristic_style, insight, plotly_futuristic_layout

st.set_page_config(page_icon="📈", page_title="Sales Analysis",layout="wide")

apply_futuristic_style()

def clean(df):
	df = df.copy()
	df.drop_duplicates(inplace=True)
	df.columns = (df.columns
		    .str.strip()
		    .str.replace(" ","_")
	)
	df['Sales_Channel']= df['Sales_Channel'].str.replace(" ","")
	df['Order_Date']=pd.to_datetime(df['Order_Date'],errors='coerce')

	numeric_cols=['Units','Unit_Price','Discount','Sales','Cost','Profit']
	
	categorical_cols = ['Customer_Name','Region','State','Product','Sales_Channel','Payment_Mode','Sales_Rep','Return_Status']
	
	for col in numeric_cols:
		df[col]=df[col].fillna(df[col].median())
	for col in categorical_cols:    
		df[col]=df[col].fillna(df[col].mode()[0])
    
	text_col = categorical_cols
	for col in text_col:
		df[col] = (df[col]
			.str.strip()
			.str.title()
			.astype(str)
		)

	df['Profit_Margin'] = np.where(df['Sales'] != 0, df['Profit'] / df['Sales'], 0)
	df['Year'] = df['Order_Date'].dt.year
	df['Month'] = df['Order_Date'].dt.month_name()

	df.reset_index(drop=True, inplace=True)
	return df

def format_value(num):

    if num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"

    elif num >= 1_000:
        return f"{num/1_000:.2f}K"

    return str(num)

def format_currency(num):

    if num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"

    elif num >= 1_000:
        return f"${num/1_000:.2f}K"

    return f"${num:.2f}"


df = clean(df)

st.sidebar.title("📊 Sales Analysis")

#-Filters----------------------------------------
defaults = {
    "region": "All",
    "product": "All",
    "sales_channel": "All",
    "sales_rep": "All",
    "payment_mode": "All",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
        
regions = (["All"] + sorted(df['Region'].dropna().unique().tolist()))
products = (["All"] + sorted(df['Product'].dropna().unique().tolist()))
sales_channels = (["All"] + sorted(df['Sales_Channel'].dropna().unique().tolist()))	
sales_rep = (["All"] + sorted(df['Sales_Rep'].dropna().unique().tolist()))

st.sidebar.selectbox("🗺️Select Region",regions, key="region")
st.sidebar.selectbox("📦Select Product",products, key="product")
st.sidebar.selectbox("🚚Select Sales Channel",sales_channels, key="sales_channel")
st.sidebar.selectbox("📊Select Sales Rep",sales_rep, key="sales_rep")
st.sidebar.selectbox("💳Select Payment Mode",["All"] + sorted(df['Payment_Mode'].dropna().unique().tolist()), key="payment_mode")

filtered_df = df.copy()
if st.session_state.region != "All":
	filtered_df = filtered_df[filtered_df['Region'] == st.session_state.region]
if st.session_state.product != "All":
	filtered_df =filtered_df[filtered_df['Product'] == st.session_state.product]
if st.session_state.sales_channel != "All":
	filtered_df = filtered_df[filtered_df['Sales_Channel'] == st.session_state.sales_channel]
if st.session_state.sales_rep != "All":
	filtered_df = filtered_df[filtered_df['Sales_Rep'] == st.session_state.sales_rep]
if st.session_state.payment_mode != "All":
	filtered_df = filtered_df[filtered_df['Payment_Mode'] == st.session_state.payment_mode]
if "region" not in st.session_state:
    st.session_state.region = "All"

#-Reset filters----------------------------------------
if "product" not in st.session_state:
    st.session_state.product = "All"

if "sales_channel" not in st.session_state:
    st.session_state.sales_channel = "All"

if "sales_rep" not in st.session_state:
    st.session_state.sales_rep = "All"

if "payment_mode" not in st.session_state:
    st.session_state.payment_mode = "All"


if st.sidebar.button("Reset Filters"):

    for key in [
        "region",
        "product",
        "sales_channel",
        "year",
        "sales_rep",
        "payment_mode",
    ]:
        del st.session_state[key]
    st.rerun()


#-Calculations and Visualizations------------------------------
st.title("📚Overview")

total_profit = filtered_df['Profit'].sum()
avg_profit_margin = filtered_df['Profit_Margin'].mean() * 100
total_sales = filtered_df['Sales'].sum()
total_cost = filtered_df['Cost'].sum()
total_order = filtered_df['Order_ID'].nunique()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales", format_currency(total_sales))
col2.metric("Total Profit", format_currency(total_profit))
col3.metric("Average Profit Margin", f"{avg_profit_margin:.2f}%")
col4.metric("Total Cost", format_currency(total_cost))
col5.metric("Total Orders", format_value(total_order))

sales_monthly = filtered_df.groupby(filtered_df['Order_Date'].dt.to_period('M'))['Sales'].sum().reset_index()
sales_monthly['Order_Date'] = sales_monthly['Order_Date'].astype(str)

fig1 = px.line(sales_monthly, x='Order_Date', y='Sales')
fig1.update_layout(**plotly_futuristic_layout("Monthly Sales Trend"))
st.plotly_chart(fig1, use_container_width=True)

region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig2 = px.pie(region, values='Sales', names='Region', title='Sales by Region')
fig2.update_layout(**plotly_futuristic_layout("Sales by Region"))

product = filtered_df.groupby('Product')['Sales'].sum().reset_index()
fig3 = px.bar(product, x='Product', y='Sales', color='Sales', title='Sales by Product')
fig3.update_layout(**plotly_futuristic_layout("Sales by Product"))

sales_channel = filtered_df.groupby('Sales_Channel')['Sales'].sum().reset_index()
fig4 = px.bar(sales_channel, x='Sales_Channel', y='Sales', color='Sales', title='Sales by Sales Channel')
fig4.update_layout(**plotly_futuristic_layout("Sales by Sales Channel"))


payment_mode = filtered_df.groupby('Payment_Mode')['Sales'].sum().reset_index()
fig5 = px.pie(payment_mode, values='Sales', names='Payment_Mode', hole=0.5, title='Sales by Payment Mode')
fig5.update_layout(**plotly_futuristic_layout("Sales by Payment Mode"))


col1, col2 = st.columns(2)
with col1:
	st.plotly_chart(fig2, use_container_width=True)
	st.plotly_chart(fig3, use_container_width=True)
with col2:
	st.plotly_chart(fig4, use_container_width=True)
	st.plotly_chart(fig5, use_container_width=True)


#-Insights----------------------------------------
insight("Most sales are generated through the Online channel, indicating a strong preference for digital purchasing among customers. This trend suggests that investing in online marketing and improving the e-commerce platform could further boost sales.",
        label="Sales Channel Insight",
        kind="success")
insight("The East region contributes the highest sales, indicating a strong market presence. Focusing marketing efforts and expanding product offerings in this region could further enhance sales performance.",
		label="Regional Sales Insight",
		kind="info")
insight("Most Payment are made through Credit Card, suggesting that customers prefer the convenience and security of this payment method. Offering promotions or discounts for credit card payments could encourage more sales.",
        label="Payment Mode Insight",
		kind="warning")
insight("Product Office Chairs generates the highest sales, indicating strong demand. Expanding the product line or offering complementary products could capitalize on this popularity and drive additional sales.",
		label="Product Sales Insight",
		kind="info")