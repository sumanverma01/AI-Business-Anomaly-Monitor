# AI Business Anomaly Monitor

An AI-powered business monitoring dashboard that detects unusual changes in business metrics and uses Google Gemini to generate business-focused anomaly analysis.

##  Project Overview

The AI Business Anomaly Monitor helps analysts monitor business performance and identify unusual changes in important metrics such as revenue, orders, traffic, conversion rate, marketing cost, and refunds.

The system automatically compares current values with a 7-day historical baseline and identifies significant changes.

When an anomaly is detected, the dashboard provides:

- Business performance monitoring
- Automatic anomaly detection
- Severity classification
- AI-powered anomaly investigation using Google Gemini
- Email alerts for detected anomalies
- Interactive Streamlit dashboard

##  Features

###  Business Monitoring
Monitor important business KPIs through an interactive dashboard.

###  Anomaly Detection
The system compares daily metrics against a 7-day rolling baseline.

A metric is flagged when its change exceeds the defined threshold.

### Severity Detection

Anomalies are classified into different severity levels:

- `NORMAL` – No significant anomaly
- `WATCH` – One metric affected
- `MEDIUM` – Two metrics affected
- `HIGH` – Multiple metrics affected

###  AI Business Analysis

Google Gemini analyzes selected anomalies and provides:

1. Explanation of what changed
2. Possible business impact
3. Possible causes
4. Recommended investigation steps

The AI is instructed not to treat possible causes as confirmed facts.

###  Email Alerts

The system can send an email alert containing:

- Anomaly date
- Severity
- Revenue change
- Orders change
- Traffic change
- Conversion rate change
- Marketing cost change
- Refund changes

##  Technologies Used

- Python
- Pandas
- Streamlit
- Google Gemini API
- OpenPyXL
- Matplotlib
- HTML
- CSS
- JavaScript
- Gmail SMTP

##  Project Structure

```text
AI-Business-Anomaly-Monitor/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── business_data_new.xlsx
│
└── src/
    ├── ai_analyzer.py
    ├── anomaly_detector.py
    ├── create_dataset.py
    ├── data_loader.py
    ├── email_alert.py
    └── report_generator.py
