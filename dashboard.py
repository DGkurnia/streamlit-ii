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
   
filtrat = hasil.copy() #salinan untuk keamanan

#Laporan terkini
terkini = {
     'kota' : pilihan,
     'Kadar partikulat' : np.round([(filtrat['PM2.5'].iloc[-1]),(filtrat['PM10'].iloc[-1])],3),
     'Senyawa CO': np.round(filtrat['CO'].iloc[-1],3),
     'Kadar ozon' : np.round(filtrat['O3'].iloc[-1],3),
     'Kadar sulfur di udara': np.round(filtrat['SO2'].iloc[-1],3),
     'Kadar nitrogen di udara': np.round(filtrat['NO2'].iloc[-1],3),
     'suhu (celsius)' : np.round(filtrat['TEMP'].iloc[-1],3),
     'Suhu dan kelembapan': np.round(filtrat[['TEMP','DEWP']].iloc[-1],3),
     'kecepatan angin': np.round(filtrat['WSPM'].iloc[-1],3)
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

# tambahan (Persiapan sub data) demi kemudahan
gruppar = filtrat[['datetime', 'PM2.5', 'PM10']].copy() #inspeksi partikulat
gruppar['datetime'] = pd.to_datetime(gruppar['datetime']) #diurutkan dari waktu
#Senyawa CO
cogrp = filtrat[['datetime','CO']].copy() #inspeksi senyawa CO
cogrp['datetime'] = pd.to_datetime(cogrp['datetime'])
#senyawa ozon
ozgrp = filtrat[['datetime','O3']].copy() #inspeksi senyawa ozon
ozgrp['datetime'] = pd.to_datetime(ozgrp['datetime'])
#Nitrogen
nigrp = filtrat[['datetime','NO2']].copy() #inspeksi senyawa nitrogen
nigrp['datetime'] = pd.to_datetime(nigrp['datetime'])
#sulfur
sulgrp = filtrat[['datetime','SO2']].copy() #inspeksi senyawa sulfur
sulgrp['datetime'] = pd.to_datetime(sulgrp['datetime'])

#tambahan 2: rata-rata mingguan
weekly = filtrat.resample('W-MON', on='datetime')[['PM2.5', 'PM10', 'CO', 'O3', 'NO2', 'SO2']].mean().copy() #data mingguan
#persiapan data mingguan
wekpar = weekly[['datetime', 'PM2.5', 'PM10']].copy() #inspeksi partikulat mingguan
wekpar['datetime'] = pd.to_datetime(wekpar['datetime']) #diurutkan dari waktu

#Inspeksi Senyawa
wekcompound = weekly.resample('W-MON', on='datetime')[['CO', 'O3', 'NO2', 'SO2']].mean().copy()#salinan untuk senyawa lain


#-------------------- (laporan mingguan: bagian data aman)
# Inspeksi keamanan partikulat (nilai PM2.5 & nilai PM10)
[anPMa, dlPMa, anPMb, dlPMb] = [40, 150, 35, 75] 

#Batas aman partikulat
safety_limits = {'PM2.5 anual': anPMa,  'PM2.5 maksimal': dlPMa, # Batas anual dan Maksimal PM 2.5   
                 'PM10 anual': anPMb, 'PM10 maksimal': dlPMb} #Batas anual dan maksimal PM.10

#Keterangan (1. a adalah inepeksi PM2.5 b adalah PM10 2. kode an adalah anual kode ma adalah nilai maksimal)

#Inspeksi batas senyawa karbon monoksida dan tiga senyawa lainnya
[cochl, cogl, ozmin, ozmax, nmax, smax ] = [4000, 30000, 50, 160, 200, 500]
#Deklarasi batas senyawa
colim = { 'China' : cochl, 'Global' : cogl} #Batas senyawa CO
ozlim = { 'minimum' : ozmin,'maksimum' : ozmax } #Inspeksi Ozon/ ozon (O3)
nitlim = {'anual': 40, 'maksimal' : nmax} #Batas  nitrogen dioksida (NO2)
sulplim = {'anual': 40, 'maksimal': smax} #Batas Sulfur dioksida (SO2)

#Penulisan ulang untuk batas senyawa di analisis mingguan
complimit = {
    'CO': {'China': colim['China'], 'Global': colim['Global']},
    'O3': {'min': ozlim['minimum'], 'maksimum': ozlim['maksimum']},
    'NO2': {'anual': nitlim['anual'], 'maksimum': nitlim['maksimal']},
    'SO2': {'anual': sulplim['anual'], 'maksimum': sulplim['maksimal']}
}

#--------------------Grafik mingguan
# Inspeksi grafik mingguan
for pollutant in ['PM2.5', 'PM10']:
    fig = px.bar(wekpar[pollutant],
                 title=f"Weekly Average {pollutant.capitalize()} Levels",
                 labels={'value': f'{pollutant.capitalize()} levels'})

    # Bagian batas aman
    fig.add_hline(y=safety_limits[f"{pollutant} anual"], line_color='orange', 
                  annotation_text="Annual Limit", annotation_position="top left")
    
    if pollutant == 'PM10':
        fig.add_hline(y=safety_limits[f"{pollutant} maksimal"], line_color='red',
                      annotation_text="Maximal Limit", annotation_position="top left")

# Inspeksi Senyawa
for pollutant in ['CO', 'O3', 'NO2', 'SO2']:
    fig = px.bar(complimit[[pollutant]],
                 title=f"Weekly Average {pollutant.capitalize()} Levels",
                 labels={f'value_{pollutant}': f'{pollutant.capitalize()} levels'})
    
    # Add safety limits as horizontal lines for CO, O3, NO2, SO2 if applicable
    if pollutant == 'CO':
        fig.add_hline(y=complimit[pollutant]['China'], line_color='red', line_dash='dash',
                      annotation_text="Batas aman di China", annotation_position="top right")
        fig.add_hline(y=safety_limits[pollutant]['Global'], line_color='orange', line_dash='dash',
                      annotation_text="Global Limit", annotation_position="top right")
    
    elif pollutant == 'O3':
        fig.add_hline(y=complimit[pollutant]['min'], line_color='red', line_dash='dash',
                      annotation_text="Batas anual", annotation_position="top right")
        fig.add_hline(y=complimit[pollutant]['maksimum'], line_color='orange', line_dash='dash',
                      annotation_text="Batas maksimal", annotation_position="top right")
    
    elif pollutant in ['NO2', 'SO2']:
        fig.add_hline(y=complimit[pollutant]['maksimum'], line_color='red', line_dash='dash',
                      annotation_text="Batas maksimal", annotation_position="top right")
        fig.add_hline(y=complimit[pollutant]['anual'], line_color='orange', line_dash='dash',
                      annotation_text="Batas Anual", annotation_position="top right")

    st.plotly_chart(fig)

#---------------------(Grafik total)
# Judul grafik total
st.header("Inspeksi partikulat dalam suatu waktu")
# komponen grafik
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
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#------------------------------------------
#A3. Grafik Inspeksi senyawa CO


#--------------------------------------------




