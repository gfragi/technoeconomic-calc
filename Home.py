# app.py
import streamlit as st
st.set_page_config(page_title="TEA Tool", layout="wide")

st.title("📊 Welcome to the Techno-Economic Analysis (TEA) Tool")
st.markdown("""
This tool allows you to simulate and compare different **business scenarios** using both **subscription-based** and **pay-per-use** models.

---

### 🧭 Navigation Guide
Use the sidebar to:
- ▶️ **Create or Edit Scenarios**: Define input parameters such as fees, CAPEX, OPEX, growth rates.
- 📈 **Compare Scenarios**: View financial projections (NPV, ROI, Break-even) and visual comparisons.

---

### 📦 Applicability
This tool is ideal for:
- Data Space Operators
- SaaS Businesses
- Platform Services
- Cloud-based Solutions

It helps explore trade-offs between growth, investment, and pricing strategy.

---

### 📚 Additional Resources
Need help? Visit the **Instructions** page in the sidebar for a step-by-step guide.
""")
