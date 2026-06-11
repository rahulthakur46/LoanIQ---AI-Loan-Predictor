import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="LoanIQ — AI Loan Predictor",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CUSTOM CSS — Deep navy × electric gold theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── Root & Reset ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #050d1a 0%, #0a1628 40%, #0d1f3c 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060e1f 0%, #0b1730 100%);
    border-right: 1px solid rgba(250,196,0,0.15);
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FAC400;
}

/* ── Main header ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #FAC400 0%, #FFF176 50%, #FAC400 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    line-height: 1.1;
    text-align: center;
    margin-bottom: 0.2rem;
}

.hero-subtitle {
    color: rgba(255,255,255,0.55);
    font-size: 1.05rem;
    text-align: center;
    letter-spacing: 0.3px;
    margin-bottom: 2rem;
    font-weight: 300;
}

.creator-badge {
    display: inline-block;
    background: linear-gradient(90deg, rgba(250,196,0,0.15), rgba(250,196,0,0.05));
    border: 1px solid rgba(250,196,0,0.4);
    border-radius: 50px;
    padding: 4px 18px;
    color: #FAC400;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    text-align: center;
}

/* ── Metric cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1.8rem;
}

.metric-card {
    background: linear-gradient(135deg, rgba(250,196,0,0.07) 0%, rgba(255,255,255,0.03) 100%);
    border: 1px solid rgba(250,196,0,0.18);
    border-radius: 16px;
    padding: 20px 18px;
    transition: border-color 0.25s;
}

.metric-card:hover { border-color: rgba(250,196,0,0.45); }

.metric-label {
    color: rgba(255,255,255,0.45);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.metric-value {
    color: #FAC400;
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
}

.metric-sub {
    color: rgba(255,255,255,0.35);
    font-size: 0.72rem;
    margin-top: 3px;
}

/* ── Section labels ── */
.section-label {
    color: #FAC400;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    border-left: 3px solid #FAC400;
    padding-left: 10px;
}

/* ── Input cards ── */
.input-section {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px 20px;
    margin-bottom: 16px;
}

/* ── Streamlit input overrides ── */
.stSlider > div > div > div {
    background: #FAC400 !important;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: white !important;
    border-radius: 10px !important;
}

.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: white !important;
    border-radius: 10px !important;
}

label, .stSlider label {
    color: rgba(255,255,255,0.75) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── Predict button ── */
.stButton > button {
    background: linear-gradient(90deg, #FAC400, #FFD740) !important;
    color: #050d1a !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.75rem 2.5rem !important;
    width: 100% !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 24px rgba(250,196,0,0.35) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(250,196,0,0.55) !important;
}

/* ── Result card ── */
.result-approved {
    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(5,150,105,0.06));
    border: 2px solid rgba(16,185,129,0.5);
    border-radius: 20px;
    padding: 28px;
    text-align: center;
}

.result-rejected {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.06));
    border: 2px solid rgba(239,68,68,0.5);
    border-radius: 20px;
    padding: 28px;
    text-align: center;
}

.result-emoji { font-size: 3rem; margin-bottom: 8px; }

.result-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 4px;
}

.result-prob {
    font-size: 0.9rem;
    opacity: 0.65;
    margin-top: 6px;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 1px solid rgba(250,196,0,0.15);
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(255,255,255,0.5) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    border-radius: 8px 8px 0 0 !important;
    border: none !important;
    padding: 10px 18px !important;
}

.stTabs [aria-selected="true"] {
    color: #FAC400 !important;
    border-bottom: 2px solid #FAC400 !important;
}

/* ── Divider ── */
hr { border-color: rgba(250,196,0,0.12) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #050d1a; }
::-webkit-scrollbar-thumb { background: rgba(250,196,0,0.3); border-radius: 3px; }

/* ── Info/warning boxes ── */
.stAlert {
    background: rgba(250,196,0,0.08) !important;
    border: 1px solid rgba(250,196,0,0.3) !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,0.8) !important;
}

.risk-chip {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin: 2px;
}

.risk-low { background: rgba(16,185,129,0.2); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.4); }
.risk-med { background: rgba(245,158,11,0.2); color: #FCD34D; border: 1px solid rgba(245,158,11,0.4); }
.risk-high { background: rgba(239,68,68,0.2); color: #FCA5A5; border: 1px solid rgba(239,68,68,0.4); }

.footer-bar {
    text-align: center;
    padding: 20px 0 8px;
    color: rgba(255,255,255,0.2);
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: 2rem;
}

.footer-bar span { color: #FAC400; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# LOAD MODEL
# ──────────────────────────────────────────────
@st.cache_resource
def load_model():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model_bundle.pkl")
    with open(model_path, "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_dataset():
    import os
    # Look for CSV in the same folder as this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "loan_approval_dataset_download.csv")
    df = pd.read_csv(csv_path)

    df.columns = df.columns.str.strip()

    df["loan_status"] = df["loan_status"].astype(str).str.strip()
    df["education"] = df["education"].astype(str).str.strip()
    df["self_employed"] = df["self_employed"].astype(str).str.strip()
    return df

bundle = load_model()
model = bundle["model"]
le_edu = bundle["le_edu"]
le_emp = bundle["le_emp"]
le_status = bundle["le_status"]
MODEL_ACCURACY = bundle["accuracy"]

df_raw = load_dataset()

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:18px 0 10px;'>
        <div style='font-size:2.6rem;'>💎</div>
        <div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#FAC400;'>LoanIQ</div>
        <div style='color:rgba(255,255,255,0.4);font-size:0.72rem;letter-spacing:1.5px;text-transform:uppercase;'>AI Loan Intelligence</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 Model Info")
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom:10px;">
        <div class="metric-label">Algorithm</div>
        <div style="color:white;font-weight:600;font-size:0.95rem;">Random Forest</div>
    </div>
    <div class="metric-card" style="margin-bottom:10px;">
        <div class="metric-label">Accuracy</div>
        <div class="metric-value">{MODEL_ACCURACY*100:.1f}%</div>
    </div>
    <div class="metric-card" style="margin-bottom:10px;">
        <div class="metric-label">Training Samples</div>
        <div style="color:white;font-weight:600;font-size:0.95rem;">{len(df_raw):,}</div>
    </div>
    <div class="metric-card" style="margin-bottom:20px;">
        <div class="metric-label">Features</div>
        <div style="color:white;font-weight:600;font-size:0.95rem;">11 Inputs</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Fill")
    profile = st.selectbox("Load example profile", 
        ["— Custom —", "👔 Salaried Graduate", "🏪 Self-Employed", "💼 High Income Pro", "🎓 Fresh Graduate"])

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:rgba(255,255,255,0.3);font-size:0.72rem;text-align:center;'>
        Built for educational purposes<br>Not financial advice
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PROFILE PRESETS
# ──────────────────────────────────────────────
presets = {
    "👔 Salaried Graduate": dict(deps=1, edu="Graduate", emp="No", income=7500000, loan=10000000, term=10, cibil=750, res=8000000, com=5000000, lux=3000000, bank=4000000),
    "🏪 Self-Employed":     dict(deps=2, edu="Not Graduate", emp="Yes", income=4000000, loan=6000000, term=8, cibil=640, res=3000000, com=7000000, lux=1500000, bank=2000000),
    "💼 High Income Pro":   dict(deps=0, edu="Graduate", emp="No", income=15000000, loan=20000000, term=20, cibil=800, res=15000000, com=10000000, lux=8000000, bank=9000000),
    "🎓 Fresh Graduate":    dict(deps=0, edu="Graduate", emp="No", income=2500000, loan=4000000, term=5, cibil=580, res=500000, com=0, lux=200000, bank=300000),
}

p = presets.get(profile, None)

# ──────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────
st.markdown('<div class="hero-title">LoanIQ</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-powered loan eligibility intelligence — instant, explainable, precise.</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center"><div class="creator-badge">✦ Created by Rahul Thakur ✦</div></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATASET METRICS BAR
# ──────────────────────────────────────────────
approved_pct = (df_raw["loan_status"] == "Approved").mean() * 100
avg_cibil = df_raw["cibil_score"].mean()
avg_income = df_raw["income_annum"].mean()

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Model Accuracy</div>
        <div class="metric-value">{MODEL_ACCURACY*100:.1f}%</div>
        <div class="metric-sub">Random Forest · 100 trees</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Dataset Size</div>
        <div class="metric-value">{len(df_raw):,}</div>
        <div class="metric-sub">Loan applications</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Approval Rate</div>
        <div class="metric-value">{approved_pct:.0f}%</div>
        <div class="metric-sub">Historical average</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Avg CIBIL Score</div>
        <div class="metric-value">{avg_cibil:.0f}</div>
        <div class="metric-sub">Credit benchmark</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎯  Predict Eligibility", "📊  Data Insights", "🔍  Feature Importance"])


# ══════════════════════════════════════════════
# TAB 1 — PREDICTION
# ══════════════════════════════════════════════
with tab1:
    col_form, col_result = st.columns([1.1, 0.9], gap="large")

    with col_form:
        # ── Personal Info ──
        st.markdown('<div class="section-label">Personal Information</div>', unsafe_allow_html=True)
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                deps = st.slider("Number of Dependents", 0, 5, p["deps"] if p else 1)
                edu = st.selectbox("Education", ["Graduate", "Not Graduate"], index=0 if (p is None or p["edu"]=="Graduate") else 1)
            with c2:
                emp = st.selectbox("Self Employed?", ["No", "Yes"], index=0 if (p is None or p["emp"]=="No") else 1)
                cibil = st.slider("CIBIL Score", 300, 900, p["cibil"] if p else 700)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Financial Info ──
        st.markdown('<div class="section-label">Financial Details</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            income = st.number_input("Annual Income (₹)", min_value=0, max_value=100000000, 
                                     value=p["income"] if p else 5000000, step=100000, format="%d")
            loan_amt = st.number_input("Loan Amount (₹)", min_value=0, max_value=200000000, 
                                        value=p["loan"] if p else 8000000, step=100000, format="%d")
        with c4:
            loan_term = st.slider("Loan Term (years)", 2, 20, p["term"] if p else 10)
            st.markdown(f"""
            <div style="background:rgba(250,196,0,0.07);border:1px solid rgba(250,196,0,0.2);border-radius:10px;padding:12px 14px;margin-top:4px;">
                <div style="color:rgba(255,255,255,0.45);font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;">EMI Estimate</div>
                <div style="color:#FAC400;font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;">
                    ₹{(loan_amt * 0.009):.0f}<span style="font-size:0.75rem;color:rgba(255,255,255,0.4);font-family:Space Grotesk,sans-serif;">/mo</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Assets ──
        st.markdown('<div class="section-label">Asset Portfolio</div>', unsafe_allow_html=True)
        c5, c6 = st.columns(2)
        with c5:
            res_val   = st.number_input("Residential Assets (₹)", 0, 500000000, p["res"] if p else 5000000, 100000, format="%d")
            com_val   = st.number_input("Commercial Assets (₹)", 0, 500000000, p["com"] if p else 3000000, 100000, format="%d")
        with c6:
            lux_val   = st.number_input("Luxury Assets (₹)", 0, 500000000, p["lux"] if p else 1000000, 100000, format="%d")
            bank_val  = st.number_input("Bank Assets (₹)", 0, 500000000, p["bank"] if p else 2000000, 100000, format="%d")

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("⚡ Predict Loan Eligibility")

    # ── Result Panel ──
    with col_result:
        st.markdown('<div class="section-label">Prediction Result</div>', unsafe_allow_html=True)

        if predict_btn:
            # Direct mapping avoids LabelEncoder whitespace issues
            edu_map = {v.strip(): i for i, v in enumerate(le_edu.classes_)}
            emp_map = {v.strip(): i for i, v in enumerate(le_emp.classes_)}
            edu_enc = edu_map.get(edu, 0)
            emp_enc = emp_map.get(emp, 0)

            features_in = np.array([[deps, edu_enc, emp_enc, income, loan_amt, loan_term,
                                      cibil, res_val, com_val, lux_val, bank_val]])

            with st.spinner(""):
                time.sleep(0.6)
                proba = model.predict_proba(features_in)[0]
                pred_idx = np.argmax(proba)
                pred_label = le_status.classes_[pred_idx].strip()
                confidence = proba[pred_idx] * 100

            approved = pred_label == "Approved"
            color = "#10B981" if approved else "#EF4444"
            emoji = "✅" if approved else "❌"
            css_class = "result-approved" if approved else "result-rejected"

            st.markdown(f"""
            <div class="{css_class}">
                <div class="result-emoji">{emoji}</div>
                <div class="result-label" style="color:{color};">{pred_label}</div>
                <div style="color:rgba(255,255,255,0.6);font-size:0.9rem;margin-top:4px;">Confidence: <strong style="color:{color};">{confidence:.1f}%</strong></div>
                <div class="result-prob">Model accuracy: {MODEL_ACCURACY*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=confidence,
                number={"suffix": "%", "font": {"color": color, "size": 36, "family": "Syne"}},
                title={"text": "Confidence Score", "font": {"color": "rgba(255,255,255,0.6)", "size": 13}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.2)", "tickfont": {"color": "rgba(255,255,255,0.4)"}},
                    "bar": {"color": color, "thickness": 0.3},
                    "bgcolor": "rgba(255,255,255,0.04)",
                    "bordercolor": "rgba(255,255,255,0.08)",
                    "steps": [
                        {"range": [0, 50], "color": "rgba(239,68,68,0.1)"},
                        {"range": [50, 75], "color": "rgba(245,158,11,0.1)"},
                        {"range": [75, 100], "color": "rgba(16,185,129,0.1)"},
                    ],
                    "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.75, "value": confidence}
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=230,
                margin=dict(t=40, b=10, l=20, r=20),
                font={"family": "Space Grotesk"}
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # ── Risk Factors ──
            st.markdown('<div class="section-label" style="margin-top:16px;">Risk Analysis</div>', unsafe_allow_html=True)
            
            dti = (loan_amt / (income + 1)) * 100
            total_assets = res_val + com_val + lux_val + bank_val
            ltv = (loan_amt / (total_assets + 1)) * 100

            factors = []
            if cibil >= 750:  factors.append(("✦ Excellent CIBIL Score", "low"))
            elif cibil >= 650: factors.append(("⚠ Average CIBIL Score", "med"))
            else: factors.append(("✗ Poor CIBIL Score", "high"))

            if dti < 40: factors.append(("✦ Healthy Debt-to-Income", "low"))
            elif dti < 70: factors.append(("⚠ Moderate DTI Ratio", "med"))
            else: factors.append(("✗ High Debt-to-Income", "high"))

            if ltv < 60: factors.append(("✦ Strong Asset Coverage", "low"))
            elif ltv < 80: factors.append(("⚠ Moderate LTV Ratio", "med"))
            else: factors.append(("✗ High Loan-to-Value", "high"))

            if edu == "Graduate": factors.append(("✦ Graduate Profile", "low"))
            if emp == "Yes": factors.append(("⚠ Self-Employed", "med"))

            html_chips = "".join([f'<span class="risk-chip risk-{r}">{label}</span>' for label, r in factors])
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:16px;line-height:2.2;">
                {html_chips}
            </div>
            """, unsafe_allow_html=True)

            # ── Key Ratios ──
            st.markdown('<div class="section-label" style="margin-top:16px;">Key Ratios</div>', unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1:
                st.metric("DTI Ratio", f"{dti:.1f}%", delta="Low risk" if dti < 40 else "High risk", delta_color="normal" if dti < 40 else "inverse")
            with r2:
                st.metric("LTV Ratio", f"{ltv:.1f}%", delta="Safe" if ltv < 60 else "Risky", delta_color="normal" if ltv < 60 else "inverse")
            with r3:
                st.metric("Assets (₹)", f"{total_assets/1e6:.1f}M")

        else:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.03);border:1px dashed rgba(250,196,0,0.25);border-radius:20px;padding:60px 30px;text-align:center;">
                <div style="font-size:3rem;margin-bottom:16px;">🎯</div>
                <div style="color:rgba(255,255,255,0.5);font-size:1rem;">Fill in the applicant details and click<br><strong style="color:#FAC400;">Predict Loan Eligibility</strong></div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — DATA INSIGHTS
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">Dataset Explorer</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    
    with c1:
        # Approval distribution donut
        status_counts = df_raw["loan_status"].value_counts()
        fig_donut = go.Figure(go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.65,
            marker_colors=["#10B981", "#EF4444"],
            textinfo="none",
        ))
        fig_donut.add_annotation(text=f"{approved_pct:.0f}%<br><span style='font-size:11px;'>Approved</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=22, color="#FAC400", family="Syne"))
        fig_donut.update_layout(
            title=dict(text="Loan Approval Split", font=dict(color="rgba(255,255,255,0.7)", size=14)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
            height=300, margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        # CIBIL score distribution
        approved_cibil = df_raw[df_raw["loan_status"]=="Approved"]["cibil_score"]
        rejected_cibil = df_raw[df_raw["loan_status"]=="Rejected"]["cibil_score"]
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=approved_cibil, name="Approved", nbinsx=30, 
                                         marker_color="rgba(16,185,129,0.7)", marker_line_width=0))
        fig_hist.add_trace(go.Histogram(x=rejected_cibil, name="Rejected", nbinsx=30,
                                         marker_color="rgba(239,68,68,0.7)", marker_line_width=0))
        fig_hist.update_layout(
            title=dict(text="CIBIL Score Distribution", font=dict(color="rgba(255,255,255,0.7)", size=14)),
            barmode="overlay",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(color="rgba(255,255,255,0.4)", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(color="rgba(255,255,255,0.4)", gridcolor="rgba(255,255,255,0.05)"),
            height=300, margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        # Income vs Loan Amount scatter
        
        sample = df_raw.sample(min(500, len(df_raw)), random_state=42)

        fig_scatter = px.scatter(
    sample,
    x="income_annum",
    y="loan_amount",
    color="loan_status",
    color_discrete_map={
        "Approved": "#10B981",
        "Rejected": "#EF4444"
    }
)
        fig_scatter.update_layout(
            title=dict(text="Income vs Loan Amount (₹M)", font=dict(color="rgba(255,255,255,0.7)", size=14)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(title="Income (₹M)", color="rgba(255,255,255,0.4)", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Loan (₹M)", color="rgba(255,255,255,0.4)", gridcolor="rgba(255,255,255,0.05)"),
            height=300, margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c4:
        # Education vs Loan Status grouped bar
        edu_status = (
    df_raw.groupby(["education", "loan_status"])
    .size()
    .reset_index(name="count")
)

        fig_bar = px.bar(
    edu_status,
    x="education",
    y="count",
    color="loan_status",
    barmode="group",
    color_discrete_map={
        "Approved": "#10B981",
        "Rejected": "#EF4444"
    }
)
        fig_bar.update_layout(
            title=dict(text="Education vs Loan Status", font=dict(color="rgba(255,255,255,0.7)", size=14)),
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(color="rgba(255,255,255,0.4)"),
            yaxis=dict(color="rgba(255,255,255,0.4)", gridcolor="rgba(255,255,255,0.05)"),
            height=300, margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Data preview
    st.markdown('<div class="section-label" style="margin-top:10px;">Raw Data Preview</div>', unsafe_allow_html=True)
    n_rows = st.slider("Rows to show", 5, 50, 10)
    styled_df = df_raw.head(n_rows).style.map(
    lambda v: "color: #10B981; font-weight:600" if v == "Approved"
    else "color: #EF4444; font-weight:600",
    subset=["loan_status"]
)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=280
)


# ══════════════════════════════════════════════
# TAB 3 — FEATURE IMPORTANCE
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">What Drives Loan Decisions?</div>', unsafe_allow_html=True)

    feature_names = ["Dependents", "Education", "Self-Employed", "Annual Income",
                     "Loan Amount", "Loan Term", "CIBIL Score",
                     "Residential Assets", "Commercial Assets", "Luxury Assets", "Bank Assets"]
    importances = model.feature_importances_
    idx_sorted = np.argsort(importances)[::-1]

    fig_fi = go.Figure(go.Bar(
        x=[feature_names[i] for i in idx_sorted],
        y=[importances[i] for i in idx_sorted],
        marker=dict(
            color=[importances[i] for i in idx_sorted],
            colorscale=[[0, "#1a2a4a"], [0.5, "#b08a00"], [1, "#FAC400"]],
            showscale=False,
            line=dict(width=0)
        ),
        text=[f"{importances[i]*100:.1f}%" for i in idx_sorted],
        textposition="outside",
        textfont=dict(color="rgba(255,255,255,0.7)", size=11)
    ))
    fig_fi.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="rgba(255,255,255,0.5)", tickangle=-30, gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(color="rgba(255,255,255,0.5)", gridcolor="rgba(255,255,255,0.06)", tickformat=".1%"),
        height=380, margin=dict(t=20, b=80, l=20, r=20)
    )
    st.plotly_chart(fig_fi, use_container_width=True)

    # Insight cards
    top3 = [feature_names[idx_sorted[i]] for i in range(3)]
    icons = ["🥇", "🥈", "🥉"]
    cols = st.columns(3)
    for i, (col, feat, icon) in enumerate(zip(cols, top3, icons)):
        with col:
            imp_val = importances[idx_sorted[i]] * 100
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div class="metric-label" style="text-align:center;margin-top:6px;">Rank {i+1}</div>
                <div style="color:white;font-weight:700;font-size:1rem;">{feat}</div>
                <div class="metric-value" style="font-size:1.5rem;">{imp_val:.1f}%</div>
                <div class="metric-sub" style="text-align:center;">importance weight</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CIBIL score impact bar
    st.markdown('<div class="section-label">CIBIL Score Impact on Approval</div>', unsafe_allow_html=True)
    buckets = [(300,500,"300–500"),(500,600,"500–600"),(600,700,"600–700"),(700,750,"700–750"),(750,900,"750–900")]
    bucket_data = []
    for lo, hi, label in buckets:
        mask = (df_raw["cibil_score"]>=lo) & (df_raw["cibil_score"]<hi)
        sub = df_raw[mask]
        if len(sub) > 0:
            rate = (sub["loan_status"]=="Approved").mean()*100
            bucket_data.append({"Band": label, "Approval Rate": rate, "Count": len(sub)})
    bd = pd.DataFrame(bucket_data)

    fig_cibil = go.Figure(go.Bar(
        x=bd["Band"], y=bd["Approval Rate"],
        marker=dict(color=bd["Approval Rate"], colorscale=[[0,"#EF4444"],[0.5,"#F59E0B"],[1,"#10B981"]], showscale=False),
        text=[f"{r:.0f}%" for r in bd["Approval Rate"]],
        textposition="outside",
        textfont=dict(color="rgba(255,255,255,0.7)", size=12)
    ))
    fig_cibil.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="rgba(255,255,255,0.5)", title="CIBIL Score Band"),
        yaxis=dict(color="rgba(255,255,255,0.5)", gridcolor="rgba(255,255,255,0.06)", title="Approval Rate (%)", range=[0,110]),
        height=300, margin=dict(t=20, b=40, l=20, r=20)
    )
    st.plotly_chart(fig_cibil, use_container_width=True)


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    💎 LoanIQ &nbsp;·&nbsp; AI Loan Intelligence Platform &nbsp;·&nbsp; 
    Crafted with ♥ by <span>Rahul Thakur</span> &nbsp;·&nbsp; 
    Powered by Random Forest + Streamlit
</div>
""", unsafe_allow_html=True)