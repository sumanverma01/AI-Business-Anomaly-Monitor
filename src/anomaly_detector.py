import pandas as pd


def detect_anomalies(df):

    metrics = [
        "Revenue",
        "Orders",
        "Traffic",
        "Conversion_Rate",
        "Marketing_Cost",
        "Refunds"
    ]

    for metric in metrics:

        # Previous 7-day average
        baseline = (
            df[metric]
            .rolling(window=7)
            .mean()
            .shift(1)
        )

        # Store baseline
        df[f"{metric}_Baseline"] = baseline

        # Percentage change
        df[f"{metric}_Change"] = (
            (df[metric] - baseline) / baseline
        ) * 100

        # Detect anomaly
        df[f"{metric}_Anomaly"] = (
            df[f"{metric}_Change"].abs() > 20
        )

    return df


def calculate_severity(row):

    anomaly_count = 0

    for metric in [
        "Revenue",
        "Orders",
        "Traffic",
        "Conversion_Rate",
        "Marketing_Cost",
        "Refunds"
    ]:

        if row[f"{metric}_Anomaly"]:
            anomaly_count += 1

    if anomaly_count == 0:
        return "NORMAL"

    elif anomaly_count == 1:
        return "WATCH"

    elif anomaly_count == 2:
        return "MEDIUM"

    else:
        return "HIGH"


if __name__ == "__main__":

    # Load Excel file
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

    # Show anomaly days
    anomaly_days = df[
        df["Severity"] != "NORMAL"
    ]

    print("\nMULTI-METRIC ANOMALY REPORT")
    print("=" * 70)

    print(
        anomaly_days[
            [
                "Date",
                "Severity",
                "Revenue_Change",
                "Orders_Change",
                "Traffic_Change",
                "Conversion_Rate_Change",
                "Marketing_Cost_Change",
                "Refunds_Change"
            ]
        ].to_string(index=False)
    )