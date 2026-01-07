import streamlit as st
import pandas as pd




from BarChart_Sales_SubCategory import Bar1
from BarChart_Sales_State import Bar2

def responsive_plotly(fig, min_w=420, max_w=650):
    fig.update_layout(
        autosize=True,
        bargap=0.3,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    # CSS trick supaya responsive tapi ada batas
    st.markdown(
        f"""
        <style>
        div[data-testid="stPlotlyChart"] > div {{
            max-width: {max_w}px;
            min-width: {min_w}px;
            margin: auto;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.plotly_chart(fig)


@st.cache_data
def load_data(data : str):
    return pd.read_csv("Sample - Superstore.csv",
                        encoding="latin1")

data = load_data("Sample - Superstore.csv")

st.write(data)

st.divider()

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

#membuat 2 kolom untuk dahsboard
# continuer = st.container(border=True, horizontal="Center")
cols = st.columns([1, 1])
with cols[0]:
    st.text("Kolom 1")
    with st.container(border=True, horizontal="Center") :
        st.title("Top 10 Category by Sales")
        chart1 = Bar1(data)
        responsive_plotly(chart1.plot())




with cols[1]:
    st.text("Kolom 2")
    with st.container(border=True, horizontal="Center") :
        # Buat bar chart
        st.title("Top 10 State by Sales")
        chart2 = Bar2(data)
        responsive_plotly(chart2.plot())
