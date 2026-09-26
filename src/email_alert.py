import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from pathlib import Path
from html import escape


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


def send_alert(row):

    # Load environment variables
    load_dotenv(ENV_FILE, override=True)

    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        raise ValueError("Email settings are missing in .env")

    # -----------------------------
    # Business data
    # -----------------------------

    date = escape(str(row["Date"]))
    severity = escape(str(row["Severity"]))

    revenue = float(row["Revenue_Change"])
    orders = float(row["Orders_Change"])
    traffic = float(row["Traffic_Change"])
    conversion = float(row["Conversion_Rate_Change"])
    marketing = float(row["Marketing_Cost_Change"])
    refunds = float(row["Refunds_Change"])

    # -----------------------------
    # Helper function
    # -----------------------------

    def change_color(value):
        if value < 0:
            return "#dc2626"
        elif value > 0:
            return "#16a34a"
        return "#64748b"

    def format_change(value):
        sign = "+" if value > 0 else ""
        return f"{sign}{value:.1f}%"

    # -----------------------------
    # Email
    # -----------------------------

    msg = EmailMessage()

    msg["Subject"] = (
        f"🚨 Business Anomaly Alert | {severity} | {date}"
    )

    msg["From"] = sender
    msg["To"] = receiver

    # Plain-text fallback
    plain_text = f"""
AI BUSINESS ANOMALY ALERT

Date: {date}
Severity: {severity}

Revenue: {format_change(revenue)}
Orders: {format_change(orders)}
Traffic: {format_change(traffic)}
Conversion Rate: {format_change(conversion)}
Marketing Cost: {format_change(marketing)}
Refunds: {format_change(refunds)}

Please investigate the affected business metrics.

AI Business Anomaly Monitoring System
"""

    msg.set_content(plain_text)

    # -----------------------------
    # Professional HTML email
    # -----------------------------

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Business Anomaly Alert</title>

</head>

<body style="
    margin:0;
    padding:0;
    background-color:#f3f4f6;
    font-family:Arial, Helvetica, sans-serif;
">

<table width="100%" cellpadding="0" cellspacing="0" style="padding:30px 10px;">

<tr>

<td align="center">

<table width="650" cellpadding="0" cellspacing="0" style="
    max-width:650px;
    background:#ffffff;
    border-radius:12px;
    overflow:hidden;
    box-shadow:0 4px 15px rgba(0,0,0,0.08);
">

<!-- HEADER -->

<tr>

<td style="
    background:#111827;
    padding:28px 30px;
    color:white;
">

<div style="
    font-size:13px;
    color:#9ca3af;
    margin-bottom:8px;
    letter-spacing:1px;
">

AI BUSINESS MONITOR

</div>

<div style="
    font-size:25px;
    font-weight:bold;
">

🚨 Business Anomaly Detected

</div>

<p style="
    margin:8px 0 0;
    color:#d1d5db;
    font-size:14px;
">

Automated business performance monitoring alert

</p>

</td>

</tr>


<!-- ALERT INFO -->

<tr>

<td style="padding:25px 30px 10px;">

<table width="100%" cellpadding="0" cellspacing="0">

<tr>

<td>

<div style="
    color:#6b7280;
    font-size:12px;
    text-transform:uppercase;
">

Anomaly Date

</div>

<div style="
    font-size:17px;
    font-weight:bold;
    color:#111827;
    margin-top:5px;
">

{date}

</div>

</td>


<td align="right">

<span style="
    display:inline-block;
    background:#fee2e2;
    color:#b91c1c;
    padding:7px 14px;
    border-radius:20px;
    font-size:12px;
    font-weight:bold;
">

{severity}

</span>

</td>

</tr>

</table>

</td>

</tr>


<!-- MESSAGE -->

<tr>

<td style="padding:15px 30px;">

<div style="
    background:#fff7ed;
    border-left:4px solid #f97316;
    padding:14px 16px;
    border-radius:6px;
    color:#7c2d12;
    font-size:14px;
    line-height:1.5;
">

<strong>Attention required:</strong>

Unusual changes have been detected in one or more business performance metrics.

Please review the affected metrics and investigate the possible causes.

</div>

</td>

</tr>


<!-- KPI SECTION -->

<tr>

<td style="padding:10px 30px 25px;">

<div style="
    font-size:18px;
    font-weight:bold;
    color:#111827;
    margin-bottom:15px;
">

Performance Changes

</div>


<table width="100%" cellpadding="0" cellspacing="8">


<!-- Revenue -->

<tr>

<td style="
    background:#f9fafb;
    padding:16px;
    border-radius:8px;
">

<div style="color:#6b7280;font-size:12px;">
Revenue
</div>

<div style="
    color:{change_color(revenue)};
    font-size:22px;
    font-weight:bold;
    margin-top:5px;
">

{format_change(revenue)}

</div>

</td>


<td style="
    background:#f9fafb;
    padding:16px;
    border-radius:8px;
">

<div style="color:#6b7280;font-size:12px;">
Orders
</div>

<div style="
    color:{change_color(orders)};
    font-size:22px;
    font-weight:bold;
    margin-top:5px;
">

{format_change(orders)}

</div>

</td>

</tr>


<!-- Traffic -->

<tr>

<td style="
    background:#f9fafb;
    padding:16px;
    border-radius:8px;
">

<div style="color:#6b7280;font-size:12px;">
Traffic
</div>

<div style="
    color:{change_color(traffic)};
    font-size:22px;
    font-weight:bold;
    margin-top:5px;
">

{format_change(traffic)}

</div>

</td>


<td style="
    background:#f9fafb;
    padding:16px;
    border-radius:8px;
">

<div style="color:#6b7280;font-size:12px;">
Conversion Rate
</div>

<div style="
    color:{change_color(conversion)};
    font-size:22px;
    font-weight:bold;
    margin-top:5px;
">

{format_change(conversion)}

</div>

</td>

</tr>


<!-- Marketing -->

<tr>

<td style="
    background:#f9fafb;
    padding:16px;
    border-radius:8px;
">

<div style="color:#6b7280;font-size:12px;">
Marketing Cost
</div>

<div style="
    color:{change_color(marketing)};
    font-size:22px;
    font-weight:bold;
    margin-top:5px;
">

{format_change(marketing)}

</div>

</td>


<td style="
    background:#f9fafb;
    padding:16px;
    border-radius:8px;
">

<div style="color:#6b7280;font-size:12px;">
Refunds
</div>

<div style="
    color:{change_color(refunds)};
    font-size:22px;
    font-weight:bold;
    margin-top:5px;
">

{format_change(refunds)}

</div>

</td>

</tr>

</table>

</td>

</tr>


<!-- NEXT STEP -->

<tr>

<td style="padding:0 30px 25px;">

<div style="
    border-top:1px solid #e5e7eb;
    padding-top:20px;
">

<div style="
    font-size:16px;
    font-weight:bold;
    color:#111827;
    margin-bottom:8px;
">

Recommended Action

</div>

<p style="
    margin:0;
    color:#4b5563;
    font-size:14px;
    line-height:1.6;
">

Review the affected metrics in the AI Business Anomaly Monitoring
dashboard and investigate the underlying business drivers.

</p>

</div>

</td>

</tr>


<!-- FOOTER -->

<tr>

<td style="
    background:#f9fafb;
    padding:20px 30px;
    text-align:center;
">

<div style="
    color:#6b7280;
    font-size:12px;
">

AI Business Anomaly Monitoring System

</div>

<div style="
    color:#9ca3af;
    font-size:11px;
    margin-top:5px;
">

Automated alert • Python • Pandas • Streamlit • Gemini

</div>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""

    msg.add_alternative(html, subtype="html")

    # -----------------------------
    # Send email
    # -----------------------------

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender, password)

        server.send_message(msg)

    return True