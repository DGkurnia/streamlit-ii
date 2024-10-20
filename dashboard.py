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
beijingdf['datetime'] = pd.to_datetime(beijingdf['datetime'], errors='coerce')

# Penentuan tanggal minimal dan maksimal
min_date = beijingdf["datetime"].min()   # Tanggal
max_date = beijingdf["datetime"].max()  

# Check if 'datetime' exists in beijingdf
if 'datetime' not in beijingdf.columns:
    raise KeyError("'datetime' column is missing from beijingdf")

# Data utama
main_df = beijingdf[(beijingdf["datetime"] >= str(min_date)) & 
                    (beijingdf["datetime"] <= str(max_date))]
main_df['datetime'] = pd.to_datetime(main_df['datetime'], errors='coerce')

# Check if main_df is empty after filtering
if main_df.empty:
    raise ValueError("main_df is empty after filtering with min_date and max_date.")

# Check if 'datetime' exists in main
if 'datetime' not in main_df.columns:
    raise KeyError("'datetime' column is missing from beijingdf")

# Pemilihan stasiun
stasiun_unik = main_df['station'].unique()

# Deklarasi
try:
    tahunan = main_df.groupby("datetime")
    print(tahunan.size())  # Check the size of each group
except ValueError as e:
    print(f"Error: {e}")

# Pilihan stasiun
pilihan = st.selectbox("Pilihan stasiun :", stasiun_unik)

# Filtrasi data
filtrat = main_df[main_df['station'] == pilihan]
#Persiapan data 
filtrat['datetime'] = pd.to_datetime(filtrat['datetime'])  # Ensure datetime format

# Ensure 'datetime' exists before converting to datetime format
if 'datetime' in filtrat.columns:
    filtrat["datetime"] = pd.to_datetime(filtrat["datetime"])
else:
    raise KeyError("'datetime' column is missing from filtrat")

#Laporan terkini
terkini = {
     'kota' : pilihan,
     'Kadar partikulat' : {'PM2.5': filtrat['PM2.5'].iloc[-1], 'PM10': filtrat['PM10'].iloc[-1]},
     'Senyawa CO': np.round(filtrat['CO'].iloc[-1],3),
     'Kadar ozon' : np.round(filtrat['O3'].iloc[-1],3),
     'Kadar sulfur di udara': np.round(filtrat['SO2'].iloc[-1],3),
     'Kadar nitrogen di udara': np.round(filtrat['NO2'].iloc[-1],3),
     'suhu (celsius)' : np.round(filtrat['TEMP'].iloc[-1],3),
     'kelembapan': np.round(filtrat['DEWP'].iloc[-1],3),
     'arah angin': filtrat['wd'].iloc[-1],
     'kecepatan angin': np.round(filtrat['WSPM'].iloc[-1],3),
     'kadar hujan': np.round(filtrat['RAIN'].iloc[-1],3)
}

# Penampilan grafik hasil jika ada record yang cocok dengan pemilihan user    
if len(filtrat)>0 :
     st.write(terkini)
else:
      print("Tidak ditemukan rekaman untuk stasiun tersebut")
#seleksi data tunggal
dtungal = {
    'datetime': pd.date_range(start= min_date, periods=100).copy(),
    'value': range(100)
}    

#Penambahan logo
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://seeklogo.com/images/S/streamlit-logo-1A3B208AE4-seeklogo.com.png")
    
    # Modifikasi tanggal awal dan akhir
    seleksi = st.date_input(
        label='Filter Tanggal',
        start_date=min_date,
        end_date=max_date,
        value=(min_date, max_date)
    )

    #pemeriksaan data untuk inspeksi
    if isinstance(seleksi, tuple):
        start_date, end_date = seleksi
    else:
        start_date = end_date = seleksi
#tampilkan jangkauan data
filtered_data = filtrat[(filtrat['datetime'].dt.date >= start_date) & 
                        (filtrat['datetime'].dt.date <= end_date)]
#tampilkan hasil
st.header("Data mingguan")
st.write(filtered_data)

#persiapan judul
st.header('Inspeksi Kualitas Udara in Beijing :sparkles:')

# tambahan (Persiapan sub data) demi kemudahan
gruppar = filtrat[["datetime", 'PM2.5', 'PM10']].copy() #inspeksi partikulat
gruppar["datetime"] = pd.to_datetime(gruppar['datetime']) #diurutkan dari waktu
#Senyawa CO
cogrp = filtrat[['datetime','CO']].copy() #inspeksi senyawa CO
cogrp["datetime"] = pd.to_datetime(cogrp["datetime"])
#senyawa ozon
ozgrp = filtrat[['datetime','O3']].copy() #inspeksi senyawa ozon
ozgrp['datetime'] = pd.to_datetime(ozgrp['datetime'])
#Nitrogen
nigrp = filtrat[['datetime','NO2']].copy() #inspeksi senyawa nitrogen
nigrp['datetime'] = pd.to_datetime(nigrp['datetime'])
#sulfur
sulgrp = filtrat[['datetime','SO2']].copy() #inspeksi senyawa sulfur
sulgrp['datetime'] = pd.to_datetime(sulgrp['datetime'])
#inspeksi di aspek fisika
tempgrp = filtrat[['datetime','TEMP','DEWP']].copy()# inspeksi suhu
tempgrp['datetime'] = pd.to_datetime(tempgrp['datetime'])

#tambahan 2: rata-rata mingguan
weekly = filtrat.resample('W-MON', on='datetime')[['PM2.5', 'PM10', 'CO', 'O3', 'NO2', 'SO2','TEMP','PRES','DEWP','WSPM','datetime']].mean().copy() 
weekly['datetime'] = pd.to_datetime(weekly['datetime']).copy()

#(data mingguan)
#persiapan data mingguan
wekpar = weekly[['datetime', 'PM2.5', 'PM10']].copy() #inspeksi partikulat mingguan
wekpar['datetime'] = pd.to_datetime(wekpar['datetime']) #diurutkan dari waktu

#Inspeksi Senyawa
wekcompound = weekly.resample('W-MON', on='datetime')[['CO', 'O3', 'NO2', 'SO2']].mean().copy()#salinan untuk senyawa lain

#Inspeksi aspek fisika
wekphs = weekly.resample('W-MON', on='datetime')[['TEMP', 'PRES', 'DEWP', 'WSPM']].mean().copy()

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
#tekanan (damal HPa)
atm = 1013.25
#kelembapan
[drl, comdr, humin] = [10, 15, 20]
#penulisan ulang batas suhu
btsuhu = {'nol' : nolim,'dingin': diglim,'normal': nrmlim, 'panas': pnslim}
#penulisan batas kelembapan
btlembap = {'kering': drl, 'biasa': comdr, 'lembap': humin}
#Batas Kecepatan angin
[btng, ring, meng, lmbt, sgr, kut] = [1, 3, 5, 11, 17, 24]


#--------------------Grafik mingguan
# Inspeksi grafik mingguan
for pollutant in ['PM2.5', 'PM10']:
    fig = px.bar(wekpar[pollutant],
                 title=f"Rata-rata mingguan {pollutant.capitalize()} Levels",
                 labels={'value': f'{pollutant.capitalize()} levels'})

    # Bagian batas aman
    fig.add_hline(y=safety_limits[f"{pollutant} anual"], line_color='orange', 
                  annotation_text="Annual Limit", annotation_position="top left")
    
    if pollutant == 'PM10':
        fig.add_hline(y=safety_limits[f"{pollutant} maksimal"], line_color='red',
                      annotation_text="Maximal Limit", annotation_position="top left")

# Inspeksi Senyawa
for pollutant in ['CO', 'O3', 'NO2', 'SO2']:
    fig = px.bar(wekcompound[[pollutant]],
                 title=f"Rata-rata mingguan {pollutant.capitalize()} Levels",
                 labels={f'value_{pollutant}': f'{pollutant.capitalize()} levels'})
    
    # Batas Inspeksi
    if pollutant == 'CO':
        fig.add_hline(y=complimit[pollutant]['China'], line_color='red', line_dash='dash',
                      annotation_text="Batas aman di China", annotation_position="top right")
        fig.add_hline(y=complimit[pollutant]['Global'], line_color='orange', line_dash='dash',
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

#Inspeksi Aspek fisika
for pollutant in ['TEMP', 'PRES', 'DEWP', 'WSPM']:
    fig = px.bar(wekphs[[pollutant]],
                 title=f"Rata-rata mingguan {pollutant.capitalize()} Levels",
                 labels={f'value_{pollutant}': f'{pollutant.capitalize()} levels'})
    
    # Batas Inspeksi suhu
    if pollutant == 'TEMP':
        fig.add_hline(y=btsuhu['nol'], line_color='red', line_dash='dash',
                      annotation_text="Batas suhu beku", annotation_position="top right")
        fig.add_hline(y=btsuhu['dingin'], line_color='black', line_dash='dash',
                      annotation_text="Suhu dingin", annotation_position="top right")
        fig.add_hline(y=btsuhu['normal'], line_color='black', line_dash='dash',
                      annotation_text="Suhu Normal", annotation_position="top right")
        fig.add_hline(y=btsuhu['panas'], line_color='black', line_dash='dash',
                      annotation_text="Suhu Normal", annotation_position="top right")
    # Batas Inspeksi tekanan    
    elif pollutant == 'PRES':
        fig.add_hline(y=atm, line_color='red', line_dash='dash',
                      annotation_text="Batas tekanan atmosfer", annotation_position="top right")
    # Batas Inspeksi kelembapan    
    elif pollutant in ['DEWP']:
        fig.add_hline(y=btlembap['kering'], line_color='red', line_dash='dash',
                      annotation_text="Batas kelembapan kering", annotation_position="top right")
        fig.add_hline(y=btlembap['biasa'], line_color='orange', line_dash='dash',
                      annotation_text="Batas kelembapan biasa", annotation_position="top right")
        fig.add_hline(y=btlembap['lembap'], line_color='orange', line_dash='dash',
                      annotation_text="Batas kelembapan tinggi", annotation_position="top right")
    # Batas Inspeksi kecepatan angin
    elif pollutant in ['WSPM']:
        fig.add_hline(y=btng, line_color='darkblue', line_dash='dash',
                      annotation_text="Batas Kecepatan tenang", annotation_position="top right")
        fig.add_hline(y=ring, line_color='blue', line_dash='dash',
                      annotation_text="Batas kecepatan angin tenang", annotation_position="top right")
        fig.add_hline(y=meng, line_color='lightblue', line_dash='dash',
                      annotation_text="Batas tenegah di angin tenang", annotation_position="top right")
        fig.add_hline(y=lmbt, line_color='green', line_dash='dash',
                      annotation_text="Batas untuk angin lambat", annotation_position="top left")
        fig.add_hline(y=sgr, line_color='yellow', line_dash='dash',
                      annotation_text="Batas untuk menegah di angin tenang", annotation_position="top left")
        fig.add_hline(y=kut, line_color='red', line_dash='dash',
                      annotation_text="Batas untuk menegah di angin tenang", annotation_position="top left")

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
#tampilkan hasil
st.pyplot(plt)
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
#tampilkan hasil
st.pyplot(plt)
#--------------------------------------------A4 Inspeksi senyawa ozon
st.header("Inspeksi senyawa ozon dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(12, 6))

# Inspeksi ozon
plt.scatter(ozgrp['datetime'], ozgrp['O3'], color='purple', label='Nilai CO', alpha=0.6)


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
#tampilkan hasil
st.pyplot(plt)
#------------------------------------------A5. Grafik Inspeksi Senyawa Nitrogen Dioksida
st.header("Inspeksi senyawa Nitrogen dioksida dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(12, 6))

# Inspeksi ozon
plt.scatter(nigrp['datetime'], nigrp['NO2'], color='black', label='Nilai NO2', alpha=0.6)


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
#tampilkan hasil
st.pyplot(plt)
#------------------------------------------A6. Grafik Inspeksi Senyawa Sulfur Dioksida
st.header("Inspeksi senyawa Nitrogen dioksida dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(12, 6))

# Inspeksi senyawa sulfur dioksida
plt.scatter(sulgrp['datetime'], sulgrp['SO2'], color='darkyellow', label='Nilai SO2', alpha=0.6)


# Batas ozon
plt.axhline(y=nitlim['anual'], color='orange', linestyle=':', label='Batas anual konsentrasi senyawa SO2')
plt.axhline(y=nitlim['maksimal'], color='red', linestyle=':', label='Batas maksimal konsentrasi senyawa SO2')


#rincian grafik ozon
plt.title('Inspeksi Senyawa sulfur dioksida sepanjang waktu')
plt.xlabel('Waktu (Tanggal dan waktu)')
plt.ylabel('Konsentrasi Sulfur dioksida (µg/m³)')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()
#tampilkan hasil
st.pyplot(plt)