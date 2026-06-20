import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Payment Analytics Dashboard",
    layout="wide",
    page_icon="💳"
)

st.title("💳 Payment Processing Dashboard")
st.markdown("Real-time analytics for transactions, fraud detection, and reconciliation.")

# -------------------------
# DB Connection
# -------------------------
engine = create_engine(
    "postgresql+psycopg2://payment_user:payment_pass@payment-postgres:5432/payment_db"
)
# -------------------------
# Cached Data Load
# -------------------------
@st.cache_data(ttl=60)
def load_data():
    transactions = pd.read_sql("SELECT * FROM transactions", engine)
    fraud_alerts = pd.read_sql("SELECT * FROM fraud_alerts", engine)
    reconciliation = pd.read_sql("SELECT * FROM reconciliation_results", engine)
    return transactions, fraud_alerts, reconciliation


# Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

with st.spinner("Loading data..."):
    transactions, fraud_alerts, reconciliation = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔍 Filters")

status_filter = st.sidebar.multiselect(
    "Transaction Status",
    options=transactions["status"].dropna().unique(),
    default=transactions["status"].dropna().unique()
)

transactions = transactions[transactions["status"].isin(status_filter)]

# -------------------------
# KPIs
# -------------------------
total_transactions = len(transactions)
total_amount = transactions["amount"].sum() if "amount" in transactions else 0
fraud_count = len(fraud_alerts)
recon_issues = len(reconciliation)

col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 Transactions", f"{total_transactions:,}")
col2.metric("💰 Total Amount", f"₹{total_amount:,.0f}")
col3.metric("🚨 Fraud Alerts", f"{fraud_count:,}")
col4.metric("⚠️ Recon Issues", f"{recon_issues:,}")

st.divider()

# -------------------------
# Tabs Layout
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Transactions",
    "🚨 Fraud Analysis",
    "⚖️ Reconciliation",
    "📄 Raw Data"
])

# -------------------------
# TAB 1 - Transactions
# -------------------------
with tab1:
    st.subheader("Transaction Status Distribution")

    if "status" in transactions.columns:
        status_counts = transactions["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]

        fig = px.bar(
            status_counts,
            x="status",
            y="count",
            text="count",
            color="status"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Amount Distribution")

    if "amount_category" in transactions.columns:
        amt_counts = transactions["amount_category"].value_counts().reset_index()
        amt_counts.columns = ["category", "count"]

        fig = px.pie(
            amt_counts,
            names="category",
            values="count",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# TAB 2 - Fraud
# -------------------------
with tab2:
    st.subheader("Fraud Reason Analysis")

    if len(fraud_alerts) > 0 and "fraud_reason" in fraud_alerts.columns:
        fraud_counts = fraud_alerts["fraud_reason"].value_counts().reset_index()
        fraud_counts.columns = ["reason", "count"]

        fig = px.bar(
            fraud_counts,
            x="reason",
            y="count",
            text="count",
            color="count"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No fraud data available.")

# -------------------------
# TAB 3 - Reconciliation
# -------------------------
with tab3:
    st.subheader("Reconciliation Status")

    if "reconciliation_status" in reconciliation.columns:
        recon_counts = reconciliation["reconciliation_status"].value_counts().reset_index()
        recon_counts.columns = ["status", "count"]

        fig = px.bar(
            recon_counts,
            x="status",
            y="count",
            text="count",
            color="status"
        )
        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# TAB 4 - Raw Data
# -------------------------
with tab4:
    st.subheader("Latest Transactions")

    st.dataframe(
        transactions.head(50),
        use_container_width=True
    )

    with st.expander("View Fraud Data"):
        st.dataframe(fraud_alerts, use_container_width=True)

    with st.expander("View Reconciliation Data"):
        st.dataframe(reconciliation, use_container_width=True)