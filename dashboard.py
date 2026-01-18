import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from BarChart_Sales_SubCategory import Bar1
from BarChart_Sales_State import Bar2
from Line_chart_sales import Bar3
from line_chart_profit import Bar4
from BarChartsales_segment import Bar5
from PieChart_profit_segment import Bar6
from BarChart_top_customer import Bar7
from map import MapSalesState
from Bubble_Chart import BubbleSalesProfit
from Bar_Chart_Lowest_Profit import BarLowestProfitCity

# --- CONFIG & STYLING ---
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    layout="wide"
)

st.markdown("""
    <style>
    /* Reset Spasi Atas agar tidak ada sekat putih */
    .main .block-container {
        padding-top: 0rem !important;
        background-color: #F8F9FA;
    }
    
    /* JUDUL UTAMA */
    .main-title {
        background-color: #1B2631; 
        color: #FFD700; 
        padding: 40px;
        border-radius: 0 0 20px 20px;
        font-size: 50px !important; 
        font-weight: 900 !important; 
        text-align: center;
        margin-bottom: 40px;
        letter-spacing: 3px;
        text-transform: uppercase;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }

    /* Kartu KPI Kuning */
    [data-testid="stMetric"] {
        background-color: #FFD700; 
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #E6C200;
        text-align: center;
    }

    /* JUDUL PER CARD KPI (Label) - DIPERBAIKI AGAR BOLD & HIGHLIGHT */
    [data-testid="stMetricLabel"] div p {
        color: #1B2631 !important;
        font-size: 20px !important; 
        font-weight: 900 !important; 
        text-transform: uppercase !important; 
        letter-spacing: 1.5px !important;
    }

    /* ANGKA KPI (Value) */
    [data-testid="stMetricValue"] div {
        color: #1B2631 !important;
        font-size: 38px !important;
        font-weight: 900 !important;
    }

    /* Judul Section Highlight */
    .section-title {
        background-color: #FFD700;
        color: #1B2631;
        padding: 15px 25px;
        border-radius: 10px 10px 0 0;
        font-size: 24px !important;
        font-weight: 900 !important;
        margin-top: 40px;
        border-left: 15px solid #1B2631;
        display: inline-block;
        width: 100%;
    }

    /* Container Box Grafik */
    div[data-testid="stContainer"] {
        background-color: #FFFFFF;
        border-radius: 0 0 15px 15px;
        border: 1px solid #DEE2E6;
        padding: 30px;
        margin-bottom: 45px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

def responsive_plotly(fig):
    fig.update_layout(
        template="plotly_white",
        autosize=True,
        margin=dict(l=20, r=20, t=80, b=20), 
        hovermode="x unified",
        font=dict(family="Arial Black", color="#1B2631")
    )
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def load_data(data_path: str):
    r = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    return r

# --- DATA PREPROCESSING ---
data = load_data("Sample - Superstore.csv")
data["Order Date"] = pd.to_datetime(data["Order Date"])
data["Year"] = data["Order Date"].dt.year
data["State"] = data["State"].str.strip()

# --- FILTER ---
st.sidebar.header("Control Panel")
year_opt = st.sidebar.selectbox("Tahun", ["All"] + sorted(data["Year"].unique().tolist()))
state_opt = st.sidebar.multiselect("State", sorted(data["State"].unique().tolist()), default=sorted(data["State"].unique().tolist()))
cat_opt = st.sidebar.multiselect("Category", sorted(data["Category"].unique().tolist()), default=sorted(data["Category"].unique().tolist()))

filtered_data = data.copy()
if year_opt != "All": filtered_data = filtered_data[filtered_data["Year"] == year_opt]
if state_opt: filtered_data = filtered_data[filtered_data["State"].isin(state_opt)]
if cat_opt: filtered_data = filtered_data[filtered_data["Category"].isin(cat_opt)]

# --- INIT SEMUA 10 CHART ---
chart1 = Bar1(filtered_data)
chart2 = Bar2(filtered_data)
chart3 = Bar3(filtered_data)
chart4 = Bar4(filtered_data)
chart5 = Bar5(filtered_data)
chart6 = Bar6(filtered_data)
chart7 = Bar7(filtered_data)
chart_map = MapSalesState(filtered_data)
chart_bubble = BubbleSalesProfit(filtered_data)
chart_low = BarLowestProfitCity(filtered_data)

# --- RENDER ---
st.markdown('<p class="main-title">SUPERSTORE SALES DASHBOARD</p>', unsafe_allow_html=True)

# KPI Section
total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
total_orders = filtered_data['Order ID'].nunique()
total_qty = filtered_data['Quantity'].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.metric('Total Sales', f"${total_sales:,.0f}")
with c2: st.metric('Total Profit', f"${total_profit:,.0f}")
with c3: st.metric('Total Orders', f"{int(total_orders):,}")
with c4: st.metric('Total Quantity', f"{int(total_qty):,}")
with c5: st.metric('Profit Margin', f"{profit_margin:.2f}%")

# 1. Spatial & Detail
st.markdown('<p class="section-title">Spatial & Transactional Analysis</p>', unsafe_allow_html=True)
col_geo, col_dtl = st.columns([1.6, 1])
with col_geo:
    with st.container(border=True): responsive_plotly(chart_map.plot(year=year_opt))
with col_dtl:
    with st.container(border=True): 
        st.write(f"**Transaction Data Details ({year_opt})**")
        st.dataframe(filtered_data[['Order ID', 'Customer Name', 'Sales', 'Profit']].head(15), use_container_width=True, height=450)

# 2. Trends
st.markdown('<p class="section-title">Performance Growth Trends</p>', unsafe_allow_html=True)
col_t1, col_t2 = st.columns(2)
with col_t1:
    with st.container(border=True): responsive_plotly(chart3.plot(year=year_opt))
with col_t2:
    with st.container(border=True): responsive_plotly(chart4.plot(year=year_opt))

# 3. Segments
st.markdown('<p class="section-title">Customer Segment Insights</p>', unsafe_allow_html=True)
col_s1, col_s2 = st.columns(2)
with col_s1:
    with st.container(border=True): responsive_plotly(chart5.plot(year=year_opt))
with col_s2:
    with st.container(border=True): responsive_plotly(chart6.plot(year=year_opt))

# 4. Rankings
st.markdown('<p class="section-title">Top Performance Rankings</p>', unsafe_allow_html=True)
col_r1, col_r2, col_r3 = st.columns(3)
with col_r1:
    with st.container(border=True): responsive_plotly(chart1.plot(year=year_opt))
with col_r2:
    with st.container(border=True): responsive_plotly(chart2.plot(year=year_opt))
with col_r3:
    with st.container(border=True): responsive_plotly(chart7.plot(year=year_opt))

# 5. Risk
st.markdown('<p class="section-title">Risk & Operational Correlation</p>', unsafe_allow_html=True)
col_risk1, col_risk2 = st.columns(2)
with col_risk1:
    with st.container(border=True): responsive_plotly(chart_bubble.plot(year=year_opt))
with col_risk2:
    with st.container(border=True): responsive_plotly(chart_low.plot(year=year_opt))