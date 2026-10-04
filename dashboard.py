import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="AquaFlow — Garbusa WRSMS",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💧 AquaFlow — Garbusa Water Refilling Station")
st.subheader("Management System Dashboard")

# Load built React app
react_index = Path(__file__).parent / "frontend" / "dist" / "index.html"

if react_index.exists():
    html_content = react_index.read_text(encoding="utf-8")
    components.html(
        html_content,
        height=900,
        scrolling=True
    )
else:
    st.error("⚠️ React build not found. Run `npm run build` inside `frontend/` first.")
    st.code("cd frontend && npm run build")

st.divider()
st.caption("Garbusa → AquaFlow • WRSMS v3.2 • Cagayan de Oro, PH")
