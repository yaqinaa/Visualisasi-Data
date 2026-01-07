import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px



@st.cache_data
def load_data(data : str):
    r = pd.read_csv("Sample - Superstore.csv",
                        encoding="latin1")
    
    return r

data = load_data("Sample - Superstore.csv")

st.write(data)

# Fungsi untuk groupby
def groupby(df, x, y):
    d = df.groupby(x)[y].sum().reset_index()
    return d

st.divider()

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)


def responsive_plotly(fig, min_w=420, max_w=650):
    fig.update_layout(
        autosize=True,
        bargap=0.3,
        margin=dict(l=80, r=20, t=30, b=20)
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

#membuat 2 kolom untuk dahsboard
# continuer = st.container(border=True, horizontal="Center")
cols = st.columns([1, 1])  
with cols[0]:
    st.text("Kolom 1")
    with st.container(border=True, horizontal="Center") :
        # Buat bar chart
        st.title("Top 10 Products by Sales")

        # Hitung total Sales per Category
        total_by_category = groupby(data, 'Sub-Category', 'Sales').sort_values(by='Sales', ascending=True).head(10)

        # Plot dengan Plotly
        fig_bar = px.bar(
            data_frame=total_by_category,
            x='Sales',
            y='Sub-Category',
            orientation='h',
            height=500,
            
        )

        fig_bar.update_layout(
            title=dict(
                text='<b></b>',
                y=0.9,
                x=0.5
            )
        )

        fig_bar.update_layout(
            margin=dict(l=20, r=20, t=30, b=20)
        )

        responsive_plotly(fig_bar)



with cols[1]:
    st.text("Kolom 2")
    with st.container(border=True, horizontal="Center") :
        # Buat bar chart
        st.title("Top 10 State by Sales")

        # Hitung total Sales per State
        total_by_state = groupby(data, 'State', 'Sales').sort_values(by='Sales', ascending=True).head(10)

        # Plot dengan Plotly
        fig_bar1 = px.bar(
            data_frame=total_by_state,
            x='Sales',
            y='State',
            orientation='h',
            height=500,
        )

        fig_bar1.update_layout(
            title=dict(
                text='<b></b>',
                y=0.9,
                x=0.5
            )
        )
        fig_bar1.update_layout(
            margin=dict(l=20, r=20, t=30, b=20)
        )

        responsive_plotly(fig_bar1)
