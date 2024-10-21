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
min_date = beijingdf["datetime"].min()  # Tanggal minimal
max_date = beijingdf["datetime"].max()   #Tanggal maksimal

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
    
    start_date = min_date
    end_date = max_date
    # Mengambil start_date & end_date dari date_input
    seleksi = st.date_input(
        label='Filter Tanggal',
        min_value= min_date,
        max_value= max_date,
        value=(min_date, max_date)
    )
    #tampilkan hasil
    st.write("Tanggal Pilihan:", seleksi)
#--------------------------Pemilihan batas tanggal
awal,akhir = seleksi
awal = pd.to_datetime(awal)
akhir = pd.to_datetime(akhir)
#deklatasi 
filtrat['datetime'] = pd.to_datetime(filtrat['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
#pemfilteran grup data
filtered_data = filtrat[(filtrat['datetime'] >= awal) & (filtrat['datetime'] <= akhir)]

#--------------------------
#persiapan judul
st.header('Inspeksi Kualitas Udara in Beijing :sparkles:')
#tambahan 1: rata-rata mingguan
weekly = filtrat.resample('W-MON', on='datetime')[['PM2.5', 'PM10', 'CO', 'O3', 'NO2', 'SO2','TEMP','PRES','DEWP','WSPM','datetime']].mean().copy() 
weekly['datetime'] = pd.to_datetime(weekly['datetime']).copy()

# tambahan (Persiapan sub data) demi kemudahan
gruppar = filtered_data[["datetime", 'PM2.5', 'PM10']].copy() #Partikulat
gruppar["datetime"] = pd.to_datetime(gruppar['datetime'])

cogrp = filtered_data[['datetime', 'CO']].copy() #Senyawa CO
cogrp["datetime"] = pd.to_datetime(cogrp["datetime"])

ozgrp = filtered_data[['datetime', 'O3']].copy() # Senyawa ozon
ozgrp['datetime'] = pd.to_datetime(ozgrp['datetime'])

nigrp = filtered_data[['datetime', 'NO2']].copy() #Senyawa NO2
nigrp['datetime'] = pd.to_datetime(nigrp['datetime'])

sulgrp = filtered_data[['datetime', 'SO2']].copy() #Senyawa SO2
sulgrp['datetime'] = pd.to_datetime(sulgrp['datetime'])

temptgrp = filtered_data[['datetime', 'TEMP', 'DEWP']].copy()#SUhu dan Kelembapan
temptgrp['datetime'] = pd.to_datetime(temptgrp['datetime'])

#(data mingguan) persiapan data mingguan
wekpar = weekly[['datetime', 'PM2.5', 'PM10']].copy() #inspeksi partikulat mingguan
wekpar['datetime'] = pd.to_datetime(wekpar['datetime']) #diurutkan dari waktu

#Inspeksi Senyawa
wekcompound = weekly.resample('W-MON')[['CO', 'O3', 'NO2', 'SO2']].mean().copy()#salinan untuk senyawa lain

#Inspeksi aspek fisika
wekphs = weekly.resample('W-MON')[['TEMP', 'PRES', 'DEWP', 'WSPM']].mean().copy() #Inspeksi Aspek fisika

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
# Inspeksi grafik mingguan
for pollutant in ['PM2.5', 'PM10']:
    fig = px.bar(wekpar[pollutant],
                 title=f"Nilai rata-rata mingguan {pollutant.capitalize()} Levels",
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
                 title=f"Nilai rata-rata mingguan {pollutant.capitalize()} Levels",
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
                 title=f"Nilai rata-rata mingguan {pollutant.capitalize()} Levels",
                 labels={f'value_{pollutant}': f'{pollutant.capitalize()} levels'})
    
    # Batas Inspeksi
    if pollutant == 'TEMP':
        fig.add_hline(y=btsuhu['nol'], line_color='red', line_dash='dash',
                      annotation_text="Batas suhu beku", annotation_position="top right")
        fig.add_hline(y=btsuhu['dingin'], line_color='black', line_dash='dash',
                      annotation_text="Suhu dingin", annotation_position="top right")
        fig.add_hline(y=btsuhu['normal'], line_color='black', line_dash='dash',
                      annotation_text="Suhu Normal", annotation_position="top right")
        fig.add_hline(y=btsuhu['panas'], line_color='black', line_dash='dash',
                      annotation_text="Suhu Normal", annotation_position="top right")
        
    elif pollutant == 'PRES':
        fig.add_hline(y=atm, line_color='red', line_dash='dash',
                      annotation_text="Batas tekanan atmosfer", annotation_position="top right")
        
    elif pollutant in ['DEWP']:
        fig.add_hline(y=btlembap['kering'], line_color='red', line_dash='dash',
                      annotation_text="Batas kelembapan kering", annotation_position="top right")
        fig.add_hline(y=btlembap['biasa'], line_color='orange', line_dash='dash',
                      annotation_text="Batas kelembapan biasa", annotation_position="top right")
        fig.add_hline(y=btlembap['lembap'], line_color='orange', line_dash='dash',
                      annotation_text="Batas kelembapan tinggi", annotation_position="top right")

    st.plotly_chart(fig)

#---------------------(Grafik total)
# A2. Judul grafik Karbon Monoksida
st.header("Inspeksi senyawa karbon monoksida dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(15, 8))

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
plt.figure(figsize=(15, 8))

# Grafik Sebaran PM2.5
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
plt.figure(figsize=(15, 8))

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
#tampilkan hasil
st.pyplot(plt)
#------------------------------------------A5. Grafik Inspeksi Senyawa Nitrogen Dioksida
st.header("Inspeksi senyawa Nitrogen dioksida dalam suatu waktu")
# komponen grafik
plt.figure(figsize=(15, 8))

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
#tampilkan hasil
st.pyplot(plt)
#------------------------------------------A6. Grafik Inspeksi Suhu dan Kelembapan
# komponen grafik
plt.figure(figsize=(15, 8))

# Grafik Sebaran Suhu
plt.scatter(temptgrp['datetime'], temptgrp['TEMP'], color='blue', label='suhu', alpha=0.6)

# Grafik sebaran Kelembapan
plt.scatter(temptgrp['datetime'], temptgrp['DEWP'], color='black', label='kelembapan', alpha=0.6)


# Batas suhu dan kelmbapan
plt.axhline(y=nolim, color='darkblue', linestyle=':', label='Batas suhu nol')
plt.axhline(y=diglim, color='blue', linestyle=':', label='Batas suhu dingin')
plt.axhline(y=comdr, color='darkgreen', linestyle=':', label='Batas kelembapan optimal')
plt.axhline(y=humin, color='green', linestyle=':', label='Batas minimum kelembapan tinggi')
plt.axhline(y=nrmlim, color='orange', linestyle=':', label='Batas minimum suhu normal')
plt.axhline(y=pnslim, color='orange', linestyle=':', label='Batas minimum suhu panas')

#rincian grafik ozon
plt.title('Inspeksi Suhu dan Kelembapan sepanjang waktu')
plt.xlabel('Waktu (Tanggal dan waktu)')
plt.ylabel('Nilai Suhu dalam celsius')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()
#tampilkan hasil
st.pyplot(plt)