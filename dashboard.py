import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style = "dark")

#Fungsi untuk menyiapkan data penyewa per hari
def create_daily_df(df):
    daily_df = df.groupby(by = "dteday").agg({
        "cnt": "sum"
    }).reset_index()
    return daily_df

#Fungsi untuk menyiapkan data penyewa per hari yang dikelompokkan berdasarkan tipe penyewa casual
def create_daily_casual_df(df):
    daily_casual_df = df.groupby(by = "dteday").agg({
        "casual": "sum"
    }).reset_index()
    return daily_casual_df

#Fungsi untuk menyiapkan data penyewa per hari yang dikelompokkan berdasarkan tipe penyewa registered
def create_daily_registered_df(df):
    daily_registered_df = df.groupby(by = "dteday").agg({
        "registered": "sum"
    }).reset_index()
    return daily_registered_df

#Fungsi untuk menyiapkan data per tahun
def create_yearly_df(df):
    yearly_df = df.groupby(by = ["mnth", "yr"]).agg({
        "cnt": "sum"
    }).reset_index()
    return yearly_df

#Fungsi untuk menyiapkan data per bulan
def create_monthly_df(df):
    monthly_df = df.groupby(by = "mnth").agg({
        "cnt": "sum"
    })
    monthly_df = monthly_df.reindex(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], fill_value = 0)
    return monthly_df

#Fungsi untuk menyiapkan data per hari kerja
def create_workingday_df(df):
    workingday_df = df.groupby(by = ["workingday", "season"]).agg({
        "cnt": "sum"
    }).reset_index()
    return workingday_df

#Fungsi untuk menyiapkan data per hari libur
def create_holiday_df(df):
    holiday_df = df.groupby(by = ["holiday", "season"]).agg({
        "cnt": "sum"
    }).reset_index()
    return holiday_df

#Fungsi untuk menyiapkan data per jam
def create_hour_df(df):
    hour_df = df.groupby(by = ["hr", "weekday"]).agg({
        "cnt": "sum"
    }).reset_index()
    return hour_df

data_df = pd.read_csv("data.csv")

#Membuat filter
min_date = pd.to_datetime(data_df["dteday"]).dt.date.min()
max_date = pd.to_datetime(data_df["dteday"]).dt.date.max()

with st.sidebar:
    st.image("Bike Sharing.jpeg")
    start_date, end_date = st.date_input(
        label = "Date Range",
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

main_df = data_df[(data_df['dteday'] >= str(start_date)) & (data_df['dteday'] <= str(end_date))]

daily_df = create_daily_df(main_df)
daily_casual_df = create_daily_casual_df(main_df)
daily_registered_df = create_daily_registered_df(main_df)
yearly_df = create_yearly_df(main_df)
monthly_df = create_monthly_df(main_df)
workingday_df = create_workingday_df(main_df)
holiday_df = create_holiday_df(main_df)
hour_df = create_hour_df(main_df)

#Membuat judul dashboard
st.header("Dashboard for Bike Rental :sparkles:")

#Menampilkan informasi total penyewaan per hari
st.subheader("Daily Rentals:")
col1, col2, col3 = st.columns(3)

with col1:
    daily_casual = daily_casual_df["casual"].sum()
    st.metric("Casual Users", value = daily_casual)

with col2:
    daily_registered = daily_registered_df["registered"].sum()
    st.metric("Registered Users", value = daily_registered)
 
with col3:
    daily_total = daily_df["cnt"].sum()
    st.metric("Total Users", value = daily_total)

#Membuat visualisasi data untuk penyewaan per tahun
st.subheader("Yearly Rentals:")
yearly_df["mnth"] = pd.Categorical(yearly_df["mnth"], categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], ordered = True)
fig, ax = plt.subplots(figsize = (10, 5))
sns.lineplot(
    x = yearly_df["mnth"],
    y = yearly_df["cnt"],
    hue = yearly_df["yr"],
    marker = "o"
)
ax.set_title("Number of Users by Month and Year", loc = "center", fontsize = 15)
ax.set_xlabel("Month")
ax.set_ylabel("Count of Users")
ax.legend(title = "Year")
st.pyplot(fig)

#Membuat visualisasi data untuk penyewaan per bulan
st.subheader("Monthly Rentals:")
fig, ax = plt.subplots(figsize = (8, 5))
sns.barplot(
    x = monthly_df.index,
    y = monthly_df["cnt"]
)
ax.set_title("Number of Users by Month", loc = "center", fontsize = 15)
ax.set_xlabel("Month")
ax.set_ylabel("Count of Users")
st.pyplot(fig)

#Membuat visualisasi data untuk penyewaan per hari kerja dan hari libur
st.subheader("Weekday and Holiday Rentals:")
fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (15, 10))
sns.barplot(
    x = workingday_df["workingday"],
    y = workingday_df["cnt"],
    hue = workingday_df["season"],
    ax = ax[0]
)
ax[0].set_title("Number of Users by Working Day and Season", loc = "center", fontsize = 15)
ax[0].set_xlabel("Working Day")
ax[0].set_ylabel("Count of Users")
ax[0].legend(title = "Season")

sns.barplot(
    x = holiday_df["holiday"],
    y = holiday_df["cnt"],
    hue = holiday_df["season"],
    ax = ax[1]
)
ax[1].set_title("Number of Users by Holiday and Season", loc = "center", fontsize = 15)
ax[1].set_xlabel("Holiday")
ax[1].set_ylabel("Count of Users")
ax[1].legend(title = "Season")
st.pyplot(fig)

#Membuat visualisasi data untuk penyewaan per jam
st.subheader("Hour Rentals:")
fig, ax = plt.subplots(figsize = (15, 8))
sns.pointplot(
    x = hour_df["hr"],
    y = hour_df["cnt"],
    hue = hour_df["weekday"]
)
ax.set_title("Number of Users by Hour and Weekday", loc = "center", fontsize = 15)
ax.set_xlabel("Hour")
ax.set_ylabel("Count of Users")
ax.legend(title = "Weekday")
st.pyplot(fig)