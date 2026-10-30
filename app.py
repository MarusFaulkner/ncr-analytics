import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# QUALITY ANALYTICS
# --------------------------------------------------
st.subheader("Quality Analytics")

chart_col1, chart_col2 = st.columns(2)

# Pareto analysis
category_summary = (
    filtered_df["category"]
    .value_counts()
    .rename_axis("Category")
    .reset_index(name="NCR Count")
)

category_summary["Cumulative %"] = (
    category_summary["NCR Count"].cumsum()
    / category_summary["NCR Count"].sum()
    * 100
)

with chart_col1:
    st.markdown("#### NCR Category Pareto")

      pareto_fig = make_subplots(
        specs=[[{"secondary_y": True}]]
    )

    # Frequency bars
    pareto_fig.add_trace(
        go.Bar(
            x=category_summary["Category"],
            y=category_summary["NCR Count"],
            name="NCR Count"
        ),
        secondary_y=False
    )

    # Cumulative percentage line
    pareto_fig.add_trace(
        go.Scatter(
            x=category_summary["Category"],
            y=category_summary["Cumulative %"],
            name="Cumulative %",
            mode="lines+markers"
        ),
        secondary_y=True
    )

    # 80% reference line
    pareto_fig.add_hline(
        y=80,
        line_dash="dash",
        annotation_text="80%",
        secondary_y=True
    )

    pareto_fig.update_xaxes(
        title_text="Category",
        tickangle=-45
    )

    pareto_fig.update_yaxes(
        title_text="NCR Count",
        secondary_y=False
    )

    pareto_fig.update_yaxes(
        title_text="Cumulative %",
        range=[0, 105],
        ticksuffix="%",
        secondary_y=True
    )

    pareto_fig.update_layout(
        title="Nonconformance Category Pareto",
        legend_orientation="h",
        legend_y=1.15
    )

    st.plotly_chart(
        pareto_fig,
        use_container_width=True
    )

# Severity analysis
severity_summary = (
    filtered_df["severity"]
    .value_counts()
    .rename_axis("Severity")
    .reset_index(name="NCR Count")
)

with chart_col2:
    st.markdown("#### Severity Breakdown")

    severity_fig = px.pie(
        severity_summary,
        names="Severity",
        values="NCR Count",
        hole=0.55
    )

    st.plotly_chart(
        severity_fig,
        use_container_width=True
    )

# --------------------------------------------------
# MONTHLY TREND
# --------------------------------------------------
st.markdown("#### Monthly NCR Trend")

monthly_summary = (
    filtered_df
    .assign(
        Month=filtered_df["date_found"].dt.to_period("M").astype(str)
    )
    .groupby("Month")
    .size()
    .reset_index(name="NCR Count")
)

trend_fig = px.line(
    monthly_summary,
    x="Month",
    y="NCR Count",
    markers=True
)

trend_fig.update_layout(
    yaxis_title="NCR Count",
    xaxis_title="Month"
)

st.plotly_chart(
    trend_fig,
    use_container_width=True
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
