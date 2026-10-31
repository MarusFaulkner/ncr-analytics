# NCR Analytics Dashboard

A Python and Streamlit quality analytics application for analyzing Nonconformance Report (NCR) data.

The dashboard transforms NCR records into interactive quality metrics and visualizations that help identify defect trends, aging issues, disposition patterns, severity levels, and higher-risk open NCRs.

## 🌐 Live Application

**[Launch the NCR Analytics Dashboard](https://ncr-quality-analytics.streamlit.app/)**

## 📊 Dashboard Capabilities

### Quality Performance Overview

Provides key NCR performance indicators including:

- Total NCRs
- Active NCRs
- Critical open NCRs
- NCRs overdue more than 30 days
- Average NCR closure time

### NCR Aging Analysis

Automatically calculates how long NCRs have remained open and groups active records into aging ranges:

- 0–7 Days
- 8–14 Days
- 15–30 Days
- 31+ Days

This helps identify aging NCRs that may require additional attention.

### NCR Category Pareto Analysis

Uses Pareto-style analysis to rank nonconformance categories by frequency.

The visualization includes:

- NCR count by category
- Cumulative percentage
- 80% reference line

This helps identify the categories contributing most heavily to overall nonconformance activity.

### Severity Breakdown

Displays the distribution of NCR severity classifications:

- Minor
- Major
- Critical

This provides a quick view of the overall risk profile of the NCR dataset.

### Monthly NCR Trend

Tracks the number of NCRs identified by month, making it easier to see changes in nonconformance activity over time.

### Disposition Analysis

Analyzes how NCRs are being dispositioned, including:

- Rework
- Accept As-Is
- Scrap
- Return to Vendor
- Pending
- Use As-Is with Deviation

### Open NCR Risk Review

Creates a focused view of active NCRs prioritized by severity and age.

The review includes:

- NCR ID
- Component
- Category
- Severity
- Status
- Assigned department
- Days open
- Aging range

This helps highlight higher-priority NCRs instead of treating every open NCR equally.

### Interactive Filtering

Dashboard results can be filtered dynamically by:

- Status
- Severity
- Nonconformance category
- Assigned department

The KPIs, charts, and tables respond to the selected filters.

### CSV Upload

Users can upload a compatible NCR CSV dataset directly through the Streamlit interface.

Uploaded data is processed with Pandas and used to dynamically generate the dashboard's calculations, analytics, charts, and NCR records.

A sample NCR dataset is included so the application can also be explored without uploading a file.

## 🛠️ Technology

- Python
- Streamlit
- Pandas
- Plotly
- CSV data processing

## 🎯 Project Purpose

This project demonstrates the intersection of manufacturing quality and data analytics by applying Python-based analysis to Nonconformance Report data.

It was developed as a hands-on Quality + Technology portfolio project focused on turning manufacturing quality records into useful information for trend analysis, prioritization, and quality performance review.

## ⚠️ Portfolio Project

The NCR records included with this repository are sample data created for demonstration and analytics purposes.

This application is a portfolio project and is not presented as a production electronic quality management system (eQMS).
