#Persiapan impor perpustakaan
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set( style='dark')

#Persiapan kepala
st.set_page_config(page_title="Dashboard Kualitas Udara", layout="wide")
st.title('Dashboard Inspeksi Kualitas Udara')
st.write("Data Ini adalah hasil Inspeksi Kualitas udara Beijing.")

#Persiapan dataset
beijingdf = pd.read_csv('beijingdf.csv')

#deklarasi waktu
date = ["datetime"]
beijingdf.sort_values(by="datetime", inplace=True)
beijingdf.reset_index(inplace = True)

#iterasi kolom
for col in date : #iterasi tanggal
    beijingdf[col] = pd.to_datetime(beijingdf[col])

#Penentuan tanggal minimal dan maksimal
min_date = beijingdf["datetime"].min()
max_date = beijingdf["datetime"].max()

#Penambahan logo
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://seeklogo.com/images/S/streamlit-logo-1A3B208AE4-seeklogo.com.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Filter Tanggal',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )