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

## Persiapan dataset
beijingdf = pd.read_csv('beijingdf.csv')
beijingdf.sort_values(by="datetime", inplace=True)
beijingdf.reset_index(inplace=True)

# Konversi kolom tanggal menjadi tanggal
beijingdf['datetime'] = pd.to_datetime(beijingdf['datetime'])

# Penentuan tanggal minimal dan maksimal
min_date = beijingdf["datetime"].min().strftime('%Y-%m-%d')  # Tanggal
max_date = beijingdf["datetime"].max().strftime('%Y-%m-%d')  

# Data utama dalam rentang waktu tertentu (optional)
main_df_filtered_dates = beijingdf[
        (beijingdf["datetime"] >= min_date) &
        (beijingdf["datetime"] <= max_date)]

# Pemilihan stasiun
unik = main_df_filtered_dates['station'].unique()
pilihan = st.selectbox("Pilih Stasiun:", unik)

# Deklarasi grup oleh tgl & stsiun
hasil = main_df_filtered_dates.groupby(['datetime','station']).filter(lambda x:x.station==pilihan)
filtrat = hasil.copy()

#Laporan terkini
terkini = {
     'kota' : pilihan,
     'Kadar partikulat' : [(filtrat['PM2.5'].iloc[-1]),(filtrat['PM10'].iloc[-1])],
     'Senyawa CO': filtrat['CO'].iloc[-1],
     'Kadar sulfur di udara': filtrat['SO2'].iloc[-1],
     'Kadar nitrogen di udara': filtrat['NO2'].iloc[-1],
     'suhu (celsius)' : filtrat['TEMP'].iloc[-1]
}

# Penampilan grafik hasil jika ada record yang cocok dengan pemilihan user    
if len(filtrat)>0 :
     st.write(terkini)
else:
      print("Tidak ditemukan rekaman untuk stasiun tersebut")
    
#Penampilan grafik laporan
st.write(terkini)
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
st.header('Inspeksi Kualitas Udara in Beijing :sparkles:')


#------------------------------------------------------------------------------------
# A.1 Grafik partikulat untuk Inspeksi keamanan partikulat (nilai PM2.5 & nilai PM10)
[anPMa, dlPMa, anPMb, dlPMb] = [40, 150, 35, 75] 

#Batas aman partikulat
safety_limits = {'PM2.5 anual': anPMa,  'PM2.5 maksimal': dlPMa, # Batas anual dan Maksimal PM 2.5   
                 'PM10 anual': anPMb, 'PM10 maksimal': dlPMb} #Batas anual dan maksimal PM.10
#Keterangan (1. a adalah inepeksi PM2.5 b adalah PM10 2. kode an adalah anual kode ma adalah nilai maksimal)

# A.2 Deklarasi sub kepala grafik
# A.2 Deklarasi sub kepala grafik
fig = px.line(filtrat, x='datetime', y=['PM2.5', 'PM10'], title='Level Partikulat untuk dua Kondisi')
fig.add_hline(y=safety_limits['PM2.5 maksimal'], line_dash="dash", line_color="red", annotation_text="Batas Maksimal Partikulat PM2.5")
fig.add_hline(y=safety_limits['PM2.5 anual'], line_dash="dash", line_color="orange", annotation_text="Batas Anual Partikulat PM2.5")
fig.add_hline(y=safety_limits['PM10 anual'], line_dash="dash", line_color="grey", annotation_text="Batas Anual Partikulat PM10")
fig.add_hline(y=safety_limits['PM10 maksimal'], line_dash="dash", line_color="yellow", annotation_text="Batas Maksimal Partikulat PM10")

# Display the dashboard
st.title("Grafik Inspeksi Partikulat untuk dua kondisi")
st.plotly_chart(fig)

#------------------------------------------
#Inspeksi batas senyawa karbon monoksida dan tiga senyawa lainnya
[cochl, cogl, ozmin, ozmax, nmax, smax ] = [4000, 30000, 50, 160, 200, 500]
#Deklarasi batas senyawa
colim = { 'China' : cochl, 'Global' : cogl} #Batas senyawa CO
ozlim = { 'minimum' : ozmin,'maksimum' : ozmax } #Ozon/ ozon (O3)
nitlim = {'anual': 40, 'maksimal' : nmax} # nitrogen dioksida (NO2)
sulplim = {'anual': 40, 'maksimal': smax} #Sulfur dioksida (SO2)


