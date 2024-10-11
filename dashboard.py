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
for column in date:
    beijingdf[column] = pd.to_datetime(beijingdf[column])


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
st.header('Inspeksi Kualitas Udara in Beijing :sparkles:')
#Data utama
main_df = beijingdf[(beijingdf["datetime"] >= str(start_date)) & 
                (beijingdf["datetime"] <= str(end_date))]

#Pemilihan stasiun
unik = main_df['station'].unique()

#Deklarasi
tahunan = main_df.groupby(["datetime","station"])

#pilihan stasiun
pilihan = st.selectbox("Pilihan stasiun :", unik)

# Filtrasi data
filtrat = tahunan[tahunan['station'].unique() == unik]

# Deklarasi tanggal
filtrat.set_index('datetime', inplace=True)

#Penampilan grafik hasil
st.write(filtrat)
#------------------------------------------------------------------------------------
# A.1 Grafik partikulat untuk Inspeksi keamanan partikulat (nilai PM2.5 & nilai PM10)
[anPMa, dlPMa, anPMb, dlPMb] = [40, 150, 35, 75] 
#Batas aman
safety_limits = {'PM2.5 anual': anPMa,  'PM2.5 maksimal': dlPMa, # Batas anual dan Maksimal PM 2.5   
                 'PM10 anual': anPMb, 'PM10 maksimal': dlPMb} #Batas anual dan maksimal PM.10
#Keterangan (1. a adalah inepeksi PM2.5 b adalah PM10 2. kode an adalah anual kode ma adalah nilai maksimal)

# A.2 Deklarasi sub kepala grafik
st.subheader("Inspeksi Partikulat")

if st.checkbox("Show Interactive Plots"):
    pm25_fig = px.line(filtrat, x=filtrat.index, y='pm25', name='PM2.5')
    pm10_fig = px.line(filtrat, x=filtrat.index, y='pm10', name='PM10')

    fig = pm25_fig | pm10_fig
    
    # Penambahan Partikulat
    fig.add_hline(y=anPMa, annotation_text=f'Safe Limit ({anPMa})', row=0,
                  col=-1).update(line_width=2)
    
    fig.add_hline(y=dlPMa, annotation_text=f'Max Safe Limit ({dlPMa})', row=0,
                  col=-1).update(line_style='dashdot', line_width=2)
    
    fig.add_hline(y=anPMb, annotation_text=f'Safe Limit ({anPMb})', row=1,
                  col=-1).update(line_width=2)
    
    fig.add_hline(y=dlPMb, annotation_text=f'Max Safe Limit ({dlPMb})', row=1,
                  col=-1).update(line_style='dashdot', line_width=2)
    
    st.plotly_chart(fig, HEIGHT=800,WIDTH=800, TITLE=F'Inspeksi Konsentrasi Partikulat')

#------------------------------------------
#Inspeksi batas senyawa karbon monoksida dan tiga senyawa lainnya
[cochl, cogl, ozmin, ozmax, nmax, smax ] = [4000, 30000, 50, 160, 200, 500]
#Deklarasi batas senyawa
colim = { 'China' : cochl, 'Global' : cogl} #Batas senyawa CO
ozlim = { 'minimum' : ozmin,'maksimum' : ozmax } #Ozon/ ozon (O3)
nitlim = {'anual': 40, 'maksimal' : nmax} # nitrogen dioksida (NO2)
sulplim = {'anual': 40, 'maksimal': smax} #Sulfur dioksida (SO2)


