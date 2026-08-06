🏥 Hospital Cost & Operations Analysis (Python + Interactive Dashboard)

A complete Python data analytics project that cleans messy hospital admission data, uncovers cost and operational insights, and displays them in an interactive HTML dashboard.
This project analyzes real-world-style hospital data to answer one core business question: **which departments and patient groups are driving the most cost, and where can the hospital optimize?**

* 💰 Total Cost & Avg Cost by Department
* 🛏️ Average Length of Stay
* 🔁 Readmission Rate by Department
* 👥 Cost by Age Group
* 📈 Monthly Admissions Trend
* ✅ No paid tools required — pure Python

🚀 Features
✔ End-to-end data cleaning (missing values, inconsistent naming, bad dates, duplicates)
✔ Department & age-group cost analysis
✔ Length of stay & readmission rate analysis
✔ Auto-generated business insights
✔ Interactive HTML dashboard (Chart.js) — auto-built by the script
✔ Cleaned CSV export (ready for Power BI / Tableau)
✔ Lightweight & beginner-friendly code

🛠️ Technologies Used

* Python
* Pandas & NumPy (data cleaning & analysis)
* Matplotlib & Seaborn (static charts)
* HTML / CSS / JavaScript (Chart.js) — interactive dashboard
* Power BI / Tableau — optional, using the cleaned CSV output

📂 Project Structure

```
hospital-cost-analysis/
│
├── healthcare_cost_analysis.py   # Main analysis script
├── dashboard_template.html       # Dashboard HTML/CSS/JS template
├── hospital_data.csv             # Raw input dataset
├── cleaned_hospital_data.csv     # Cleaned output dataset
├── dashboard.html                # Auto-generated interactive dashboard
└── README.md                     # Project documentation
```

📦 Installation
1️⃣ Clone this repository

```
git clone https://github.com/your-username/hospital-cost-analysis.git
```

2️⃣ Navigate to project

```
cd hospital-cost-analysis
```

3️⃣ Install dependencies

```
pip install pandas numpy matplotlib seaborn
```

▶️ How to Run

```
python healthcare_cost_analysis.py
```

Then open `dashboard.html` in your browser to view the interactive dashboard.

📡 How It Works
🔹 Step 1: Load & clean the raw dataset
Handles missing patient IDs, inconsistent department names (e.g., "Cardio" → "Cardiology"), invalid dates, currency-formatted costs, and duplicate rows.

🔹 Step 2: Analyze cost & operations
Calculates total/average cost by department, length of stay, readmission rate, and cost by age group.

🔹 Step 3: Generate insights
Auto-prints key findings, e.g.:

```
- Orthopedics has the highest total cost (₹9,727,655) across 160 patients.
- Neurology has the highest average length of stay (6.4 days).
- Gen Medicine has the highest readmission rate (19.2%).
- Top 20% of patients account for 38.2% of total hospital cost.
```

🔹 Step 4: Build the dashboard
Exports a clean CSV and generates `dashboard.html` — a self-contained interactive dashboard with KPI cards, charts, and business recommendations.

📌 Example Output

```
Hospital Cost & Operations Dashboard
Total Cost: ₹388.3L | Patients: 1,065 | Avg Length of Stay: 4.1 days
Top Cost Department: Orthopedics
Highest Readmission: Gen Medicine (19.2%)
```

❗ Error Handling
The script handles:

* Missing/invalid patient records
* Inconsistent department name spellings
* Currency-formatted or non-numeric cost values
* Invalid or unparseable dates
* Duplicate records

⭐ Future Improvements

* Add diagnosis-level cost breakdown
* Fuzzy-match department names instead of fixed lookup
* Predictive model for readmission risk
* Power BI / Tableau published dashboard link
* Dark/light theme toggle for dashboard

🤝 Contributing
Pull requests are welcome.
Feel free to suggest new features or improvements.

📜 License
This project is open-source and free to use.
