#Persiapan impor perpustakaan
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set( style='dark')

#Persiapan kepala
st.set_page_config(page_title="Dashboard Kualitas Udara", layout="wide")
st.title('Dashboard Inspeksi Kualitas Udara')
st.write("Data Ini adalah hasil Inspeksi Kualitas udara Beijing.")

## Persiapan dataset
beijingdf = pd.read_csv('beijingdf.csv') #Data
beijingdf.sort_values(by="datetime", inplace=True)
beijingdf.reset_index(inplace=True)

# Konversi kolom tanggal menjadi tanggal
beijingdf['datetime'] = pd.to_datetime(beijingdf['datetime'])

# Penentuan tanggal minimal dan maksimal
min_date = beijingdf["datetime"].min().strftime('%Y-%m-%d')  # Tanggal
max_date = beijingdf["datetime"].max().strftime('%Y-%m-%d')  

# Data utama dalam rentang waktu tertentu (optional)
main_df_filtered_dates = beijingdf[(beijingdf["datetime"]>=min_date)&(beijingdf["datetime"]<=max_date)]
   
unik = main_df_filtered_dates['station'].unique() #penenda
   
pilihan = st.selectbox("Select Station:", unik)
   
hasil = main_df_filtered_dates.groupby(['datetime','station']).filter(lambda x:x.station == pilihan)
   
filtrat = hasil.copy()

#Laporan terkini
terkini = {
     'kota' : pilihan,
     'Kadar partikulat' : [(filtrat['PM2.5'].iloc[-1]),(filtrat['PM10'].iloc[-1])],
     'Senyawa CO': filtrat['CO'].iloc[-1],
     'Kadar ozon' : filtrat['O3'].iloc[-1],
     'Kadar sulfur di udara': filtrat['SO2'].iloc[-1],
     'Kadar nitrogen di udara': filtrat['NO2'].iloc[-1],
     'suhu (celsius)' : filtrat['TEMP'].iloc[-1],
     'Suhu dan kelembapan': filtrat[['TEMP','DEWP']].iloc[-1],
     'kecepatan angin': filtrat['WSPM'].iloc[-1] 
}

# Penampilan grafik hasil jika ada record yang cocok dengan pemilihan user    
if len(filtrat)>0 :
     st.write(terkini)
else:
      print("Tidak ditemukan rekaman untuk stasiun tersebut")
    
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
#persiapan judul
st.header('Inspeksi Kualitas Udara in Beijing :sparkles:')

#-------------------- 

# #(Persiapan sub data)
gruppar = filtrat[['datetime', 'PM2.5', 'PM10']] #inspeksi partikulat
cogrp = filtrat[['datetime','CO']] #inspeksi senyawa CO
ozgrpm = filtrat[['datetime','O3']] #inspeksi senyawa ozon
nigrp = filtrat[['datetime','NO2']] #inspeksi senyawa nitrogen
sulgrp = filtrat[['datetime','SO2']] #inspeksi senyawa sulfur

#--------------------
# A.1 Grafik partikulat untuk Inspeksi keamanan partikulat (nilai PM2.5 & nilai PM10)
[anPMa, dlPMa, anPMb, dlPMb] = [40, 150, 35, 75] 

#Batas aman partikulat
safety_limits = {'PM2.5 anual': anPMa,  'PM2.5 maksimal': dlPMa, # Batas anual dan Maksimal PM 2.5   
                 'PM10 anual': anPMb, 'PM10 maksimal': dlPMb} #Batas anual dan maksimal PM.10
#Keterangan (1. a adalah inepeksi PM2.5 b adalah PM10 2. kode an adalah anual kode ma adalah nilai maksimal)
# Judul grafik
st.header("Inspeksi partikulat dalam suatu waktu")

# Koversi grup ke data waktu [partikulat]
gruppar['datetime'] = pd.to_datetime(gruppar['datetime'])
#grafik
plt.figure(figsize=(12, 6))

# Scatter plot for PM2.5
plt.scatter(gruppar['datetime'], gruppar['PM2.5'], color='blue', label='PM2.5', alpha=0.6)

# Grafik sebaran
plt.scatter(gruppar['datetime'], gruppar['PM10'], color='orange', label='PM10', alpha=0.6)

# Batas anual
plt.axhline(y=safety_limits['PM2.5 annual'], color='lightblue', linestyle=':', label='Annual Safe PM2.5 (40 µg/m³)')
plt.axhline(y=safety_limits['PM10 annual'], color='lightyellow', linestyle=':', label='Annual Safe PM10 (35 µg/m³)')

# Batas Maksimal
plt.axhline(y=safety_limits['PM2.5 maximum'], color='blue', linestyle='--', label='Max Safe PM2.5 (150 µg/m³)')
plt.axhline(y=safety_limits['PM10 maximum'], color='orange', linestyle='--', label='Max Safe PM10 (75 µg/m³)')

#rincian grafik partikulat
plt.title('Inspeksi Partikulat sepanjang waktu')
plt.xlabel('Date and Time')
plt.ylabel('Particulate Levels (µg/m³)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#------------------------------------------
#Inspeksi batas senyawa karbon monoksida dan tiga senyawa lainnya
[cochl, cogl, ozmin, ozmax, nmax, smax ] = [4000, 30000, 50, 160, 200, 500]
#Deklarasi batas senyawa
colim = { 'China' : cochl, 'Global' : cogl} #Batas senyawa CO
ozlim = { 'minimum' : ozmin,'maksimum' : ozmax } #Inspeksi Ozon/ ozon (O3)
nitlim = {'anual': 40, 'maksimal' : nmax} #Batas  nitrogen dioksida (NO2)
sulplim = {'anual': 40, 'maksimal': smax} #Batas Sulfur dioksida (SO2)
#--------------------------------------------
#A3. Grafik Inspeksi senyawa CO



