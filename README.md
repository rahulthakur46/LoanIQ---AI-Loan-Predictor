# 💎 LoanIQ — AI Loan Approval Predictor

<p align="center">
  <img width="1920" height="1080" alt="Screenshot 2026-06-12 012647" src="https://github.com/user-attachments/assets/93882f32-8a45-4349-befe-50b911b411dd" />

  <img width="1920" height="1080" alt="Screenshot 2026-06-12 012706" src="https://github.com/user-attachments/assets/c6239ded-27fa-4810-8ccc-104617dc952d" />

  <img width="1920" height="1080" alt="Screenshot 2026-06-12 012724" src="https://github.com/user-attachments/assets/66d42beb-e0a3-45af-a0a7-f741763ddffc" />

  <img width="1920" height="1080" alt="Screenshot 2026-06-12 012737" src="https://github.com/user-attachments/assets/6a259f40-17c5-41e7-8eea-b78dad455222" />

</p>


> **An AI-powered loan eligibility prediction platform** built with Random Forest and Streamlit.  
> Instantly predicts whether a loan application will be **Approved** or **Rejected** — with confidence scores, risk analysis, and interactive data visualizations.

---

**Created by — Rahul Thakur**

---

## 🚀 Features

- 🎯 **Instant Prediction** — Enter applicant details and get an AI decision in seconds
- 📊 **Confidence Gauge** — Visual confidence score for every prediction
- ⚠️ **Risk Analysis** — Automatic DTI ratio, LTV ratio, and risk chip analysis
- 💡 **Smart Presets** — One-click example profiles (Salaried, Self-Employed, High Income, Fresh Graduate)
- 📈 **Data Insights Tab** — Approval split, CIBIL distribution, Income vs Loan scatter, Education breakdown
- 🔍 **Feature Importance Tab** — See exactly what the model cares about most
- 💎 **Premium Dark UI** — Deep navy × electric gold theme, fully responsive

---

## 📁 Project Structure

```
RF-Loan Approval/
│
├── loan_approval_app.py                 # Main Streamlit application
├── model_bundle.pkl                     # Pre-trained Random Forest model + encoders
├── loan_approval_dataset_download.csv   # Dataset (4,269 loan records)
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
```

---

## ⚙️ Installation & Setup

### 1. Clone or Download the Project

Download all files and place them in the **same folder**.

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run loan_approval_app.py
```

The app will open automatically at **http://localhost:8501**

---

## 🧠 Model Details

| Property | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Number of Trees | 100 |
| Test Accuracy | **97.78%** |
| Training Samples | 4,269 |
| Features Used | 11 |
| Target | Loan Approved / Rejected |

### Input Features

| Feature | Description |
|---|---|
| `no_of_dependents` | Number of financial dependents |
| `education` | Graduate / Not Graduate |
| `self_employed` | Yes / No |
| `income_annum` | Annual income (₹) |
| `loan_amount` | Requested loan amount (₹) |
| `loan_term` | Loan term in years |
| `cibil_score` | Credit score (300–900) |
| `residential_assets_value` | Value of residential property (₹) |
| `commercial_assets_value` | Value of commercial property (₹) |
| `luxury_assets_value` | Value of luxury assets (₹) |
| `bank_asset_value` | Bank balance / assets (₹) |

---

## 📊 Dataset

- **Source:** Loan Approval Dataset
- **Records:** 4,269 loan applications
- **Approval Rate:** ~62% Approved, ~38% Rejected
- **Class Balance:** Reasonably balanced — no oversampling needed

---

## 🗂️ App Tabs Overview

### 🎯 Tab 1 — Predict Eligibility
Fill in the applicant's personal, financial, and asset details. Click **Predict** to get:
- Approved / Rejected decision with confidence %
- Animated gauge chart
- Risk chips (CIBIL risk, DTI risk, LTV risk)
- EMI estimate, DTI ratio, LTV ratio

### 📊 Tab 2 — Data Insights
Explore the training dataset visually:
- Approval donut chart
- CIBIL score distribution (Approved vs Rejected)
- Income vs Loan Amount scatter plot
- Education vs Loan Status grouped bar
- Raw data table with adjustable row count

### 🔍 Tab 3 — Feature Importance
Understand what drives loan decisions:
- Full feature importance bar chart (gradient colored)
- Top-3 features with medal cards
- CIBIL score band → Approval rate bar chart

---

## 💻 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Web application framework |
| Scikit-learn | Random Forest model |
| Plotly | Interactive charts |
| Pandas | Data manipulation |
| NumPy | Numerical operations |

---

## 🛠️ Troubleshooting

**App not starting?**
```bash
# Make sure you're in the correct folder
cd "C:\Users\YourName\RF-Loan Approval"
streamlit run loan_approval_app.py
```

**Module not found error?**
```bash
pip install -r requirements.txt
```

**Port already in use?**
```bash
streamlit run loan_approval_app.py --server.port 8503
```

**All 3 files must be in the same folder:**
```
✅ loan_approval_app.py
✅ model_bundle.pkl
✅ loan_approval_dataset_download.csv
```

---

## 📄 License

This project is created for educational and demonstration purposes.

---

<p align="center">
  Made with ❤️ by <strong>Rahul Thakur</strong> &nbsp;·&nbsp; Powered by Random Forest + Streamlit
</p>
