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
min_date = beijingdf["datetime"].min().date()  # Tanggal
max_date = beijingdf["datetime"].max().date()  

# Data utama dalam rentang waktu tertentu (optional)
#Data utama
main_df = beijingdf[(beijingdf["datetime"] >= str(min_date)) & 
                (beijingdf["datetime"] <= str(max_date))]

#Pemilihan stasiun
stasiun_unik = main_df['station'].unique()

#Deklarasi
tahunan = main_df.groupby("datetime")

#pilihan stasiun
pilihan = st.selectbox("Pilihan stasiun :", stasiun_unik)

# Filtrasi data
filtrat = main_df[main_df['station'] == pilihan]

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
#pemeriksaan tanggal
filtrat['datetime'] = pd.to_datetime(filtrat['datetime'])

#persiapan analisis data (data mingguan)
weekly = filtrat.resample('W-MON')[['PM2.5', 'PM10', 'CO', 'O3', 'NO2', 'SO2','TEMP','PRES','DEWP','WSPM']].mean().copy() 

#persiapan data mingguan
wekpar = weekly[['PM2.5', 'PM10']].mean().copy() #inspeksi partikulat mingguan

#Inspeksi Senyawa
wekcompound = weekly.resample('W-MON')[['CO', 'O3', 'NO2', 'SO2']].mean().copy()#salinan untuk senyawa lain

#Inspeksi aspek fisika
wekphs = weekly.resample('W-MON')[['TEMP', 'PRES', 'DEWP', 'WSPM']].mean().copy()

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
#inspeksi batas suhu, tekanan, dan kelembapan
#suhu
[nolim, diglim, nrmlim, pnslim] = [0, 10, 25, 35]
#tekanan
atm = 1013.25
#kelembapan
[drl, comdr, humin] = [10, 15, 20]
#penulisan ulang batas suhu
btsuhu = {'nol' : nolim,'dingin': diglim,'normal': nrmlim, 'panas': pnslim}
#penulisan batas kelembapan
btlembap = {'kering': drl, 'biasa': comdr, 'lembap': humin}

#--------------------Grafik mingguan
# Inspeksi grafik mingguan di partikulat
for pollutant in ['PM2.5', 'PM10']:
    # Create a DataFrame for the specific pollutant
    pollutant_data = wekpar[['datetime', pollutant]].copy()  # Jaga data asli
    fig = px.bar(pollutant_data,
                 x='datetime',  # Set x-axis to datetime
                 y=pollutant,
                 title=f"Weekly Average {pollutant.capitalize()} Levels",
                 labels={'value': f'{pollutant.capitalize()} levels'})

    # Bagian batas aman
    fig.add_hline(y=safety_limits[f"{pollutant} annual"], line_color='orange', 
                  annotation_text="Annual Limit", annotation_position="top left")
    
    if pollutant == 'PM10':
        fig.add_hline(y=safety_limits[f"{pollutant} maximal"], line_color='red',
                      annotation_text="Maximal Limit", annotation_position="top left")

    # Show the figure
    fig.show()
# Inspeksi Senyawa
# Inspeksi Senyawa
for pollutant in ['CO', 'O3', 'NO2', 'SO2']:
    # Create a DataFrame for the specific compound
    compound_data = wekcompound[['datetime', pollutant]].copy()  # Include datetime for x-axis

    fig = px.bar(compound_data,
                 x='datetime',  # Set x-axis to datetime
                 y=pollutant,
                 title=f"Weekly Average {pollutant.capitalize()} Levels",
                 labels={'value': f'{pollutant.capitalize()} levels'})

    # Batas Inspeksi
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

    # Display the figure using Streamlit
    st.plotly_chart(fig)

#Inspeksi Aspek fisika
for pollutant in ['TEMP', 'PRES', 'DEWP', 'WSPM']:
    fig = px.bar(wekphs[[pollutant]],
                 title=f"Weekly Average {pollutant.capitalize()} Levels",
                 labels={f'value_{pollutant}': f'{pollutant.capitalize()} levels'})
    
    # Batas Inspeksi
    if pollutant == 'TEMP':
        fig.add_hline(y=btsuhu[pollutant]['nol'], line_color='red', line_dash='dash',
                      annotation_text="Batas suhu beku", annotation_position="top right")
        fig.add_hline(y=btsuhu[pollutant]['dingin'], line_color='black', line_dash='dash',
                      annotation_text="Suhu dingin", annotation_position="top right")
        fig.add_hline(y=btsuhu[pollutant]['normal'], line_color='black', line_dash='dash',
                      annotation_text="Suhu Normal", annotation_position="top right")
        fig.add_hline(y=btsuhu[pollutant]['panas'], line_color='black', line_dash='dash',
                      annotation_text="Suhu Normal", annotation_position="top right")
        
    elif pollutant == 'PRES':
        fig.add_hline(y=atm, line_color='red', line_dash='dash',
                      annotation_text="Batas tekanan atmosfer", annotation_position="top right")
        
    elif pollutant in ['DEWP']:
        fig.add_hline(y=btlembap[pollutant]['kering'], line_color='red', line_dash='dash',
                      annotation_text="Batas kelembapan kering", annotation_position="top right")
        fig.add_hline(y=btlembap[pollutant]['biasa'], line_color='orange', line_dash='dash',
                      annotation_text="Batas kelembapan biasa", annotation_position="top right")
        fig.add_hline(y=btlembap[pollutant]['lembap'], line_color='orange', line_dash='dash',
                      annotation_text="Batas kelembapan tinggi", annotation_position="top right")

    st.plotly_chart(fig)

#---------------------(Grafik total)
# A2. Judul grafik Karbon Monoksida
st.header("Inspeksi senyawa karbon monoksida dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(12, 6))

# Inspeksi CO
plt.scatter(cogrp['datetime'], cogrp['CO'], color='pink', label='Nilai CO', alpha=0.6)


# Batas anual
plt.axhline(y=colim['China'], color='yellow', linestyle=':', label='Batas aman China')
plt.axhline(y=colim['Global'], color='red', linestyle=':', label='Batas aman global')


#rincian grafik CO
plt.title('Inspeksi Senyawa Karbon Monoksida sepanjang waktu')
plt.xlabel('Waktu (Tanggal dan waktu)')
plt.ylabel('Konsentrasi CO (µg/m³)')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#------------------------------------------A3. Grafik Inspeksi Partikulat
# Judul grafik partikulat total
st.header("Inspeksi partikulat dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(12, 6))

# Scatter plot for PM2.5
plt.scatter(gruppar['datetime'], gruppar['PM2.5'], color='blue', label='PM2.5', alpha=0.6)

# Grafik sebaran PM10
plt.scatter(gruppar['datetime'], gruppar['PM10'], color='orange', label='PM10', alpha=0.6)

# Batas anual
plt.axhline(y=safety_limits['PM2.5 anual'], color='lightblue', linestyle=':', label='Annual Safe PM2.5 (40 µg/m³)')
plt.axhline(y=safety_limits['PM10 anual'], color='lightyellow', linestyle=':', label='Annual Safe PM10 (35 µg/m³)')

# Batas Maksimal
plt.axhline(y=safety_limits['PM2.5 maksimal'], color='blue', linestyle='--', label='Max Safe PM2.5 (150 µg/m³)')
plt.axhline(y=safety_limits['PM10 maksimal'], color='orange', linestyle='--', label='Max Safe PM10 (75 µg/m³)')

#rincian grafik partikulat
plt.title('Inspeksi Partikulat sepanjang waktu')
plt.xlabel('Waktu (Tanggal dan waktu)')
plt.ylabel('Tingkatan Partikulat (µg/m³)')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#--------------------------------------------A4 Inspeksi senyawa ozon
st.header("Inspeksi senyawa ozon dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(12, 6))

# Inspeksi ozon
plt.scatter(ozgrp['datetime'], ozgrp['O3'], color='pink', label='Nilai CO', alpha=0.6)


# Batas ozon
plt.axhline(y=ozlim['minimum'], color='blue', linestyle=':', label='Batas konsentrasi ozon minimum')
plt.axhline(y=ozlim['maksimum'], color='green', linestyle=':', label='Batas konsentrasi ozon maksimum')


#rincian grafik ozon
plt.title('Inspeksi Senyawa ozon sepanjang waktu')
plt.xlabel('Waktu (Tanggal dan waktu)')
plt.ylabel('Konsentrasi ozon (µg/m³)')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#------------------------------------------A5. Grafik Inspeksi Senyawa Nitrogen Dioksida
st.header("Inspeksi senyawa Nitrogen dioksida dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(12, 6))

# Inspeksi ozon
plt.scatter(ozgrp['datetime'], ozgrp['O3'], color='pink', label='Nilai CO', alpha=0.6)


# Batas ozon
plt.axhline(y=nitlim['anual'], color='orange', linestyle=':', label='Batas anual konsentrasi senyawa NO2')
plt.axhline(y=nitlim['maksimal'], color='red', linestyle=':', label='Batas maksimal konsentrasi senyawa NO2')


#rincian grafik ozon
plt.title('Inspeksi Senyawa nitrogen dioksida sepanjang waktu')
plt.xlabel('Waktu (Tanggal dan waktu)')
plt.ylabel('Konsentrasi Nitrogen dioksida (µg/m³)')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
