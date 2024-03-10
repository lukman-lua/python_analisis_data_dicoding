import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams.update({
    'text.color': "white",
    'axes.labelcolor': "white",
    'axes.grid': True
})

# Load cleaned data
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")


def question_one(agg):
    use_agg = {}
    asc_by = ""
    if agg:
        for user in agg:
            if user == "Casual":
                use_agg['casual'] = "sum"
                if asc_by == "":
                    asc_by = "casual"
            elif user == "Registered":
                use_agg['registered'] = "sum"
                if asc_by != "cnt":
                    asc_by = "registered"
            elif user == "Cnt":
                use_agg['cnt'] = "sum"
                asc_by = "cnt"
    else:
        use_agg = {
            "casual": "sum",
            "registered": "sum",
            "cnt": "sum"
        }
        asc_by = 'cnt'
    grouped_day_df = day_df.groupby(by="season").agg(use_agg).sort_values(by=asc_by, ascending=True)
    grouped_day_df.reset_index(inplace=True)
    grouped_day_df['season'].replace({1: 'springer', 2: 'summer', 3: 'fall', 4: 'winter'}, inplace=True)

    x_axis = np.arange(len(grouped_day_df['season']))
    width = 0.3
    y_range = 200000
    y_max = 0

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    if agg:
        if len(agg) == 1:
            width = 0
            if agg[0] == "Casual":
                y_range = 50000
                width = 1
        for user in agg:
            if user == "Casual":
                ax.bar(x_axis - width, grouped_day_df['casual'], width=0.3, label="Casual")
                if y_max == 0:
                    y_max = (max(grouped_day_df['casual']) // y_range + 1) * y_range
            elif user == "Registered":
                ax.bar(x_axis, grouped_day_df['registered'], width=0.3, label="Registered")
                if y_max < (max(grouped_day_df['registered']) // y_range + 1) * y_range:
                    y_max = (max(grouped_day_df['registered']) // y_range + 1) * y_range
            elif user == "Cnt":
                ax.bar(x_axis + width, grouped_day_df['cnt'], width=0.3, label="CNT")
                y_max = (max(grouped_day_df['cnt']) // y_range + 1) * y_range
    else:
        y_max = (max(grouped_day_df['cnt']) // y_range + 1) * y_range

        ax.bar(x_axis - width, grouped_day_df['casual'], width=width, label="Casual")
        ax.bar(x_axis, grouped_day_df['registered'], width=width, label="Registered")
        ax.bar(x_axis + width, grouped_day_df['cnt'], width=width, label="CNT")

    ax.set_xticks(x_axis)  # Correct usage of set_xticks
    ax.set_xticklabels(grouped_day_df['season'])  # Set x-axis tick labels
    ax.set_xlabel('Musim')  # Correct usage of set_xlabel
    ax.set_ylabel('Jumlah')
    ax.set_yticks(np.arange(0, y_max, y_range))  # Correct usage of set_yticks
    ax.set_yticklabels(
        ['{} K'.format(int(y_val / 1000)) for y_val in np.arange(0, y_max, y_range)]
    )  # Set y-axis tick labels
    ax.tick_params(rotation=0)  # Rotate x-axis tick labels
    ax.legend()

    st.pyplot(fig)


def question_twou():
    ask_2_df = day_df.groupby(by="weathersit").agg({
        "cnt": "sum"
    }).sort_values(by="cnt", ascending=True)
    ask_2_df.reset_index(inplace=True)
    ask_2_df['weathersit'] = ask_2_df['weathersit'].astype(str)

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    y_range = 500000
    y_max = (max(ask_2_df['cnt']) // y_range + 1) * y_range

    ax.bar(ask_2_df['weathersit'], ask_2_df['cnt'], color="green")
    ax.set_xlabel('Cuaca')
    ax.set_ylabel('Jumlah')
    ax.tick_params(rotation=0)  # Rotate x-axis labels for better readability
    ax.set_yticks(
        np.arange(
            0,
            y_max,
            y_range
        ),
        ['{} K'.format(int(y_val / 1000)) for y_val in np.arange(0, y_max, y_range)]
    )

    st.pyplot(fig)


def question_three():
    working_hour_df = hour_df[hour_df['workingday'] == 1].groupby(by=["hr"]).agg({
        "casual": ["max", 'mean', "sum"],
    }).sort_values(by=("casual", "sum"), ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    ax.bar(working_hour_df.index.values, working_hour_df['casual']['sum'], color='orange')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah')
    ax.set_xticks(working_hour_df.index.values)
    ax.set_xticklabels(working_hour_df.index.values)
    st.pyplot(fig)


def question_four():
    year_day_df = day_df.groupby(by=["yr", "mnth"]).agg({
        "cnt": "sum",
    })

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    ax.plot(year_day_df.loc[0]['cnt'].index.values, year_day_df.loc[0]["cnt"], color='orange', label="2011")
    ax.plot(year_day_df.loc[1]['cnt'].index.values, year_day_df.loc[1]["cnt"], color='blue', label="2012")
    ax.set_xlabel('Bulan', size=12)
    ax.set_ylabel('Total Pengunjung', size=12)

    ax.set_xticks(year_day_df.loc[1]['cnt'].index.values)
    ax.set_xticklabels(year_day_df.loc[1]['cnt'].index.values)

    ax.legend()

    st.pyplot(fig)

def pie_four():
    # Membuat Visualisasi Pie Chart untuk Membandingkan Jumlah Pengguna Bike Sharing Tahun 2011 dan 2012
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    ax.pie(
        [day_df[day_df['yr'] == 1].cnt.sum(), day_df[day_df['yr'] == 0].cnt.sum()],
        labels=[2012, 2011],
        shadow=True,
        autopct='%1.1f%%',
        wedgeprops={
            "edgecolor": "white",
            'linewidth': 1,
            'antialiased': True
        }
    )

    st.pyplot(fig)


# Set page title
st.title("Proyek Analisis Data: Bike Sharing Dataset")

# Sidebar
with st.sidebar:
    st.markdown(
        """
       - **Nama:** Lukman Mul Hakim
       - **Email:** serlifa@gmail.com / m184d4ky3143@bangkit.academy
       - **ID Dicoding:** serlifa@gmail.com
        """
    )

    st.header('Bike Sharing Dataset')
    st.markdown("""
    Hadi Fanaee-T

    Laboratory of Artificial Intelligence and Decision Support (LIAAD), University of Porto
    INESC Porto, Campus da FEUP
    Rua Dr. Roberto Frias, 378
    4200 - 465 Porto, Portugal
    """)

    st.header('Bike Sharing Dataset')

    st.markdown("""
       - hour.csv : bike sharing counts aggregated on hourly basis. Records: 17379 hours
       - day.csv - bike sharing counts aggregated on daily basis. Records: 731 days
        """)

st.markdown("""
Bisnis Goals
- Bagaimana perubahan pola perilaku peminjaman Bike Sharing untuk setiap musim ?
- Keadaan cuaca yang bagaimana meningkatkan pengguna Bike Sharing ?
- Pada jam berapa pengguna biasa (casual) meningkat pada hari kerja ?
- Bagaimana peforma peminjaman Bike sharing 2012 jika dibangdingkan dengan 2011 ?
""")

tab1, tab2, tab3, tab4 = st.tabs(["Goals 1", "Goals 2", "Goals 3", "Goals 4"])

with tab1:
    # Pertanyaan Bisnis 1
    st.subheader('Perubahan Pola Perilaku Peminjaman Bike Sharing berdasarkan Musim')
    st.markdown("""
    - Casual: jumlah pengguna kasual
    - Registered: jumlah pengguna terdaftar
    - Cnt: jumlah total sepeda yang disewakan termasuk yang kasual dan terdaftar
    """)
    user_qone = st.multiselect(
        label="Lihat per user :",
        options=('Casual', 'Registered', 'Cnt')
    )
    question_one(user_qone)

with tab2:
    # Pertanyaan Bisnis 2
    st.subheader('Keadaan Cuaca yang meningkatkan Pengguna Bike Sharing')
    st.markdown("""
    - 1: Cerah, Sedikit awan, Sebagian berawan, Sebagian berawan
    - 2: Kabut + Mendung, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
    - 3: Salju Ringan, Hujan Ringan + Badai Petir + Awan berserakan, Hujan Ringan + Awan berserakan
    """)
    question_twou()

with tab3:
    # Pertanyaan Bisnis 3
    st.subheader('Pengguna Hari Kerja berdasarkan Jam')
    question_three()

with tab4:
    # Pertanyaan Bisnis 4
    st.subheader('Pengguna Bike Sharing berdasarkan Tahun')
    genre = st.selectbox(
        label="Mode",
        options=('Line Chart', 'Pie Chart'),
    )
    if genre == "Line Chart":
        question_four()
    else:
        pie_four()

