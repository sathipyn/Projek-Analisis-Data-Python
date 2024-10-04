# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configurasi untuk tampilan Streamlit
st.set_page_config(page_title="Analisis Peminjaman Sepeda", layout="wide")
st.title("Dashboard Analisis Peminjaman Sepeda")

# Load dataset
day_df = pd.read_csv('D:\KULIah UNESA\Bangkit Learning\Dicoding\day.csv')
hour_df = pd.read_csv('D:\KULIah UNESA\Bangkit Learning\Dicoding\hour.csv')

# Format kolom datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mendapatkan tanggal minimum dan maksimum dari dataset
min_date_days = day_df["dteday"].min()
max_date_days = day_df["dteday"].max()

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")

# Menambahkan logo perusahaan atau gambar
st.sidebar.image("https://media.istockphoto.com/id/1329906434/vector/city-bicycle-sharing-system-isolated-on-white.jpg?s=612x612&w=0&k=20&c=weiMZhJoWWzNGtx7khfXPbE3s2Lpw5n6M7iWoxCsBPU=")

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Waktu",
    value=(min_date_days, max_date_days),  
    min_value=min_date_days,
    max_value=max_date_days
)

filtered_day_df = day_df[(day_df["dteday"] >= pd.Timestamp(start_date)) & (day_df["dteday"] <= pd.Timestamp(end_date))]

total_count = filtered_day_df["cnt"].sum()
st.sidebar.metric(label="Total Peminjaman Sepeda", value=total_count)

option = st.sidebar.selectbox("Pilih Analisis", 
                              ("Pengaruh Kondisi Cuaca", "Tren Peminjaman Sepeda Harian"))

if st.sidebar.checkbox("Tampilkan Data"):
    st.write("Data Harian:")
    if not filtered_day_df.empty:  # Memastikan data tidak kosong
        st.write(filtered_day_df.head())
    else:
        st.write("Tidak ada data untuk rentang waktu yang dipilih.")
        
    st.write("Data Jam:")
    st.write(hour_df.head())

# Case 1: Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman
if option == "Pengaruh Kondisi Cuaca":
    st.subheader("Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman Sepeda")

    weather_data = filtered_day_df.groupby('weathersit').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    weather_data['weathersit'] = weather_data['weathersit'].map({
        1: 'Cerah',
        2: 'Kabut',
        3: 'Hujan Ringan/Salju',
        4: 'Hujan Lebat'
    })

    fig, ax = plt.subplots(figsize=(8, 4))
    bar_width = 0.35
    x = np.arange(len(weather_data['weathersit']))

    ax.bar(x - bar_width, weather_data['cnt'], width=bar_width, label='Total Peminjaman', color='skyblue')
    ax.bar(x, weather_data['casual'], width=bar_width, label='Pengguna Kasual', color='orange')
    ax.bar(x + bar_width, weather_data['registered'], width=bar_width, label='Pengguna Terdaftar', color='green')

    ax.set_xticks(x)
    ax.set_xticklabels(weather_data['weathersit'])
    ax.set_title('Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman Sepeda')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Peminjaman')
    ax.legend()

    st.pyplot(fig)

    st.markdown("""
    Kesimpulan:
    - Cuaca cerah memiliki jumlah peminjaman sepeda tertinggi, terutama untuk pengguna kasual.
    - Cuaca buruk seperti hujan atau salju secara signifikan menurunkan jumlah peminjaman.
    - Pengguna terdaftar lebih cenderung tetap meminjam sepeda meskipun kondisi cuaca kurang baik.
    """)

# Case 2: Tren Peminjaman Sepeda Berdasarkan Jam dalam Sehari
elif option == "Tren Peminjaman Sepeda Harian":
    st.subheader("Tren Peminjaman Sepeda Berdasarkan Jam dalam Sehari")

    hour_df['workingday'] = hour_df['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})

    hour_avg = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()

   
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=hour_avg, x='hr', y='cnt', hue='workingday', marker='o', ax=ax, palette={"Akhir Pekan": 'orange', "Hari Kerja": 'blue'})
    ax.set_title('Tren Peminjaman Sepeda per Jam (Hari Kerja vs Akhir Pekan)')
    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax.legend(title='Tipe Hari')
    
    st.pyplot(fig)

    st.markdown("""
    Kesimpulan:
    - Pada hari kerja, terdapat dua puncak peminjaman: pagi dan sore, yang menunjukkan pola penggunaan untuk komuter.
    - Pada akhir pekan, peminjaman lebih tinggi di tengah hari hingga sore, menunjukkan penggunaan untuk rekreasi.
    - Distribusi ini menunjukkan bahwa waktu dan hari sangat memengaruhi tren peminjaman sepeda.
    """)