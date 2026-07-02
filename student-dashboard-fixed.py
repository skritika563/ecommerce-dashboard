import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    layout="wide"
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------
st.markdown(r"""
<style>
.stApp{background-color:#0B1F3A;color:white;}
section[data-testid="stSidebar"]{background:#13294B;}
h1,h2,h3,p,label{color:white!important;}
div[data-testid="stMetric"]{
background:#D6EAF8!important;
border:2px solid #5DADE2;
border-radius:12px;
padding:15px;
}
div[data-testid="stMetric"] *{
color:#111111!important;
fill:#111111!important;
}
.stDownloadButton>button{
background:#3498DB;color:white;border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🛒 E-Commerce Sales Analytics Dashboard")
st.write("Analyze e-commerce sales using Pandas and Matplotlib.")

# -------------------------------------------------
# Read CSV
# -------------------------------------------------
df = pd.read_csv("ecommerce_sales.csv")

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("Filters")

cat = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

city = st.sidebar.multiselect(
    "City",
    df["City"].unique(),
    default=df["City"].unique()
)

pay = st.sidebar.multiselect(
    "Payment Method",
    df["Payment_Method"].unique(),
    default=df["Payment_Method"].unique()
)

stat = st.sidebar.multiselect(
    "Order Status",
    df["Order_Status"].unique(),
    default=df["Order_Status"].unique()
)

amt = st.sidebar.slider(
    "Total Amount",
    int(df["Total_Amount"].min()),
    int(df["Total_Amount"].max()),
    (
        int(df["Total_Amount"].min()),
        int(df["Total_Amount"].max())
    )
)

# -------------------------------------------------
# Filter Data
# -------------------------------------------------
filtered = df[
    (df["Category"].isin(cat)) &
    (df["City"].isin(city)) &
    (df["Payment_Method"].isin(pay)) &
    (df["Order_Status"].isin(stat)) &
    (df["Total_Amount"].between(amt[0], amt[1]))
]

# -------------------------------------------------
# Display Data
# -------------------------------------------------
st.subheader("Filtered Data")
st.dataframe(filtered, width="stretch")

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Orders", len(filtered))

with c2:
    st.metric("Revenue", f"₹ {filtered['Total_Amount'].sum():,}")

with c3:
    avg = filtered["Total_Amount"].mean() if len(filtered) else 0
    st.metric("Average Order", f"₹ {avg:.2f}")

with c4:
    mx = filtered["Total_Amount"].max() if len(filtered) else 0
    st.metric("Highest Order", f"₹ {mx:,}")

# -------------------------------------------------
# Summary Statistics
# -------------------------------------------------
st.subheader("Summary Statistics")
st.dataframe(filtered.describe(), width="stretch")

# -------------------------------------------------
# Charts
# -------------------------------------------------
st.subheader("Sales Visualizations")

col1, col2 = st.columns(2, gap="large")

# -------------------------------
# Bar Chart
# -------------------------------
with col1:

    fig, ax = plt.subplots(figsize=(5.8, 3.8))

    filtered.groupby("Category")["Total_Amount"].mean().plot(
        kind="bar",
        color="skyblue",
        ax=ax
    )

    ax.set_title("Average Revenue by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue")

    st.pyplot(fig)

# -------------------------------
# Pie Chart
# -------------------------------
with col2:

    fig, ax = plt.subplots(figsize=(5.8, 3.8))

    filtered["Payment_Method"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")
    ax.set_title("Payment Method Distribution")

    st.pyplot(fig)

# Second Row
col3, col4 = st.columns(2, gap="large")

# -------------------------------
# Histogram
# -------------------------------
with col3:

    fig, ax = plt.subplots(figsize=(5.8, 3.8))

    ax.hist(
        filtered["Total_Amount"],
        bins=10,
        color="lightgreen",
        edgecolor="black"
    )

    ax.set_title("Order Amount Distribution")
    ax.set_xlabel("Total Amount")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

# -------------------------------
# Scatter Plot
# -------------------------------
with col4:

    fig, ax = plt.subplots(figsize=(5.8, 3.8))

    ax.scatter(
        filtered["Quantity"],
        filtered["Total_Amount"],
        color="orange"
    )

    ax.set_title("Quantity vs Total Amount")
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Total Amount")

    st.pyplot(fig)

# -------------------------------------------------
# Download CSV
# -------------------------------------------------
st.download_button(
    label="📥 Download Filtered CSV",
    data=filtered.to_csv(index=False),
    file_name="filtered_sales.csv",
    mime="text/csv"
)