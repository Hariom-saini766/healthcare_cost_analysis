# Hospital Department Cost & Operations Analysis

A Python script that cleans raw hospital admission data, analyzes cost and operational patterns across departments, and auto-generates an interactive HTML dashboard — no Power BI/Tableau license required to view the results.

---

## 1. Business Question

**Which departments and patient groups are driving the most cost, and where can the hospital optimize?**

The analysis answers this by looking at:
- Cost and length-of-stay by department
- Admission trends over time
- Cost by age group
- Cost efficiency (cost per day of stay)
- Readmission rates by department
- The "top 20% of patients" cost concentration (Pareto check)

---

## 2. What This Project Produces

| Output | Description |
|---|---|
| `cleaned_hospital_data.csv` | Cleaned, de-duplicated dataset ready for BI tools |
| `los_by_department.png` | Bar chart — average length of stay by department |
| `total_cost_by_department.png` | Bar chart — total cost by department |
| `monthly_admissions_trend.png` | Line chart — admissions over time |
| `cost_by_age_group.png` | Bar chart — total cost by age group |
| `readmission_rate_by_department.png` | Bar chart — readmission % by department (if data available) |
| `dashboard_template.html` | Self-contained interactive dashboard (double-click to open in any browser) |
| Console output | Printed summary stats + auto-generated key insights |

---

## 3. Requirements

**Python libraries:**
```bash
pip install pandas numpy matplotlib seaborn
```

**Input data:**
A hospital/healthcare CSV dataset. Suggested sources:
- Kaggle — search "Healthcare Analytics dataset" or "Hospital Management Dataset"
- [data.gov.in](https://data.gov.in) — real Indian public health data

**A dashboard template file:**
`dashboard_template.html` must exist in the same folder as the script (Step 7 reads it and injects the computed data into it as JSON).

---

## 4. Setup & Usage

### Step 1 — Download data
Get a hospital dataset with, at minimum, columns for patient ID, cost, and department.

### Step 2 — Update file paths
Edit these two lines near the top/bottom of the script to point at your machine:
```python
RAW_FILE_PATH = r"C:\Users\hs639\Downloads\hospital_data.csv"   # your input file
...
build_dashboard(r"C:\Users\hs639\Downloads\dashboard_template.html")  # your output path
```

### Step 3 — Map your columns
Your dataset's column names almost certainly won't match the script's internal names. Update only the **right-hand side** of `COLS`:

```python
COLS = {
    "patient_id": "PatientID",        # <- change this to your actual column name
    "age": "Age",
    "gender": "Gender",
    "department": "Department",
    "admission_date": "AdmissionDate",
    "discharge_date": "DischargeDate",
    "cost": "TotalCost",
    "diagnosis": "Diagnosis",
    "readmission_flag": "Readmission",  # optional — set to None if you don't have this
}
```

### Step 4 — Run it
```bash
python healthcare_cost_analysis.py
```
Or run cell-by-cell in Jupyter for easier inspection at each stage.

---

## 5. How the Script Works (Pipeline Stages)

### Step 0 — Load Data + Column Mapping
Reads the raw CSV and renames columns to standardized internal names so the rest of the script doesn't care what your source column headers were called.

### Step 1 — Data Cleaning
- Drops rows missing critical fields (patient ID, cost, department)
- Standardizes messy department names (e.g. "Cardio", "Ortho" → "Cardiology", "Orthopedics")
- Parses admission/discharge dates, drops unparseable rows
- Calculates **length of stay** and removes impossible values (negative or >100 days)
- Cleans the cost column (strips currency symbols, removes zero/negative values)
- Removes duplicate rows
- Buckets patients into age groups: `0-18, 19-30, 31-45, 46-60, 61-75, 76+`

### Step 2 — Exploratory Analysis
- Average length of stay by department
- Total/average cost and patient count by department
- Monthly admission trend
- Total cost by age group

### Step 3 — Deeper Analysis
- **Cost efficiency**: average cost per day of stay, by department
- **Readmission rate** by department (only if readmission data exists)
- **Pareto check**: what % of total cost comes from the top 20% of patients by spend

### Step 4 — Auto-Generated Insights
Prints a plain-English summary using the actual numbers from your dataset (highest-cost department, highest-LOS department, worst readmission rate, top-20% cost share, etc.)

### Step 5 — Business Recommendations Template
A commented-out template reminding you to translate the Step 4 numbers into recommendations for a README or stakeholder report.

### Step 6 — Export
Saves the cleaned dataset as `cleaned_hospital_data.csv` for import into Power BI, Tableau, or any other BI tool.

### Step 7 — Interactive HTML Dashboard
Packages all computed summaries (department cost, age cost, monthly admissions, readmission rates, top-20% share, totals) into a JSON blob, then injects that JSON into `dashboard_template.html` in place of a `__DATA_JSON__` placeholder — producing a single, shareable HTML file with no server needed.

---

## 6. Notes, Assumptions & Known Limitations

- **File paths are hardcoded** to a specific Windows user folder (`C:\Users\hs639\Downloads\...`). Update these before running on another machine.
- **`readmission_flag` is optional.** If your dataset doesn't have it, set `"readmission_flag": None` in `COLS` — related steps (3.2, readmission chart, readmission insight) are skipped automatically.
- **Length of stay filter** discards any stay ≥ 100 days as a likely data error — adjust this threshold if your dataset legitimately includes long-term care.
- **Currency symbol stripping** on the cost column assumes cost is stored as text with symbols/commas (e.g. `"₹12,000"`). If your cost column is already numeric, this step is a no-op.
- **`dashboard_template.html` is a separate required file** — the script will fail at Step 7 if it's missing from the same directory as the script.
- Charts are saved as static `.png` files in the current working directory, not displayed inline (useful for headless/script runs, less convenient in Jupyter — add `plt.show()` if you want inline plots too).

---

## 7. Suggested Folder Structure

```
project/
├── healthcare_cost_analysis.py
├── dashboard_template.html
├── hospital_data.csv              (your raw input)
├── cleaned_hospital_data.csv      (generated)
├── dashboard_template.html        (generated output, overwrites input template if same path)
└── *.png                          (generated charts)
```

> ⚠️ Note: the input template and output dashboard currently share a similar name/path (`dashboard_template.html`). Consider renaming the **output** file (e.g. `dashboard_output.html`) to avoid overwriting your source template.
