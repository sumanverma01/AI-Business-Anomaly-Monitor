import pandas as pd
from anomaly_detector import detect_anomalies
from anomaly_detector import calculate_severity
from ai_analyzer import analyze_anomaly



def format_change(value):
    """Format percentage change."""

    if pd.isna(value):
        return "N/A"

    return f"{value:+.1f}%"


def generate_business_summary(row):

    findings = []
    recommendations = []

    # -----------------------------
    # Revenue
    # -----------------------------

    revenue_change = row["Revenue_Change"]

    if not pd.isna(revenue_change):

        if revenue_change > 20:
            findings.append(
                f"Revenue increased significantly "
                f"({format_change(revenue_change)})."
            )

        elif revenue_change < -20:
            findings.append(
                f"Revenue declined significantly "
                f"({format_change(revenue_change)})."
            )

            recommendations.append(
                "Review recent sales performance and "
                "possible causes of the revenue decline."
            )


    # -----------------------------
    # Traffic
    # -----------------------------

    traffic_change = row["Traffic_Change"]

    if not pd.isna(traffic_change):

        if traffic_change > 20:
            findings.append(
                f"Website traffic increased sharply "
                f"({format_change(traffic_change)})."
            )

            recommendations.append(
                "Check which traffic sources or marketing "
                "campaigns caused the increase."
            )

        elif traffic_change < -20:
            findings.append(
                f"Website traffic dropped significantly "
                f"({format_change(traffic_change)})."
            )

            recommendations.append(
                "Review website traffic sources and "
                "recent marketing activity."
            )


    # -----------------------------
    # Conversion Rate
    # -----------------------------

    conversion_change = row["Conversion_Rate_Change"]

    if not pd.isna(conversion_change):

        if conversion_change < -20:

            findings.append(
                f"Conversion rate decreased sharply "
                f"({format_change(conversion_change)})."
            )

            recommendations.append(
                "Check the checkout process, website "
                "performance, and traffic quality."
            )

        elif conversion_change > 20:

            findings.append(
                f"Conversion rate improved significantly "
                f"({format_change(conversion_change)})."
            )


    # -----------------------------
    # Refunds
    # -----------------------------

    refunds_change = row["Refunds_Change"]

    if not pd.isna(refunds_change):

        if refunds_change > 20:

            findings.append(
                f"Refunds increased significantly "
                f"({format_change(refunds_change)})."
            )

            recommendations.append(
                "Review recent refund reasons and "
                "customer complaints."
            )


    # -----------------------------
    # Marketing Cost
    # -----------------------------

    marketing_change = row["Marketing_Cost_Change"]

    if not pd.isna(marketing_change):

        if marketing_change > 20:

            findings.append(
                f"Marketing cost increased "
                f"({format_change(marketing_change)})."
            )

            recommendations.append(
                "Check whether the additional marketing "
                "spend is generating proportional revenue."
            )


    # -----------------------------
    # Orders
    # -----------------------------

    orders_change = row["Orders_Change"]

    if not pd.isna(orders_change):

        if orders_change < -20:

            findings.append(
                f"Orders decreased significantly "
                f"({format_change(orders_change)})."
            )

            recommendations.append(
                "Review product availability, pricing, "
                "and checkout performance."
            )


    # -----------------------------
    # Overall Summary
    # -----------------------------

    if not findings:

        summary = (
            "No significant business anomalies were detected."
        )

    else:

        summary = " ".join(findings)


    # Remove duplicate recommendations
    recommendations = list(
        dict.fromkeys(recommendations)
    )


    return summary, recommendations


def generate_report(df):

    reports = []

    for _, row in df.iterrows():

        if row["Severity"] == "NORMAL":
            continue

        summary, recommendations = (
            generate_business_summary(row)
        )

        report = {

            "Date": row["Date"],

            "Severity": row["Severity"],

            "Summary": summary,

            "Recommendations": recommendations

        }

        reports.append(report)

    return reports


if __name__ == "__main__":

  

    # Load dataset
    df = pd.read_excel(
        "data/business_data_new.xlsx"
    )

    # Detect anomalies
    df = detect_anomalies(df)

    # Calculate severity
    df["Severity"] = df.apply(
        calculate_severity,
        axis=1
    )

    # Select anomaly days
    anomaly_days = df[
        df["Severity"] != "NORMAL"
    ]

    print("\n")
    print("=" * 70)
    print("AI BUSINESS ANOMALY ANALYSIS")
    print("=" * 70)

    for _, row in anomaly_days.iterrows():

        print("\nDate:", row["Date"])
        print("Severity:", row["Severity"])

        print("\nDetected Changes:")

        print(
            f"Revenue: {row['Revenue_Change']:.1f}%"
        )

        print(
            f"Orders: {row['Orders_Change']:.1f}%"
        )

        print(
            f"Traffic: {row['Traffic_Change']:.1f}%"
        )

        print(
            f"Conversion Rate: "
            f"{row['Conversion_Rate_Change']:.1f}%"
        )

        print(
            f"Marketing Cost: "
            f"{row['Marketing_Cost_Change']:.1f}%"
        )

        print(
            f"Refunds: {row['Refunds_Change']:.1f}%"
        )

        print("\nAI BUSINESS ANALYSIS:")

        try:

            analysis = analyze_anomaly(row)

            print(analysis)

        except Exception as e:

            print(
                "AI analysis failed:",
                e
            )

        print("-" * 70)