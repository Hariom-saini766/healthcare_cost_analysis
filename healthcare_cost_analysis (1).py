"""
==============================================================
PROJECT: Hospital Department Cost & Operations Analysis
Business Question: Which departments/patient groups are driving
the most cost, and where can the hospital optimize?
==============================================================

HOW TO USE THIS SCRIPT:
1. Download a hospital/healthcare dataset from Kaggle
   (search: "Healthcare Analytics dataset", "Hospital Management Dataset",
   or use data.gov.in for real Indian public health data).
2. Update the COLUMN MAPPING section below to match your dataset's
   actual column names.
3. Run cell by cell in Jupyter Notebook, or run as a full script.

Recommended libraries: pandas, numpy, matplotlib, seaborn
Install with: pip install pandas numpy matplotlib seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Plot styling
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ==============================================================
# STEP 0: LOAD DATA + COLUMN MAPPING
# ==============================================================
# Update the file path to your actual CSV file
RAW_FILE_PATH = r"C:\Users\hs639\Downloads\hospital_data.csv"

df = pd.read_csv(RAW_FILE_PATH)

# ---- COLUMN MAPPING ----
# Change the values (right side) to match YOUR dataset's actual column names.
# Keep the keys (left side) the same, since the rest of the script uses these.
COLS = {
    "patient_id": "PatientID",
    "age": "Age",
    "gender": "Gender",
    "department": "Department",
    "admission_date": "AdmissionDate",
    "discharge_date": "DischargeDate",
    "cost": "TotalCost",
    "diagnosis": "Diagnosis",
    "readmission_flag": "Readmission",   # optional; set to None if not available
}

# Rename columns to standard internal names for the rest of the script
df = df.rename(columns={v: k for k, v in COLS.items() if v in df.columns})

print("Initial shape:", df.shape)
print(df.head())
print(df.info())


# ==============================================================
# STEP 1: DATA CLEANING
# ==============================================================

# --- 1.1 Check missing values ---
print("\nMissing values per column:")
print(df.isnull().sum())

# --- 1.2 Drop rows with missing critical fields (patient_id, cost, department) ---
critical_cols = ["patient_id", "cost", "department"]
before = len(df)
df = df.dropna(subset=[c for c in critical_cols if c in df.columns])
print(f"\nDropped {before - len(df)} rows missing critical fields.")

# --- 1.3 Standardize department names (common real-world issue) ---
if "department" in df.columns:
    df["department"] = (
        df["department"]
        .astype(str)
        .str.strip()
        .str.title()
        .replace({
            "Cardio": "Cardiology",
            "Ortho": "Orthopedics",
            "Orthopaedics": "Orthopedics",
            "Gyn": "Gynecology",
            "Gynae": "Gynecology",
            "Peads": "Pediatrics",
            "Paeds": "Pediatrics",
        })
    )

# --- 1.4 Fix date columns ---
for col in ["admission_date", "discharge_date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Drop rows where dates failed to parse
if "admission_date" in df.columns and "discharge_date" in df.columns:
    before = len(df)
    df = df.dropna(subset=["admission_date", "discharge_date"])
    print(f"Dropped {before - len(df)} rows with invalid dates.")

    # --- 1.5 Calculate length of stay (LOS) ---
    df["length_of_stay"] = (df["discharge_date"] - df["admission_date"]).dt.days

    # Remove impossible values (negative or zero-day errors, extreme outliers)
    before = len(df)
    df = df[(df["length_of_stay"] >= 0) & (df["length_of_stay"] < 100)]
    print(f"Dropped {before - len(df)} rows with invalid length of stay.")

# --- 1.6 Fix cost column (remove currency symbols, negative values) ---
if "cost" in df.columns:
    if df["cost"].dtype == object:
        df["cost"] = (
            df["cost"].astype(str).str.replace(r"[^\d.]", "", regex=True)
        )
    df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
    df = df.dropna(subset=["cost"])
    df = df[df["cost"] > 0]  # remove zero/negative cost errors

# --- 1.7 Remove duplicate patient records ---
before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before - len(df)} duplicate rows.")

# --- 1.8 Age groups (useful for segmentation later) ---
if "age" in df.columns:
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df = df.dropna(subset=["age"])
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 18, 30, 45, 60, 75, 120],
        labels=["0-18", "19-30", "31-45", "46-60", "61-75", "76+"],
    )

print("\nCleaned shape:", df.shape)


# ==============================================================
# STEP 2: EXPLORATORY ANALYSIS
# ==============================================================

# --- 2.1 Average length of stay by department ---
if "length_of_stay" in df.columns:
    los_by_dept = (
        df.groupby("department")["length_of_stay"]
        .mean()
        .sort_values(ascending=False)
    )
    print("\nAverage Length of Stay by Department:\n", los_by_dept)

    plt.figure()
    los_by_dept.plot(kind="bar", color="steelblue")
    plt.title("Average Length of Stay by Department")
    plt.ylabel("Days")
    plt.xlabel("Department")
    plt.tight_layout()
    plt.savefig(r"C:\Users\hs639\Downloads\los_by_department.png")
    plt.close()

# --- 2.2 Total and average cost by department ---
cost_by_dept = (
    df.groupby("department")["cost"]
    .agg(total_cost="sum", avg_cost="mean", patient_count="count")
    .sort_values("total_cost", ascending=False)
)
print("\nCost Summary by Department:\n", cost_by_dept)

plt.figure()
cost_by_dept["total_cost"].plot(kind="bar", color="darkorange")
plt.title("Total Cost by Department")
plt.ylabel("Total Cost")
plt.xlabel("Department")
plt.tight_layout()
plt.savefig(r"C:\Users\hs639\Downloads\total_cost_by_department.png")
plt.close()

# --- 2.3 Admissions trend over time (monthly) ---
if "admission_date" in df.columns:
    df["admission_month"] = df["admission_date"].dt.to_period("M")
    monthly_admissions = df.groupby("admission_month").size()

    plt.figure()
    monthly_admissions.plot(kind="line", marker="o", color="green")
    plt.title("Monthly Admissions Trend")
    plt.ylabel("Number of Admissions")
    plt.xlabel("Month")
    plt.tight_layout()
    plt.savefig(r"C:\Users\hs639\Downloads\monthly_admissions_trend.png")
    plt.close()

# --- 2.4 Cost by age group ---
if "age_group" in df.columns:
    cost_by_age = df.groupby("age_group")["cost"].sum().sort_values(ascending=False)
    print("\nTotal Cost by Age Group:\n", cost_by_age)

    plt.figure()
    cost_by_age.plot(kind="bar", color="purple")
    plt.title("Total Cost by Age Group")
    plt.ylabel("Total Cost")
    plt.xlabel("Age Group")
    plt.tight_layout()
    plt.savefig(r"C:\Users\hs639\Downloads\cost_by_age_group.png")
    plt.close()


# ==============================================================
# STEP 3: DEEPER ANALYSIS — COST EFFICIENCY & READMISSIONS
# ==============================================================

# --- 3.1 Cost per day of stay, by department (efficiency metric) ---
if "length_of_stay" in df.columns:
    df["cost_per_day"] = df["cost"] / df["length_of_stay"].replace(0, np.nan)
    cost_efficiency = (
        df.groupby("department")["cost_per_day"]
        .mean()
        .sort_values(ascending=False)
    )
    print("\nAverage Cost per Day of Stay by Department:\n", cost_efficiency)

# --- 3.2 Readmission rate by department (if data available) ---
if "readmission_flag" in df.columns:
    df["readmission_flag"] = df["readmission_flag"].astype(str).str.lower()
    df["is_readmitted"] = df["readmission_flag"].isin(["1", "yes", "true"])

    readmission_rate = (
        df.groupby("department")["is_readmitted"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )
    print("\nReadmission Rate (%) by Department:\n", readmission_rate)

    plt.figure()
    readmission_rate.plot(kind="bar", color="crimson")
    plt.title("Readmission Rate by Department (%)")
    plt.ylabel("Readmission Rate (%)")
    plt.xlabel("Department")
    plt.tight_layout()
    plt.savefig(r"C:\Users\hs639\Downloads\readmission_rate_by_department.png")
    plt.close()

# --- 3.3 High-cost patient segment (Pareto-style check) ---
patient_cost = df.groupby("patient_id")["cost"].sum().sort_values(ascending=False)
top_20_pct_count = int(len(patient_cost) * 0.2)
top_20_pct_cost_share = patient_cost.head(top_20_pct_count).sum() / patient_cost.sum() * 100
print(f"\nTop 20% of patients account for {top_20_pct_cost_share:.1f}% of total cost.")


# ==============================================================
# STEP 4: KEY INSIGHTS SUMMARY (auto-generated text)
# ==============================================================

print("\n" + "=" * 60)
print("KEY INSIGHTS SUMMARY")
print("=" * 60)

if "length_of_stay" in df.columns:
    top_los_dept = los_by_dept.idxmax()
    print(f"- {top_los_dept} has the highest average length of stay "
          f"({los_by_dept.max():.1f} days), which may be driving higher costs.")

top_cost_dept = cost_by_dept["total_cost"].idxmax()
print(f"- {top_cost_dept} has the highest total cost "
      f"(₹{cost_by_dept['total_cost'].max():,.0f}) across "
      f"{int(cost_by_dept['patient_count'].loc[top_cost_dept])} patients.")

if "age_group" in df.columns:
    top_age_group = cost_by_age.idxmax()
    age_share = cost_by_age.max() / cost_by_age.sum() * 100
    print(f"- The {top_age_group} age group accounts for "
          f"{age_share:.1f}% of total hospital cost.")

if "readmission_flag" in df.columns:
    worst_readmit_dept = readmission_rate.idxmax()
    print(f"- {worst_readmit_dept} has the highest readmission rate "
          f"({readmission_rate.max():.1f}%), a potential cost and quality concern.")

print(f"- The top 20% of patients (by spend) account for "
      f"{top_20_pct_cost_share:.1f}% of total hospital cost.")


# ==============================================================
# STEP 5: BUSINESS RECOMMENDATIONS (write these in your README,
# customized with YOUR actual numbers once you run this on real data)
# ==============================================================
"""
Example recommendation template (fill in with your real output numbers):

1. [Department X] shows [Y]% longer average length of stay than other
   departments. Recommend reviewing discharge planning procedures to
   reduce unnecessary bed occupancy and free capacity for new admissions.

2. Patients aged [Age Group] account for [Z]% of total cost despite being
   [W]% of patient volume. Recommend a preventive care / early intervention
   program targeted at this segment to reduce high-cost admissions.

3. [Department Y] has the highest readmission rate at [R]%. Recommend a
   post-discharge follow-up call/check-in program to catch complications
   early and reduce costly readmissions.

4. The top 20% of patients drive [P]% of total cost. Recommend a case
   management program for high-cost/high-complexity patients to better
   coordinate their care and control costs.
"""

# ==============================================================
# STEP 6: EXPORT CLEANED DATA (for Power BI / Tableau dashboard)
# ==============================================================
df.to_csv("cleaned_hospital_data.csv", index=False)
print("\nCleaned dataset exported as 'cleaned_hospital_data.csv'")
print("Import this file into Power BI or Tableau to build your dashboard.")

print("\nAll chart images saved in current folder:")
print("- los_by_department.png")
print("- total_cost_by_department.png")
print("- monthly_admissions_trend.png")
print("- cost_by_age_group.png")
print("- readmission_rate_by_department.png")


# ==============================================================
# STEP 7: AUTO-GENERATE INTERACTIVE HTML DASHBOARD
# This builds a self-contained dashboard.html you can double-click
# and open in any browser -- no server, no extra setup needed.
# ==============================================================

def build_dashboard(output_path=r"C:\Users\hs639\Downloads\dashboard_template.html"):
    # ---- Gather data needed for the dashboard, as plain Python objects ----
    dept_summary = cost_by_dept.reset_index().rename(columns={"index": "department"})
    if "avg_los" not in dept_summary.columns and "length_of_stay" in df.columns:
        dept_summary["avg_los"] = dept_summary["department"].map(los_by_dept)
    dept_records = dept_summary.to_dict(orient="records")

    age_records = []
    if "age_group" in df.columns:
        age_records = (
            df.groupby("age_group", observed=True)["cost"]
            .sum()
            .reset_index()
            .rename(columns={"cost": "cost"})
            .to_dict(orient="records")
        )

    monthly_records = []
    if "admission_month" in df.columns:
        monthly_records = (
            monthly_admissions.reset_index()
            .rename(columns={0: "count", "admission_month": "month"})
        )
        monthly_records["month"] = monthly_records["month"].astype(str)
        monthly_records = monthly_records.to_dict(orient="records")

    readmit_records = []
    if "readmission_flag" in df.columns:
        readmit_records = (
            readmission_rate.reset_index()
            .rename(columns={"is_readmitted": "rate"})
            .to_dict(orient="records")
        )

    dashboard_data = {
        "deptCost": dept_records,
        "ageCost": age_records,
        "monthly": monthly_records,
        "readmit": readmit_records,
        "top20Share": round(top_20_pct_cost_share, 1),
        "totalPatients": int(df["patient_id"].nunique()),
        "totalCost": float(df["cost"].sum()),
        "avgCost": float(df["cost"].mean()),
        "avgLOS": float(df["length_of_stay"].mean()) if "length_of_stay" in df.columns else None,
    }

    data_json = json.dumps(dashboard_data, default=str)

    # Read the HTML template from a separate file (dashboard_template.html
    # must be in the same folder as this script). Keeping the template in
    # its own file avoids Python string-quoting issues entirely.
    import os
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    html_output = html_template.replace("__DATA_JSON__", data_json)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"\nInteractive dashboard generated: {output_path}")
    print("Double-click this file (or open it in any browser) to view your dashboard.")
    return

build_dashboard(r"C:\Users\hs639\Downloads\dashboard_template.html")
