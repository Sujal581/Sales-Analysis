import os
import pandas as pd
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sales_data.csv")


def load_raw() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    df["Sales_Channel"] = df["Sales_Channel"].str.replace(" ", "")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

    numeric_cols = ["Units", "Unit_Price", "Discount", "Sales", "Cost", "Profit"]
    categorical_cols = [
        "Customer_Name", "Region", "State", "Product",
        "Sales_Channel", "Payment_Mode", "Sales_Rep", "Return_Status",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])
            df[col] = df[col].str.strip().str.title().astype(str)

    df["Profit_Margin"] = np.where(df["Sales"] != 0, df["Profit"] / df["Sales"], 0)
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month_name()
    df["Month_Num"] = df["Order_Date"].dt.month
    df["Quarter"] = df["Order_Date"].dt.quarter.apply(lambda q: f"Q{q}")

    df["Return_Status"] = (
        df["Return_Status"]
        .astype(str)
        .str.strip()
        .str.replace("Unkown Status", "Unknown Status")
        .str.replace("Unkown", "Unknown")
    )

    df.reset_index(drop=True, inplace=True)
    return df


def format_currency(num: float) -> str:
    if num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num/1_000:.2f}K"
    return f"${num:.2f}"


def format_value(num: float) -> str:
    if num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.2f}K"
    return str(int(num))


def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    import streamlit as st

    defaults = {
        "region": "All", "product": "All", "sales_channel": "All",
        "sales_rep": "All", "payment_mode": "All", "state": "All",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    st.sidebar.title("Sales Intelligence")

    st.sidebar.selectbox("Region", ["All"] + sorted(df["Region"].dropna().unique().tolist()), key="region")
    st.sidebar.selectbox("Product", ["All"] + sorted(df["Product"].dropna().unique().tolist()), key="product")
    st.sidebar.selectbox("Sales Channel", ["All"] + sorted(df["Sales_Channel"].dropna().unique().tolist()), key="sales_channel")
    st.sidebar.selectbox("Sales Rep", ["All"] + sorted(df["Sales_Rep"].dropna().unique().tolist()), key="sales_rep")
    st.sidebar.selectbox("Payment Mode", ["All"] + sorted(df["Payment_Mode"].dropna().unique().tolist()), key="payment_mode")
    st.sidebar.selectbox("State", ["All"] + sorted(df["State"].dropna().unique().tolist()), key="state")

    if st.sidebar.button("Reset Filters"):
        for key in list(defaults.keys()):
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    filtered = df.copy()
    if st.session_state.get("region", "All") != "All":
        filtered = filtered[filtered["Region"] == st.session_state.region]
    if st.session_state.get("product", "All") != "All":
        filtered = filtered[filtered["Product"] == st.session_state.product]
    if st.session_state.get("sales_channel", "All") != "All":
        filtered = filtered[filtered["Sales_Channel"] == st.session_state.sales_channel]
    if st.session_state.get("sales_rep", "All") != "All":
        filtered = filtered[filtered["Sales_Rep"] == st.session_state.sales_rep]
    if st.session_state.get("payment_mode", "All") != "All":
        filtered = filtered[filtered["Payment_Mode"] == st.session_state.payment_mode]
    if st.session_state.get("state", "All") != "All":
        filtered = filtered[filtered["State"] == st.session_state.state]

    return filtered
