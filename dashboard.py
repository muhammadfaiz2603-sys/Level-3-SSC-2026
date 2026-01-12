import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & DATA LOADING
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Level 3 Dashboard", layout="wide")

# CSS to style the metric cards
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #d6d6d6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA (Embedded from Level 3.xlsx) ---

# 1. Regional Performance Comparison
df_regional = pd.DataFrame({
    'Region': ['Central', 'Northern', 'Southern', 'East Coast', 'Sabah', 'Sarawak'],
    'Pass': [23, 16, 25, 31, 17, 10],
    'Fail': [32, 18, 15, 15, 20, 20],
    'Total Headcount': [55, 34, 40, 46, 37, 30]
})

# 2. Outlet Performance Comparison
df_outlet = pd.DataFrame({
    'Outlet': ['MT', 'PY', 'EV', 'MF'],
    'Pass': [4, 2, 1, 0],
    'Fail': [0, 3, 2, 1]
})

# -----------------------------------------------------------------------------
# COLUMN 1: SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("SSC 2026 Dashboard : Master")
    st.write("Select the dataset to view:")
    
    # Radio button to switch views
    view_selection = st.selectbox(
        "Dataset:",
        ["Regional Performance", "Outlet Performance"]
    )
    
    st.markdown("---")
    st.caption("© 2026 SSC 2026 | Insight Team")

# -----------------------------------------------------------------------------
# COLUMN 2: MAIN AREA
# -----------------------------------------------------------------------------

st.title(f"📊 {view_selection}")

# -- Logic to prepare data based on selection --
if view_selection == "Regional Performance":
    # Prepare Data
    active_df = df_regional
    
    # KPIs
    total_pass = active_df['Pass'].sum()
    total_fail = active_df['Fail'].sum()
    total_vol = active_df['Total Headcount'].sum()
    
    # Chart Data Preparation
    chart_df = active_df.melt(id_vars=['Region'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
    fig = px.bar(chart_df, x='Region', y='Count', color='Status', barmode='group',
                 color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'}, 
                 title="Pass vs Fail by Region", text_auto=True)

elif view_selection == "Outlet Performance":
    # Prepare Data
    active_df = df_outlet
    
    # KPIs
    total_pass = active_df['Pass'].sum()
    total_fail = active_df['Fail'].sum()
    total_vol = total_pass + total_fail
    
    # Chart Data Preparation
    chart_df = active_df.melt(id_vars=['Outlet'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
    fig = px.bar(chart_df, x='Outlet', y='Count', color='Status', barmode='group',
                 color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'}, 
                 title="Pass vs Fail by Outlet", text_auto=True)

# Calculate Pass Rate for all views
pass_rate = (total_pass / total_vol) * 100 if total_vol > 0 else 0


# --- ROW 1: DATA CARDS (KPIs) ---
st.subheader("1. Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Volume", f"{total_vol}")
kpi2.metric("Total Pass", f"{total_pass}")
kpi3.metric("Total Fail", f"{total_fail}")
kpi4.metric("Pass Rate", f"{pass_rate:.1f}%")

st.markdown("---")

# --- ROW 2: GRAPHS ---
st.subheader("2. Graphical Analysis")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- ROW 3: DATA TABLE ---
st.subheader("3. Raw Data Table")
st.dataframe(active_df, use_container_width=True)
