import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_anomaly(row):

    prompt = f"""
You are a business data analyst.

Analyze the following detected business anomaly.

Date:
{row["Date"]}

Severity:
{row["Severity"]}

Revenue change:
{row["Revenue_Change"]:.1f}%

Orders change:
{row["Orders_Change"]:.1f}%

Traffic change:
{row["Traffic_Change"]:.1f}%

Conversion rate change:
{row["Conversion_Rate_Change"]:.1f}%

Marketing cost change:
{row["Marketing_Cost_Change"]:.1f}%

Refunds change:
{row["Refunds_Change"]:.1f}%

Your task:

1. Explain what changed.
2. Explain why these changes may matter to the business.
3. Give possible causes, clearly labeling them as possibilities.
4. Give 2-3 recommended investigation steps.

Important:
- Do not invent facts.
- Do not claim a possible cause is confirmed.
- Use only the provided data.
- Keep the response concise and business-friendly.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text