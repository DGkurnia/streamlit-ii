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
#persiapan grafik partikulat
st.header('Air Quality in Aotizhongxin :sparkles:')
#Data utama
main_df = beijingdf[(beijingdf["datetime"] >= str(start_date)) & 
                (beijingdf["datetime"] <= str(end_date))]
#Deklarasi sub kepala
st.subheader("Inspeksi Partikulat")
tahunan = main_df.groupby("datetime").mean(numeric_only=True)

#pemilihan stasiun
pilihan = st.selectbox("Pilihan stasiun", tahunan['station'].unique())
# Filtrasi data
filtrat = tahunan[tahunan['station'] == pilihan]

# Deklarasi tangga
filtrat.set_index('datetime', inplace=True)

#Grafik partikulat untuk Inspeksi partikulat (nilai PM2.5 & nilai PM10)
[anPMa, dlPMa, anPMb, dlPMb] = [40, 150, 35, 75] 
#Batas aman
safety_limits = {'PM2.5 anual': anPMa,  'PM2.5 maksimal': dlPMa, # Batas anual dan Maksimal PM 2.5   
                 'PM10 anual': anPMb, 'PM10 maksimal': dlPMb} #Batas anual dan maksimal PM.10
#Keterangan (1. a adalah inepeksi PM2.5 b adalah PM10 2. kode an adalah anual kode ma adalah nilai maksimal)
fig = px.line(hasil, x='datetime', y=['PM2.5', 'PM10'],
              labels={['PM2.5','PM10']: 'Kadar Partikulat', 'datetime': 'Tanggal'},
              title='Inspeksi Partikulat')
#Inspeksi Batas Aman
for pollutant, limit in safety_limits.items():
    fig.add_hline(y=limit, line_color="red", line_dash="dash",
                   annotation_text=f"{pollutant} Batas aman: {limit} µg/m³", 
                   annotation_position="top right")
#Ilustrasi normal untuk partikulat
st.plotly_chart(fig)
#Pemeriksaan batas partikulat
batasanu = hasil[(hasil['PM2.5'] > safety_limits['PM2.5 anual'] & hasil['PM2.5'] < safety_limits['PM2.5 maksimal']) 
                 | (hasil['PM10'] > safety_limits['PM10 anual'] & hasil['PM10'] < safety_limits['10 maksimal'])] #Batas anual
lwt = hasil[(hasil['PM2.5'] > safety_limits['PM2.5 maksimal']) | (hasil['PM10'] > safety_limits['PM10 maksimal'])] #Batas maksimal
#Area batas anual
if not lwt.empty:
    st.warning("Peringatan : Ini sudah terlalu bahaya")
elif not batasanu.empty and lwt.empty:
    st.warning("Peringatan : Ini harus hati-hati") #Kasus melewati batas anual (tapi di dibawah nilai maksimal)
else:
    st.success("Kadar udara masih aman")
 #------------------------------------------