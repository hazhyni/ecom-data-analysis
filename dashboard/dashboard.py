import datetime
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import folium as folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from io import StringIO


# Show app title and description.
st.set_page_config(page_title="E-commerce Data Analysis",
                   page_icon=":shopping_bags:")
st.write(
    """
# :shopping_bags: Brazilian E-Commerce Public Dataset by Olist

**Welcome to Hazhiyah Yumni's Data Analysis X Dicoding Indonesia!**
Informational dashboard that will help you to know business improvement according to the data provided. 😉
"""
)

# Dashboard sidebar
with st.sidebar:
    selected = option_menu(
        menu_title = "Dashboard",
        options = ["Sales Trend", "Top Product Revenue", "Top Payment Method", "Delivery Time & Map", "Negative Review on Sales"]
    )

# ------------------------------------------ QUESTION 1------------------------------
if selected == "Sales Trend":
    st.title('Q1: Sales Trend Over Time')
    st.write("Pertanyaan 1: Bagaimana tren penjualan tiap tahunnya?")
    st.info(
    "As an analyst, We need to know more about sales trends and their total revenue to make the right decisions. Here's our structured data to analyze.")

    @st.cache_data
    def load_data(url):
        visual_data = pd.read_csv(url)  # �� Download the data
        return visual_data

    visual_data = load_data("data/monthly_sales_vis.csv")

    visual_data = visual_data.rename(columns={
        'month': 'Bulan',
        'sales_2016': '2016',
        'sales_2017': '2017',
        'sales_2018': '2018',
    })

# Mengatur ulang indeks dan menambahkan 1
    visual_data.reset_index(drop=True, inplace=True)
    visual_data.index += 1  # Menambahkan 1 ke setiap indeks

    st.dataframe(visual_data, use_container_width=True)

    st.info("Here's our preview sales trend data over the year")


# Mengubah data ke format long untuk visualisasi
    long_data = visual_data.melt(id_vars='Bulan', 
                              value_vars=['2016', '2017', '2018'],
                              var_name='year', 
                              value_name='sales')

# Mengatur bulan sebagai kategori untuk memastikan urutan yang benar
    long_data['Bulan'] = pd.Categorical(long_data['Bulan'], categories=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Membuat chart garis
    chart = alt.Chart(long_data).mark_line(point=True).encode(
        x=alt.X('Bulan:O', title='Bulan', sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
        y=alt.Y('sales:Q', title='Penjualan'),
        color='year:N',
        tooltip=['Bulan', 'year', 'sales']
    ).properties(
        title='Penjualan Bulanan'
    )

# Menampilkan chart di Streamlit
    st.altair_chart(chart, use_container_width=True)


    st.info("We can choose the data by year sales. Please choose year")

# Ubah data ke format long untuk visualisasi (opsional)
    long_data = visual_data.melt(id_vars='Bulan', 
                              value_vars=['2016', '2017', '2018'],
                              var_name='year', 
                              value_name='sales')

# Dropdown untuk memilih tahun
    selected_year = st.selectbox("Pilih Tahun:", [2016, 2017, 2018])

# Ambil kolom penjualan untuk tahun yang dipilih
    sales_column = str(selected_year)  # Pastikan ini string
    full_data = visual_data.loc[:, ['Bulan', sales_column]]  # Seleksi kolom menggunakan :loc

# Atur bulan sebagai kategori untuk memastikan urutan yang benar
    bulan_kategori = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    full_data['Bulan'] = pd.Categorical(full_data['Bulan'], categories=bulan_kategori, ordered=True)

# Mengurutkan data berdasarkan bulan
    full_data = full_data.sort_values('Bulan')

# Set 'Bulan' sebagai indeks
    full_data.set_index('Bulan', inplace=True)

# Tampilkan chart penjualan berdasarkan tahun yang dipilih
    st.line_chart(full_data.loc[:, sales_column])

# -------------------------------------- QUESTION 2 ----------------------------------------------------------
if selected == "Top Product Revenue":
    st.title('Q2: Top 10 Product Revenue')
    st.write("Apa saja jenis produk yang paling banyak terjual?")
    st.info("Bagaimana dengan produk yang dijual? Produk apa saja yang paling laris dalam beberapa tahun ini? Berikut adalah jenis produk yang paling laris:")

    def load_data(url):
        visual_data2 = pd.read_csv(url)  # �� Download the data
        return visual_data2
    
    visual_data2 = load_data("data/top10revenue_vis.csv")

# Streamlit app
    st.header('Product Categories and Prices')

# Display the DataFrame
    visual2_data = visual_data2.loc[:, ['product_category_name', 'price']]

# Mengganti nama kolom
    visual2_data = visual2_data.rename(columns={
        'product_category_name': 'Kategori Produk',
        'price': 'Harga'
    })
# Mengatur ulang indeks dan menambahkan 1
    visual2_data.reset_index(drop=True, inplace=True)
    visual2_data.index += 1  # Menambahkan 1 ke setiap indeks
    st.dataframe(visual2_data)

    st.subheader('Chart of Product Categories by Prices')
    st.bar_chart(visual_data2.set_index('product_category_name')['price'])

# ------------------------------------------QUESTION 3--------------------------------------------------------
if selected == "Top Payment Method":
    st.title('Q3: Most Used Payment Methods')
    st.write("Apa saja jenis metode pembayaran yang paling sering digunakan pengguna dalam bertransaksi?")
    st.info("Sekarang kita sudah mengetahui jenis produk yang paling laris, lalu metode pembayaran apa yang paling sering digunakan pengguna untuk bertransaksi?")
    def load_data(url):
        visual_data3 = pd.read_csv(url)
        return visual_data3
    visual_data3 = load_data("data/payment_counts_vis.csv")
    
# Buat DataFrame dari data
    df = pd.DataFrame(visual_data3)

# Step 2: Buat Chart Pie
    fig = px.pie(df, 
             values='count', 
             names='payment_type', 
             title='Distribusi Tipe Pembayaran',
             )  # Menampilkan persentase dan label

# Step 3: Tampilkan Chart di Streamlit
    st.plotly_chart(fig)



# QUESTION 4
if selected == "Delivery Time & Map":
    st.title("Q4: E-commerece Delivery Services")
    st.write("Berapa lama rata - rata waktu pengiriman produk ke pelanggan dan di provinsi mana saja produk dijualkan?")
    st.info("Peta di bawah ini menggambarkan lokasi pengantaran produk untuk mengetahui kondisi geografis pengguna e-commerce")
    
    @st.cache_data
    def load_data(url):
        listdata4 = pd.read_csv(url)
        return listdata4
    listdata4 = load_data('data/delivery_time_result.csv')
    listdata4 = listdata4.loc[:, ['customer_zip_code_prefix','customer_state_x', 'customer_city', 'avg_delivery_time_days']]
    listdata4 = listdata4.rename(columns={
        'customer_zip_code_prefix': 'ZIP Code',
        'customer_state_x': 'State Code',
        'customer_city': 'City Name',
        'avg_delivery_time_days': 'Waktu Pengiriman (hari)'
    })
    st.dataframe(listdata4, use_container_width=True)
    
    def load_data(url):
        mapdata = pd.read_csv(url)
        return mapdata
    mapdata = load_data("data/delivery_location_vis.csv")

# DEFAULT MAP STREAMLIT
    df = pd.DataFrame(
        mapdata,
        columns=["latitude", "longitude"],
    )
    st.map(df)

# FOLIUM MAP STREAMLIT
    def load_data(url):
        visual_data4 = pd.read_csv(url)
        return visual_data4
    visual_data4 = load_data("data/delivery_location_vis.csv")
# st.dataframe(visual_data4)

    map_center = [-11.129510435529394, -51.71638421174256]
    map_folium = folium.Map(location=map_center, zoom_start=5)
# Menambahkan marker ke peta
    for index, row in visual_data4 .iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"<b>Area:</b> {row['geolocation_zip_code_prefix']}",
            icon=folium.Icon(icon="location-dot", color="blue")  # Using a default icon
        ).add_to(map_folium)

# Menampilkan peta di Streamlit
    st.title("Peta Lokasi Delivery Pelanggan")
    st_data = st_folium(map_folium, width=725)


# QUESTION 05
if selected == "Negative Review on Sales":
    st.title('Q5: Correlation of Sales and Negative Reviews')
    st.write("Apakah terdapat korelasi antara respon negatif pengguna terhadap penjualan produk?")
    st.info("Meskipun penjualan produk terus berlanjut, pihak pengelola juga perlu mengetahui bagaimana komentar/review negatif produk dapat mempengaruhi penjualan untuk menjaga reputasi e-commerce")

    def load_data(url):
        visual_data5 = pd.read_csv(url)
        return visual_data5
    visual_data5 = load_data("data/correlation_vis.csv")
    st.dataframe(visual_data5)

    fig = px.imshow(visual_data5)
    st.plotly_chart(fig)
