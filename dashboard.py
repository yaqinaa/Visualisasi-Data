import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



@st.cache_data
def load_data(data : str):
    r = pd.read_csv("Sample - Superstore.csv",
                        encoding="latin1")
    
    return r

data = load_data("Sample - Superstore.csv")

st.write(data)