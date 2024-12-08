import datetime
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import folium as folium
from streamlit_folium import st_folium
from io import StringIO

# Show app title and description.
st.set_page_config(page_title="E-commerce Data Analysis",
                   page_icon=":shopping_bags:")
st.write(
    """
# :shopping_bags: Brazilian E-Commerce Public Dataset by Olist

**Welcome to Hazhiyah Yumni's Data Analysis X Dicoding Indonesia!**
Dashboard that will help you to know business improvement according to the data provided.
"""
)

# Dashboard sidebar
st.title('Dashboard')
add_selectbox = st.sidebar.selectbox(
    'Which Question In Your Mind?',
    ('Sales Trend', 'Top Sales', 'Most Used Payment',
     'Delivery Services', 'Negative Feedback Checker')
)

# Show section to view and edit existing tickets in a table.
st.header("Sales Trend Over Time")
# st.write(f"Data Required: `orders.csv`, `order_items.csv`, `order_payments.csv`, `order_reviews.csv`, `products.csv`, `sellers.csv`, `customers.csv`, `geolocation.csv`")
st.info(
    "As an analyst, We need to know more about sales trends and their total revenue to make the right decisions. Here's our structured data to analyze.")

@st.cache_data
def load_data(url):
    visual_data = pd.read_csv(url)  # �� Download the data
    return visual_data

visual_data = load_data("data/monthly_sales_vis.csv")
st.dataframe(visual_data)

st.info("Here's our preview sales trend data over the year")


# Mengubah data ke format long untuk visualisasi
long_data = visual_data.melt(id_vars='month', 
                              value_vars=['sales_2016', 'sales_2017', 'sales_2018'],
                              var_name='year', 
                              value_name='sales')

# Mengatur bulan sebagai kategori untuk memastikan urutan yang benar
long_data['month'] = pd.Categorical(long_data['month'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Membuat chart garis
chart = alt.Chart(long_data).mark_line(point=True).encode(
    x=alt.X('month:O', title='Bulan', sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
    y=alt.Y('sales:Q', title='Penjualan'),
    color='year:N',
    tooltip=['month', 'year', 'sales']
).properties(
    title='Penjualan Bulanan'
)

# Menampilkan chart di Streamlit
st.altair_chart(chart, use_container_width=True)


st.info("We can choose the data by year sales. Please choose year ")
# Ubah data ke format long untuk visualisasi
long_data = visual_data.melt(id_vars='month', 
                              value_vars=['sales_2016', 'sales_2017', 'sales_2018'],
                              var_name='year', 
                              value_name='sales')

# Dropdown untuk memilih tahun
selected_year = st.selectbox("Pilih Tahun:", [2016, 2017, 2018])

# Ambil kolom penjualan untuk tahun yang dipilih
sales_column = f'sales_{selected_year}'
full_data = visual_data[['month', sales_column]]

# Atur bulan sebagai kategori untuk memastikan urutan yang benar
full_data.loc[:, 'month'] = pd.Categorical(full_data['month'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Tampilkan chart penjualan berdasarkan tahun yang dipilih
st.line_chart(full_data.set_index('month')[sales_column])


# QUESTION 3

st.header('Top 10 Product Revenue')

st.info("Bagaimana dengan produk yang dijual? Produk apa saja yang paling laris dalam beberapa tahun ini? Berikut adalah jenis produk yang paling laris:")

def load_data(url):
    visual_data2 = pd.read_csv(url)  # �� Download the data
    return visual_data2

visual_data2 = load_data("data/top10revenue_vis.csv")

# Streamlit app
st.header('Product Categories and Prices')

# Display the DataFrame
st.dataframe(visual_data2)

st.subheader('Chart of Product Categories by Prices')
st.bar_chart(visual_data2.set_index('product_category_name')['price'])

# QUESTION 3
st.header('Most Used Payment Methods')
st.info("Sekarang kita sudah mengetahui jenis produk yang paling laris, lalu metode pembayaran apa yang paling sering digunakan pengguna untuk bertransaksi?")
def load_data(url):
    visual_data3 = pd.read_csv(url)
    return visual_data3
visual_data3 = load_data("data/payment_counts_vis.csv")

# st.bar_chart(visual_data3.set_index('payment_type')['count'])  # Display the bar chart

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
st.title("E-commerece Delivery Services")
st.info("Peta di bawah ini menggambarkan lokasi pengantaran produk untuk mengetahui kondisi geografis pengguna e-commerce")

@st.cache_data
def load_data(url):
    mapdata = pd.read_csv(url)
    return mapdata
mapdata = load_data("data/delivery_location_vis.csv")

# st.dataframe(mapdata)

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
st.dataframe(visual_data4)

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
st.title('Correlation of Sales and Negative Reviews')
st.info("Meskipun penjualan produk terus berlanjut, pihak pengelola juga perlu mengetahui bagaimana komentar/review negatif produk dapat mempengaruhi penjualan untuk menjaga reputasi e-commerce")

def load_data(url):
    visual_data5 = pd.read_csv(url)
    return visual_data5
visual_data5 = load_data("data/correlation_vis.csv")
# st.dataframe(visual_data5)

fig = px.imshow(visual_data5)
st.plotly_chart(fig)