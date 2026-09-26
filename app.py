import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))


# =========================================================
# IMPORT PROJECT MODULES
# =========================================================

from anomaly_detector import detect_anomalies, calculate_severity
from ai_analyzer import analyze_anomaly
from email_alert import send_alert


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Business Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   GLOBAL
   ===================================================== */

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: #f3f4f6;
}


/* Sidebar Date Input */

section[data-testid="stSidebar"]
[data-testid="stDateInput"]
input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 600 !important;
    background-color: #ffffff !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"]
[data-testid="stDateInput"]
input::placeholder {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}


/* Date input text containers */

section[data-testid="stSidebar"]
[data-testid="stDateInput"] {
    color: #111827 !important;
}


/* Multiselect */

section[data-testid="stSidebar"]
[data-testid="stMultiSelect"] div {
    color: #111827;
}


/* =====================================================
   HEADER
   ===================================================== */

.dashboard-title {
    font-size: 34px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 4px;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 25px;
}


/* =====================================================
   STATUS
   ===================================================== */

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background-color: #dcfce7;
    color: #166534;
    padding: 7px 13px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.status-dot {
    width: 8px;
    height: 8px;
    background-color: #22c55e;
    border-radius: 50%;
}


/* =====================================================
   KPI CARDS
   ===================================================== */

.kpi-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
}

.kpi-icon {
    font-size: 22px;
    margin-bottom: 8px;
}

.kpi-label {
    color: #6b7280;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.4px;
}

.kpi-value {
    color: #111827;
    font-size: 27px;
    font-weight: 800;
    margin-top: 7px;
}


/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #111827;
    margin-top: 28px;
    margin-bottom: 5px;
}

.section-description {
    color: #6b7280;
    font-size: 13px;
    margin-bottom: 15px;
}


/* =====================================================
   AI BUTTON AREA
   ===================================================== */

.ai-container {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px;
    margin-top: 10px;
}


/* =====================================================
   STREAMLIT BUTTONS
   ===================================================== */

.stButton > button {
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 42px;
}


/* =====================================================
   TABLE
   ===================================================== */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}


/* =====================================================
   HIDE STREAMLIT BRANDING
   ===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer-text {
    text-align: center;
    color: #9ca3af;
    font-size: 12px;
    padding-top: 30px;
    line-height: 1.7;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

file_path = BASE_DIR / "data" / "business_data_new.xlsx"

if not file_path.exists():

    st.error(
        f"Dataset not found: {file_path}"
    )

    st.stop()


df = pd.read_excel(file_path)

df["Date"] = pd.to_datetime(df["Date"])


# =========================================================
# ANOMALY DETECTION
# =========================================================

df = detect_anomalies(df)

df["Severity"] = df.apply(
    calculate_severity,
    axis=1
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:25px;
            font-weight:800;
            color:#ffffff;
            margin-bottom:4px;
        ">
            📊 AI Monitor
        </div>

        <div style="
            color:#9ca3af;
            font-size:12px;
            margin-bottom:30px;
        ">
            Business Intelligence System
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### Dashboard Filters"
    )

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    selected_dates = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    severity_filter = st.multiselect(
        "Severity",
        options=[
            "HIGH",
            "MEDIUM",
            "WATCH"
        ],
        default=[
            "HIGH",
            "MEDIUM",
            "WATCH"
        ]
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            font-size:11px;
            color:#9ca3af;
            line-height:1.8;
        ">
            <b style="color:#e5e7eb;">SYSTEM STATUS</b><br>
            Anomaly Detection: <span style="color:#4ade80;">Active</span><br>
            AI Analysis: <span style="color:#4ade80;">Gemini</span><br>
            Alerts: <span style="color:#4ade80;">Gmail SMTP</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


if (
    isinstance(selected_dates, tuple)
    and len(selected_dates) == 2
):

    start_date = pd.Timestamp(
        selected_dates[0]
    )

    end_date = pd.Timestamp(
        selected_dates[1]
    )

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date)
        &
        (filtered_df["Date"] <= end_date)
    ]


# Keep normal records for charts,
# but use severity filter for anomaly records.

anomaly_days = filtered_df[
    filtered_df["Severity"].isin(
        severity_filter
    )
].copy()


# =========================================================
# HEADER
# =========================================================

# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.html("""
    <div style="
        padding-top: 5px;
        padding-bottom: 5px;
    ">

        <div style="
            font-size: 34px;
            font-weight: 800;
            color: #111827;
            letter-spacing: -0.5px;
        ">
            AI Business Monitor
        </div>

        <div style="
            color: #6b7280;
            font-size: 14px;
            margin-top: 5px;
        ">
            Intelligent business performance and anomaly monitoring
        </div>

    </div>
    """)


with header_right:

    st.html("""
    <div style="
        text-align: right;
        padding-top: 12px;
    ">

        <span style="
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: #dcfce7;
            color: #166534;
            padding: 7px 13px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
        ">

            <span style="
                width: 8px;
                height: 8px;
                background: #22c55e;
                border-radius: 50%;
                display: inline-block;
            "></span>

            SYSTEM ONLINE

        </span>

    </div>
    """)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = filtered_df["Revenue"].sum()

total_orders = filtered_df["Orders"].sum()

total_traffic = filtered_df["Traffic"].sum()

anomaly_count = len(anomaly_days)


# =========================================================
# KPI CARDS
# =========================================================

# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.html(f"""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-radius:14px;
        padding:20px;
        min-height:105px;
        box-shadow:0 2px 8px rgba(15,23,42,0.04);
    ">

        <div style="
            font-size:22px;
            margin-bottom:8px;
        ">
            💰
        </div>

        <div style="
            color:#6b7280;
            font-size:11px;
            font-weight:700;
            letter-spacing:0.5px;
        ">
            TOTAL REVENUE
        </div>

        <div style="
            color:#111827;
            font-size:25px;
            font-weight:800;
            margin-top:6px;
        ">
            ₹{total_revenue:,.0f}
        </div>

    </div>
    """)


with k2:

    st.html(f"""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-radius:14px;
        padding:20px;
        min-height:105px;
        box-shadow:0 2px 8px rgba(15,23,42,0.04);
    ">

        <div style="
            font-size:22px;
            margin-bottom:8px;
        ">
            📦
        </div>

        <div style="
            color:#6b7280;
            font-size:11px;
            font-weight:700;
            letter-spacing:0.5px;
        ">
            TOTAL ORDERS
        </div>

        <div style="
            color:#111827;
            font-size:25px;
            font-weight:800;
            margin-top:6px;
        ">
            {total_orders:,}
        </div>

    </div>
    """)


with k3:

    st.html(f"""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-radius:14px;
        padding:20px;
        min-height:105px;
        box-shadow:0 2px 8px rgba(15,23,42,0.04);
    ">

        <div style="
            font-size:22px;
            margin-bottom:8px;
        ">
            👥
        </div>

        <div style="
            color:#6b7280;
            font-size:11px;
            font-weight:700;
            letter-spacing:0.5px;
        ">
            TOTAL TRAFFIC
        </div>

        <div style="
            color:#111827;
            font-size:25px;
            font-weight:800;
            margin-top:6px;
        ">
            {total_traffic:,}
        </div>

    </div>
    """)


with k4:

    st.html(f"""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-radius:14px;
        padding:20px;
        min-height:105px;
        box-shadow:0 2px 8px rgba(15,23,42,0.04);
    ">

        <div style="
            font-size:22px;
            margin-bottom:8px;
        ">
            🚨
        </div>

        <div style="
            color:#6b7280;
            font-size:11px;
            font-weight:700;
            letter-spacing:0.5px;
        ">
            ANOMALIES DETECTED
        </div>

        <div style="
            color:#111827;
            font-size:25px;
            font-weight:800;
            margin-top:6px;
        ">
            {anomaly_count}
        </div>

    </div>
    """)

# =========================================================
# BUSINESS PERFORMANCE
# =========================================================

st.markdown(
    """
    <div class="section-title">
        📈 Business Performance
    </div>

    <div class="section-description">
        Track revenue and operational activity over time.
    </div>
    """,
    unsafe_allow_html=True
)


chart_left, chart_right = st.columns(
    [2, 1]
)


# =========================================================
# REVENUE CHART
# =========================================================

with chart_left:

    fig_revenue = px.area(
        filtered_df,
        x="Date",
        y="Revenue"
    )

    fig_revenue.update_layout(
        title="Revenue Trend",
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(
            family="Arial"
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            gridcolor="#e5e7eb"
        )
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )


# =========================================================
# ANOMALY DISTRIBUTION
# =========================================================

with chart_right:

    severity_counts = (
        filtered_df["Severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = [
        "Severity",
        "Count"
    ]

    fig_severity = px.pie(
        severity_counts,
        names="Severity",
        values="Count",
        hole=0.55
    )

    fig_severity.update_layout(
        title="Severity Distribution",
        height=360,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        ),
        paper_bgcolor="white",
        font=dict(
            family="Arial"
        ),
        legend=dict(
            orientation="h",
            y=-0.1
        )
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )


# =========================================================
# ORDERS + TRAFFIC
# =========================================================

fig_activity = go.Figure()


fig_activity.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Orders"],
        name="Orders",
        mode="lines+markers",
        line=dict(width=3)
    )
)


fig_activity.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Traffic"],
        name="Traffic",
        mode="lines",
        yaxis="y2",
        line=dict(width=3)
    )
)


fig_activity.update_layout(
    title="Orders & Traffic",
    height=370,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),
    xaxis=dict(
        showgrid=False
    ),
    yaxis=dict(
        title="Orders",
        gridcolor="#e5e7eb"
    ),
    yaxis2=dict(
        title="Traffic",
        overlaying="y",
        side="right",
        showgrid=False
    )
)


st.plotly_chart(
    fig_activity,
    use_container_width=True
)


# =========================================================
# ANOMALY TABLE
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🚨 Detected Business Anomalies
    </div>

    <div class="section-description">
        Business metrics that moved significantly from their baseline.
    </div>
    """,
    unsafe_allow_html=True
)


if len(anomaly_days) > 0:

    display_columns = [
        "Date",
        "Severity",
        "Revenue_Change",
        "Orders_Change",
        "Traffic_Change",
        "Conversion_Rate_Change",
        "Marketing_Cost_Change",
        "Refunds_Change"
    ]

    display_df = anomaly_days[
        display_columns
    ].copy()

    display_df["Date"] = (
        display_df["Date"]
        .dt.strftime("%Y-%m-%d")
    )


    for column in display_columns[2:]:

        display_df[column] = (
            display_df[column]
            .map(
                lambda x: f"{x:.1f}%"
            )
        )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No anomalies detected for the selected filters."
    )


# =========================================================
# AI ANOMALY INVESTIGATION
# =========================================================


st.markdown(
    "## 🤖 AI Anomaly Investigation"
)

st.write(
    "Use Gemini to investigate a selected anomaly "
    "and generate business-focused insights."
)


if len(anomaly_days) > 0:

    anomaly_dates = (
        anomaly_days["Date"]
        .dt.strftime("%Y-%m-%d")
        .tolist()
    )

    selected_date = st.selectbox(
        "Select anomaly date",
        anomaly_dates
    )

    selected_row = anomaly_days[
        anomaly_days["Date"]
        .dt.strftime("%Y-%m-%d")
        == selected_date
    ].iloc[0]


    # =====================================================
    # ANOMALY CARD
    # =====================================================

    severity = str(
        selected_row["Severity"]
    ).upper()

    if severity == "HIGH":
        severity_color = "#b91c1c"
        severity_bg = "#fee2e2"

    elif severity == "MEDIUM":
        severity_color = "#b45309"
        severity_bg = "#fef3c7"

    else:
        severity_color = "#1d4ed8"
        severity_bg = "#dbeafe"


    alert_html = f"""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-left:5px solid {severity_color};
        border-radius:12px;
        padding:18px 20px;
        margin:15px 0;
    ">

        <div style="
            color:#111827;
            font-size:16px;
            font-weight:700;
            margin-bottom:6px;
        ">
            ⚠️ {severity} Severity Anomaly
        </div>

        <div style="
            color:#6b7280;
            font-size:13px;
            line-height:1.6;
        ">
            Business anomaly detected on
            <strong style="color:#111827;">
                {selected_date}
            </strong>.

            Review the affected metrics before taking action.
        </div>

    </div>
    """

    st.html(alert_html)


    # =====================================================
    # SELECTED METRICS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Revenue Change",
            f"{selected_row['Revenue_Change']:.1f}%"
        )

    with col2:

        st.metric(
            "Orders Change",
            f"{selected_row['Orders_Change']:.1f}%"
        )

    with col3:

        st.metric(
            "Traffic Change",
            f"{selected_row['Traffic_Change']:.1f}%"
        )


    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    st.markdown("### Actions")

    ai_col, email_col = st.columns(2)


    with ai_col:

        generate_ai = st.button(
            "🤖 Generate AI Analysis",
            type="primary",
            use_container_width=True
        )


    with email_col:

        send_email = st.button(
            "📧 Send Email Alert",
            use_container_width=True
        )


    # =====================================================
    # GEMINI
    # =====================================================

    if generate_ai:

        with st.spinner(
            "Gemini is analyzing the anomaly..."
        ):

            try:

                analysis = analyze_anomaly(
                    selected_row
                )

                st.success(
                    "AI analysis generated successfully!"
                )

                st.markdown(
                    "### 🧠 AI Business Analysis"
                )

                st.write(
                    analysis
                )

            except Exception as e:

                st.error(
                    "AI analysis could not be generated."
                )

                st.warning(
                    f"Details: {e}"
                )


    # =====================================================
    # EMAIL
    # =====================================================

    if send_email:

        with st.spinner(
            "Sending email alert..."
        ):

            try:

                send_alert(
                    selected_row
                )

                st.success(
                    "📧 Email alert sent successfully!"
                )

            except Exception as e:

                st.error(
                    "Email alert could not be sent."
                )

                st.warning(
                    f"Details: {e}"
                )


else:

    st.info(
        "No anomalies match the selected filters."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.html("""
<div style="
    text-align:center;
    padding:18px 10px 8px 10px;
    color:#6b7280;
    font-size:13px;
">

    <div style="
        color:#111827;
        font-size:15px;
        font-weight:700;
        margin-bottom:6px;
    ">
        AI Business Anomaly Monitor
    </div>

    <div style="margin-bottom:8px;">
        Developed by <strong style="color:#111827;">Suman Verma</strong>
    </div>

    <div style="
        font-size:12px;
        color:#9ca3af;
    ">
        Python • Pandas • Streamlit • Google Gemini 
    </div>

    <div style="
        margin-top:10px;
        font-size:11px;
        color:#9ca3af;
    ">
        AI-powered business performance & anomaly monitoring
    </div>

</div>
""")