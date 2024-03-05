import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

day_df = pd.read_csv("https://raw.githubusercontent.com/ipenn13/proyek-akhir-data/main/dashboard/day_df.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/ipenn13/proyek-akhir-data/main/dashboard/hour_df.csv")

day_hours_df = pd.merge(
    left=day_df,
    right=hour_df,
    how="left",
    left_on="dteday",
    right_on="dteday"
)

def categorize_hour(hr):
    if 0 <= hr < 6:
        return 'Dini Hari'
    elif 6 <= hr < 12:
        return 'Pagi'
    elif 12 <= hr < 18:
        return 'Siang'
    else:
        return 'Malam'
    
day_hours_df['hour_categorize'] = day_hours_df['hr'].apply(categorize_hour)
day_hours_df.groupby(['weekday_x', 'hour_categorize']).agg({'dteday':'nunique','cnt_y': 'sum'})

st.header("Bike Rent Dashboard :bike:")

with st.sidebar:
    # Menambahkan logo sepeda
    st.image("https://cdn-icons-png.flaticon.com/512/5320/5320247.png")
    st.header("Proyek Analisis Data")
    st.subheader("Bangkit Academy")
    st.write("by Ivan Danendra Ramadhnani")

st.subheader("Total Rents")

col1,col2,col3=st.columns(3)
with col1:
    total_rent = day_df.cnt.sum()
    st.metric("Total", value=total_rent)

with col2:
    total_casual =  day_df.casual.sum()
    st.metric("Casual Users",value=total_casual)

with col3:
    total_registered = day_df.registered.sum()
    st.metric("Registered Users", value=total_registered)

st.subheader("Total Renters by Season")
sum_season_df = day_df.groupby(by='season').agg({'dteday':'nunique', 'cnt': 'sum'})

# Membuat visualisasi untuk jumlah penyewa berdasarkan musim
fig1, ax1 = plt.subplots(figsize=(21, 7))
sns.barplot(x="season", y="cnt", data=sum_season_df, ax=ax1)
plt.title("Jumlah Penyewa Berdasarkan Musim")
ax1.set_ylabel(None)
ax1.set_ylim(400000, 1100000)
ax1.yaxis.set_major_formatter('{x:,.0f}')
ax1.set_xticklabels(["Springer", "Summer", "Fall", "Winter"])

# Tampilkan plot menggunakan st.pyplot()
st.pyplot(fig1)

#Membuat penjelasan untuk gambar pertama
with st.expander("Penjelasan gambar 1"):
    st.write("Sepeda paling banyak disewa pada musim gugur dengan total penyewa 1.061.129 dan yang paling sedikit pada musim semi dengan total penyewa 471.348. Selisih jumlah penyewa pada musim gugur dengan musim yang lain terbilang sedikit, tetapi selisih dengan musim semi cukup jauh dan jumlah penyewa pada musim semi bisa dibilang cukup anjlok.")

#Membuat visualisasi untuk jumlah penyewa berdasarkan hari dan waktu
st.subheader("Total Rentes by Day and Time")
sum_day_categorizeHour_df = day_hours_df.groupby(by=['weekday_x','hour_categorize']).agg({'cnt_y': 'sum'})
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.barplot(x='weekday_x', y='cnt_y', hue='hour_categorize', data=sum_day_categorizeHour_df,ax=ax2)

plt.title('Jumlah Penyewa Berdasarkan Hari dan Waktu')
plt.xlabel(None)
ax2.set_ylabel(None)
ax2.set_xticklabels(['Minggu','Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])

plt.legend(title='Kategori Jam')
st.pyplot(fig2)

#Membuat penjelasan untuk gambar kedua
with st.expander("Penjelasan gambar 2"):
    st.write("Sepeda paling banyak disewa pada hari sabtu siang dengan total 233.632 dan disusul minggu siang dengan total penyewa 224.661 sementara paling sedikit adalah selasa dini hari dengan total penyewa 8.091. Terlihat bahwa dini hari merupakan waktu yang paling sedikit sepeda disewa karena waktu tersebuta adalah waktunya orang istirahat.")
