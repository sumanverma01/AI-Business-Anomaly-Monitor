import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range(
    start="2026-06-01",
    periods=90,
    freq="D"
)

data = []

for date in dates:

    traffic = np.random.randint(9500, 12500)
    orders = int(traffic * np.random.uniform(0.065, 0.08))

    revenue = orders * np.random.randint(140, 180)

    marketing_cost = np.random.randint(35000, 50000)

    refunds = np.random.randint(15, 30)

    data.append([
        date,
        revenue,
        orders,
        traffic,
        marketing_cost,
        refunds
    ])


df = pd.DataFrame(
    data,
    columns=[
        "Date",
        "Revenue",
        "Orders",
        "Traffic",
        "Marketing_Cost",
        "Refunds"
    ]
)


# --------------------------------
# Introduce artificial anomalies
# --------------------------------

# Traffic spike + conversion drop + refund increase

df.loc[70:72, "Traffic"] = (
    df.loc[70:72, "Traffic"] * 1.7
).round().astype(int)

df.loc[70:72, "Orders"] = (
    df.loc[70:72, "Traffic"] * 0.045
).round().astype(int)

df.loc[70:72, "Refunds"] = (
    df.loc[70:72, "Refunds"] * 2.5
).round().astype(int)


# Revenue drop

df.loc[80:82, "Revenue"] = (
    df.loc[80:82, "Revenue"] * 0.55
).round().astype(int)


# Marketing cost spike

df.loc[85:87, "Marketing_Cost"] = (
    df.loc[85:87, "Marketing_Cost"] * 2.2
).round().astype(int)


# --------------------------------
# Calculate conversion rate
# --------------------------------

df["Conversion_Rate"] = (
    df["Orders"] / df["Traffic"] * 100
)


# --------------------------------
# Save Excel file
# --------------------------------

df.to_excel(
    "data/business_data_new.xlsx",
    index=False
)


print("Dataset created successfully!")

print("\nLast 20 rows:")
print(df.tail(20))