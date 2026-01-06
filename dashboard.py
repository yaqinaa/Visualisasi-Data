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

# Buat bar chart
st.title("Total Sales by Region")

# Hitung total Sales per State
total_by_region = groupby(data, 'Region', 'Sales').sort_values(by='Sales', ascending=False)

# Plot dengan Plotly
fig_bar = px.bar(
    data_frame=total_by_region,
    x='Region',
    y='Sales',
    height=500,
    
)

fig_bar.update_layout(
    title=dict(
        text='<b></b>',
        y=0.9,
        x=0.5
    )
)

st.plotly_chart(fig_bar)
#membuat 2 kolom untuk dahsboard
# continuer = st.container(border=True, horizontal="Center")
cols = st.columns(2)  
with cols[0]:
    st.text("Kolom 1")
    


with cols[1]:
    st.text("Kolom 2")