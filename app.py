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
# LOAD AND PREPARE NCR DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_ncr_data.csv")

    df["date_found"] = pd.to_datetime(df["date_found"])
    df["date_closed"] = pd.to_datetime(
        df["date_closed"],
        errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    # Use closure date for closed NCRs and today's date for active NCRs
    end_date = df["date_closed"].fillna(today)

    df["days_open"] = (
        end_date - df["date_found"]
    ).dt.days.clip(lower=0)

    # Aging groups
    df["aging_bucket"] = pd.cut(
        df["days_open"],
        bins=[-1, 7, 14, 30, float("inf")],
        labels=["0–7 Days", "8–14 Days", "15–30 Days", "31+ Days"]
    )

    return df


df = load_data()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("Filters")

status_filter = st.sidebar.multiselect(
    "Status",
    options=sorted(df["status"].unique()),
    default=sorted(df["status"].unique())
)

severity_filter = st.sidebar.multiselect(
    "Severity",
    options=sorted(df["severity"].unique()),
    default=sorted(df["severity"].unique())
)

category_filter = st.sidebar.multiselect(
    "Category",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)

owner_filter = st.sidebar.multiselect(
    "Assigned To",
    options=sorted(df["assigned_to"].unique()),
    default=sorted(df["assigned_to"].unique())
)

filtered_df = df[
    df["status"].isin(status_filter)
    & df["severity"].isin(severity_filter)
    & df["category"].isin(category_filter)
    & df["assigned_to"].isin(owner_filter)
].copy()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("📊 NCR Analytics Dashboard")

st.caption(
    "Python + Pandas analysis of nonconformance trends, severity, "
    "aging, disposition, and quality performance."
)

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
total_ncrs = len(filtered_df)

open_ncrs = len(
    filtered_df[filtered_df["status"] != "Closed"]
)

critical_open = len(
    filtered_df[
        (filtered_df["severity"] == "Critical")
        & (filtered_df["status"] != "Closed")
    ]
)

overdue_ncrs = len(
    filtered_df[
        (filtered_df["status"] != "Closed")
        & (filtered_df["days_open"] > 30)
    ]
)

closed_df = filtered_df[
    filtered_df["status"] == "Closed"
]

avg_close_days = (
    closed_df["days_open"].mean()
    if not closed_df.empty
    else 0
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
st.subheader("Quality Performance Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total NCRs", total_ncrs)
col2.metric("Active NCRs", open_ncrs)
col3.metric("Critical Open", critical_open)
col4.metric("Overdue >30 Days", overdue_ncrs)
col5.metric("Avg. Closure Time", f"{avg_close_days:.1f} days")

# --------------------------------------------------
# AGING ANALYSIS
# --------------------------------------------------
st.subheader("NCR Aging Analysis")

active_df = filtered_df[
    filtered_df["status"] != "Closed"
]

aging_summary = (
    active_df["aging_bucket"]
    .value_counts(sort=False)
    .rename_axis("Aging Range")
    .reset_index(name="NCR Count")
)

st.bar_chart(
    aging_summary,
    x="Aging Range",
    y="NCR Count"
)

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------
st.subheader("NCR Records")

st.write(
    f"Showing **{len(filtered_df)}** of **{len(df)}** NCR records."
)

display_df = filtered_df.copy()

display_df["date_found"] = display_df["date_found"].dt.strftime("%Y-%m-%d")
display_df["date_closed"] = display_df["date_closed"].dt.strftime("%Y-%m-%d")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
