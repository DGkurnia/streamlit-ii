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
st.header('Air Quality in China :sparkles:')
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
#------------------------------------------
#Grafik partikulat untuk Inspeksi partikulat (nilai PM2.5 & nilai PM10)
[anPMa, dlPMa, anPMb, dlPMb] = [40, 150, 35, 75] 
#Batas aman
safety_limits = {'PM2.5 anual': anPMa,  'PM2.5 maksimal': dlPMa, # Batas anual dan Maksimal PM 2.5   
                 'PM10 anual': anPMb, 'PM10 maksimal': dlPMb} #Batas anual dan maksimal PM.10
#Keterangan (1. a adalah inepeksi PM2.5 b adalah PM10 2. kode an adalah anual kode ma adalah nilai maksimal)
fig = px.line(filtrat, x='datetime', y=['PM2.5', 'PM10'],
              labels={['PM2.5','PM10']: 'Kadar Partikulat', 'datetime': 'Tanggal'},
              title='Inspeksi Partikulat')
#Inspeksi Batas Aman
for pollutant, limit in safety_limits.items():
    fig.add_hline(y=limit, line_color="red", line_dash="dash",
                   annotation_text=f"{pollutant} Batas aman: {limit} µg/m³", 
                   annotation_position="top right")
#Pemeriksaan batas partikulat
batasanu = filtrat[(filtrat['PM2.5'] > safety_limits['PM2.5 anual'] & filtrat['PM2.5'] < safety_limits['PM2.5 maksimal']) 
                 | (filtrat['PM10'] > safety_limits['PM10 anual'] & filtrat['PM10'] < safety_limits['10 maksimal'])] #Batas anual
lwt = filtrat[(filtrat['PM2.5'] > safety_limits['PM2.5 maksimal']) | (filtrat['PM10'] > safety_limits['PM10 maksimal'])] #Batas maksimal
#Area batas anual
if not lwt.empty:
    st.warning("Peringatan : Ini sudah terlalu bahaya")
elif not batasanu.empty and lwt.empty:
    st.warning("Peringatan : Ini harus hati-hati") #Kasus melewati batas anual (tapi di dibawah nilai maksimal)
else:
    st.success("Kadar udara masih aman")
#Ilustrasi normal untuk partikulat
st.plotly_chart(fig)

#------------------------------------------
#Inspeksi batas senyawa karbon monoksida dan tiga senyawa lainnya
[cochl, cogl, ozmin, ozmax, nmax, smax ] = [4000, 30000, 50, 160, 200, 500]
#Deklarasi batas senyawa
colim = { 'China' : cochl, 'Global' : cogl} #Batas senyawa CO
ozlim = { 'minimum' : ozmin,'maksimum' : ozmax } #Ozon/ ozon
nitlim = {'anual': 40, 'maksimal' : nmax} # nitrogen dioksida (NO2)
sulplim = {'anual': 40, 'maksimal': smax} #Sulfur dioksida

#Pemeriksaan senyawa CO
#Grafik pengecekan senyawa karbon monoksida (CO)
fig = px.line(filtrat, x='datetime', y=['CO'],
              labels={'CO': 'Konsentrasi CO', 'datetime': 'Tanggal'},
              title='Inspeksi Partikulat')
#Inspeksi Batas Aman
for pollutant, limit in colim.items():
    fig.add_hline(y=limit, line_color="red", line_dash="dash",
                   annotation_text=f"{pollutant} Batas aman: {limit} µg/m³", 
                   annotation_position="top right")
#Ilustrasi normal untuk senyawa (CO)
st.plotly_chart(fig)
#Pemeriksaan batas partikulat
lwtchina = filtrat[(filtrat['CO'] > colim['China']) & (filtrat['CO'] < colim['Global'])] #Batas di 
lwtglobal = filtrat[(filtrat['CO'] > colim['Global'])] #Batas aglobal
#Area batas anual
if not lwtglobal.empty:
    st.warning("Peringatan : Ini sudah terlalu bahaya untuk global juga")
elif not lwtchina.empty and lwtglobal.empty:
    st.warning("Peringatan : Otoritas china boleh melarang ini") # 
else:
    st.success("Kadar senyawa CO masih aman")
#-----------------------------------------------
#Inspeksi senyawa Ozon (Grafik inspeksi O3)
#Grafik pengecekan senyawa Ozon (O3)
fig = px.line(filtrat, x='datetime', y=['O3'],
              labels={'O3': 'Konsentrasi ozon', 'datetime': 'Tanggal'},
              title='Inspeksi Senyawa ozon')
#Inspeksi Batas Aman
for pollutant, limit in ozlim.items():
    fig.add_hline(y=limit, line_color="red", line_dash="dash",
                   annotation_text=f"{pollutant} Batas aman: {limit} µg/m³", 
                   annotation_position="top right")
#Ilustrasi normal untuk senyawa (CO)
st.plotly_chart(fig)
#Pemeriksaan kadar ozon
ozrdh = filtrat[(filtrat['O3'] < ozlim['minimum'])] #rendah
ozopti = filtrat[(filtrat['O3'] > ozlim['minimum']) & (filtrat['O3'] < ozlim['maksimum'])] #optimal
ozmaks = filtrat[(filtrat['O3'] > ozlim['maksimum'])]
#Kondisional untuk senaywa ozon
if not ozmaks.empty :
    st.warning("Kadar ozon sangat tinggi")
elif (ozmaks.empy and ozrdh.empy) and not ozopti.empty:
    st.success("Kadar ozon masih aman")
else:
    st.warning("Kadar ozon sangat rendah")
#----------------------------------
#Inspeksi senyawa Nitrogen dioksida (Grafik inspeksi NO2)
#Grafik pengecekan senyawa Nitrogen Dioksida (NO2)
fig = px.line(filtrat, x='datetime', y=['NO2'],
              labels={'NO2': 'Konsentrasi NO2', 'datetime': 'Tanggal'},
              title='Inspeksi Partikulat')
#Inspeksi Batas Aman
for pollutant, limit in nitlim.items():
    fig.add_hline(y=limit, line_color="red", line_dash="dash",
                   annotation_text=f"{pollutant} Batas aman: {limit} µg/m³", 
                   annotation_position="top right")
#Ilustrasi normal untuk senyawa (NO2)
st.plotly_chart(fig)
#Pemeriksaan kondisi NO2
nitinggi = filtrat[(filtrat['NO2'] < nitlim['maksimum']) & (filtrat['NO2'] > nitlim['anual'])]
nibhy = filtrat[(filtrat['NO2'] > nitlim['maksimum'])]
#Kondisional senyawa NO2
if not nibhy.empty:
    st.warning("Kadar nitrogen dioksida terlalu berbahaya")
elif nibhy.empty and not nitinggi.empty:
    st.warning("Kadar nitrogen dioksida tinggo")
else :
    st.success("Kadar masih aman")
    st.success("Kadar masih aman")