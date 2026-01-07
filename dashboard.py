import streamlit as st
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px




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

    r = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    
    return r
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

# --- KPI Utama ---
st.header('KPI Utama')

# deteksi nama kolom yang umum
def find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

sales_col = find_col(data, ['Sales', 'sales'])
profit_col = find_col(data, ['Profit', 'profit'])
order_col = find_col(data, ['Order ID', 'OrderID', 'Order Id', 'Order_Id', 'Order Id '])
quantity_col = find_col(data, ['Quantity', 'quantity', 'Qty'])

total_sales = data[sales_col].sum() if sales_col in data.columns else None
total_profit = data[profit_col].sum() if profit_col in data.columns else None
total_orders = data[order_col].nunique() if order_col in data.columns else data.shape[0]
total_quantity = data[quantity_col].sum() if quantity_col in data.columns else None
profit_margin = None
if total_sales and total_sales != 0 and total_profit is not None:
    profit_margin = (total_profit / total_sales) * 100

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if total_sales is None:
        st.metric('Total Sales', 'N/A')
    else:
        st.metric('Total Sales', f"{total_sales:,.2f}")
with c2:
    if total_profit is None:
        st.metric('Total Profit', 'N/A')
    else:
        st.metric('Total Profit', f"{total_profit:,.2f}")
with c3:
    st.metric('Total Orders', f"{int(total_orders):,}")
with c4:
    if total_quantity is None:
        st.metric('Total Quantity', 'N/A')
    else:
        st.metric('Total Quantity', f"{int(total_quantity):,}")
with c5:
    if profit_margin is None:
        st.metric('Profit Margin', 'N/A')
    else:
        st.metric('Profit Margin', f"{profit_margin:.2f}%")

st.write(data)
def groupby(x, y):
    d = data.groupby(x)[y].sum().reset_index()
    return d


# --- Analisis Waktu: Sales & Profit per Tahun (interaktif) ---
data ['Orderdate'] = pd.to_datetime(data ['Order Date'])
data ['Year'] = data ['Orderdate'].dt.year

yearly_data = (data.
               groupby("Year")
               .agg(
                   Sales =("Sales", "sum"),
                   Profit = ("Profit", "sum")
               ) 
               .reset_index()
            )

st.header('Analisis Waktu: Sales & Profit per Tahun')

cols = st.columns(2)
with cols[0]:
    with st.container(border=True, horizontal="Center") :
        st.title("Total Sales per Tahun")
        fig_sales = px.line(
            yearly_data, 
            x='Year', 
            y='Sales', 
            markers=True
        )
        
        fig_sales.update_xaxes(
        tickmode="linear",
        tick0=yearly_data["Year"].min(),
        dtick=1
        )
        st.plotly_chart(fig_sales)

with cols[1]:
    with st.container(border=True, horizontal="Center") :
        st.title("Total Profit per Tahun")
        fig_profit = px.line(
            yearly_data, 
            x='Year', 
            y='Profit', 
            markers=True
        )
        fig_profit.update_xaxes(
            tickmode="linear",
            tick0=yearly_data["Year"].min(),
            dtick=1
        )
        st.plotly_chart(fig_profit)


st.header('Analisis Customer & Segment')

cols = st.columns(2)

with cols[0]:
    with st.container(border=True, horizontal="Center") :
        st.title("Total Sales per Customer Segment")
        segment_sales = groupby("Segment", "Sales")
        fig_segment_sales = px.bar(
            segment_sales, 
            x='Segment', 
            y='Sales',
           color="Sales",
           color_continuous_scale=[
                            "#eef2f7",
                            "#86a3be",
                            "#5281b8",
                            "#1E3D5E"
                            ],
            text_auto=".2s"
        )
        fig_segment_sales.update_layout(coloraxis_showscale=False)
              
        st.plotly_chart(fig_segment_sales)

with cols[1]:
    with st.container(border=True):
        st.title("Total Profit per Customer Segment")

        segment_profit = (
            data.groupby("Segment")["Profit"]
            .sum()
            .reset_index()
            .sort_values("Profit", ascending=False) 
        )

        fig_segment_profit = px.pie(
            segment_profit,
            names="Segment",
            values="Profit",
            hole=0.4,
            color="Profit",
            color_discrete_sequence=[
                "#1E3D5E",  # paling gelap → profit terbesar
                "#5281b8",
                "#86a3be",
                "#eef2f7" 
            ]
        )

        fig_segment_profit.update_traces(
            textinfo="percent+label",
            textfont_size=14
        )

        fig_segment_profit.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=80, b=80, l=40, r=40)
        )

        st.plotly_chart(fig_segment_profit, use_container_width=True)


st.set_page_config(layout="wide")
with st.container(border=True,) :
        st.title("Top 10 Customer by Sales")
        fig_top_customer = (
                    data.groupby("Customer Name")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False).head(10))
        fig_top_customer = px.bar(
                                fig_top_customer,
                                x="Sales",
                                y="Customer Name",
                                color="Sales",
                                color_continuous_scale=[
                                    "#eef2f7",
                                    "#86a3be",
                                    "#5281b8",
                                    "#1E3D5E"
                                ],
                                text_auto=".2s"
                            )

        fig_top_customer.update_layout(
            yaxis=dict(autorange="reversed"),  
            xaxis_title="Total Sales",
            yaxis_title="Customer Name",
            margin=dict(t=60, b=40, l=120, r=40),
            height=500,
            coloraxis_showscale=False
            )
        fig_top_customer.update_yaxes(automargin=True)
        st.plotly_chart(fig_top_customer, use_container_width=True)


