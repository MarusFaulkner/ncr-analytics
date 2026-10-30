import pandas as pd
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="NCR Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# LOAD NCR DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_ncr_data.csv")

    # Convert date columns into real Python/Pandas dates
    df["date_found"] = pd.to_datetime(df["date_found"])
    df["date_closed"] = pd.to_datetime(df["date_closed"], errors="coerce")

    return df


df = load_data()

# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------
st.title("📊 NCR Analytics Dashboard")

st.caption(
    "Python-based analysis of nonconformance trends, severity, aging, "
    "disposition, and quality performance."
)

# --------------------------------------------------
# BASIC DATA CHECK
# --------------------------------------------------
st.subheader("NCR Dataset")

st.write(f"Records loaded: {len(df)}")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
