# Proyek Inspeksi udara ✨

## Komponen Colab
```
a. dataset kotor yang terismpan di folder 'aqins' di bagian notebook
b. catatan google colab
c. ilustrasi hasil
```

## Komponen Dashboard

```
dashboard : Streamlit dashboard
data dashboaed: beijingdf.csv
teks requirement
file json comp dengan nama 'launch.jsonc'
```

#### Rincian komponen submisi
```
link dashboard : https://dummyaqidash.streamlit.app/
data : dataset AQI (beijingdf)
Notebook colab : airquality.ipynb 
link ke colab : https://colab.research.google.com/drive/1Dm7FyKKAo8SHvwUhlsJEXIb2MsrruYwv?usp=sharing
```
#### Informasi data
```
a informasi partikulat di dua kondisi berbeda
**Resume Inspeksi Partikulat**
* Bagian inspeksi partikulat ukuran 2.5 mikrometer
*- Total kasus partikulat melewati batas anual untuk semua kota sudah melewati 10 ribu
*- Di sisi lain, kasus partikulat 2.5 mikro yang melampaui ambang batas sudah menembus 20 ribu.
*- Kota Changping, Kota Huairou, dan Kota Dingling mempunyai kasus partikulat yang melewati batas maksimal untuk ukuran 2.5 mikro di atas 30 ribu. Kota Dingling adalah kota yang paling tinggi diantara ketiganya.
*-Melanjuti hal sebelumnya, kota Huairo di urutan kedua tertinggi
* Bagian inspeksi partikulat ukuran 10 mikrometer
*- Jumlah kasus partikulat melewati batas anual partikulat 10 mikrometer untuk semua kota sudah melewati 5 ribu.
*- Ada empat kota (Changping, Dingling, Huairou, Tiantan) yang melewati delapan ribu kasus untuk partikulat melewati batas anual
*- Total kasus yang melampaui batas maksimal partikulat sudah melampaui 10 ribu.
*- Kota Dingling adalah satu-satunya kota dengan total kasus partikulat ukuran 10 mikro yang melewati batas maksimal yang memiliki nilai di atas 20 ribu.

b. informasi untuk senyawa CO
- Semua kadar gas karbon monoksida (CO) di cina tidak melewati batas global
- Inspeksi kadar gas 'CO' untuk standar level cina:
- 11 dari 12 yang memiliki kadar CO di atas 1000 mikrometer per meter kubik (standar cina) sehingga Kelompok kota ini melebihi batas aman kadar CO standar cina.
- Ada dua kota, Huairou & Dingling, yang memiliki kasus kadar CO dengan kadar melewati batas cina dengan nilai di bawah 500

c. inspeksi kadar ozon
Inspeksi (Insight) di pemeriksan senyawa ozon/O3:**
- 1. Semua kota memiliki total kadar ozon paling tinggi melebihi 1500 unit
- 2. Kota dengan total kasus paling banyak untuk ozon paling tinggi adalah 'Kota Nonzhanguan' dengan total kasus 2600
- 3. Mayoritas kota mempunyai kadar ozon yang melebihi batas minimal dengan
- 4. Kota Dingling adalah kota dengan kasus ozon optimal sangat banyak
- 5. Semua kasus ozon yang dominan di data adalah kasus dengan kadar ozon rendah dengan kasus terbanyak dialami di kota Wanliu dengan total melewati 20 ribu (tepatnya 22259)
- 6. Semua kote memiliki kasus ozon optimal dengan semua nilai diatas 10 ribu (paling rendah di Wanliu, paling tinggi di Dingling)

d. inspeksi senyawa SO2 (sulfur dioksida)
- a. Kota Wanahouxigong adalah satu dari dua kota yang pernah mengalami kasus kadar sulfur dioksida di atas batas anual (nilainya "jauh" lebih rendah daripada kasus di Gucheng)
- b. Semua kota belum memiliki kasus sulfur dioksida melewati batas maksimal
- c. Kota Gucheng memiliki kasus kadar SO2 melewati anual paling tinggi

e. Inspeksi senyawa NO2
-a. Kota Dingling adalah satu-satunya kota dengan satu kasus nitrogen dioksida melewati batas maksimal yang dibolehkan, kota ini adalah satu dari empat kota dengan kasus dibawah sepuluh untuk kelebihan kadar nitrogen dioksida yang melewati batas maksimal.
-b. Mayoritas kasus untuk inspeksi senyawa NO2/ nitrogen dioksida adalah 'melewati batas anual'
-c. Dari empat kota dengan kasus nitrogen dioksida melewati batas maksimal yang dibolehkan, Kota Wanliu adalah kota dengan nilai paling tinggi


```
### Komando  di Streamlit
```
a. git clone https://github.com/DGkurnia/streamlit-ii #Isi dokuman dashboard.py
b. install git github desktop #Demi memeindahkan file 'beijingdf.csv' 
c. proses 'clone' dari laptop ke github untuk memasukan file 'beijingdf.csv'
d. Publikasi di streamlit.share.io
e. lakukan pengeditan
```


### Eksekusi komando dashboard
```
a. siapkan repositori 'streamlit-ii' di github
b. pastikan elemen di dalam sudah sesuai
c. link ke streamlit: 'https://dummyaqi.streamlit.app/'

```




### Instalasi di Streamlit
```
pip install streamlit
pip install -r requirements.txt # untuk instalasi file di vscode
instal di streamlit online dengan url : https://dummyaqidash.streamlit.app/
```


