import datetime
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import folium as folium
from io import StringIO

# Show app title and description.
st.set_page_config(page_title="E-commerce Data Analysis",
                   page_icon=":shopping_bags:")
st.write(
    """
# :shopping_bags: Brazilian E-Commerce Public Dataset by Olist

**Welcome to Hazhiyah Yumni's Data Analysis X Dicoding Indonesia!**
This App will help you to know business improvement according to the data provided.
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
st.write(f"Data Required: `orders.csv`, `order_items.csv`, `order_payments.csv`, `order_reviews.csv`, `products.csv`, `sellers.csv`, `customers.csv`, `geolocation.csv`")
st.info(
    "As an analyst, We need to know more about sales trends and their total revenue to make the right decisions. Here's our clean and structured data to analyze.")

def load_data(url):
    visual_data = pd.read_csv(url)  # �� Download the data
    return visual_data

visual_data = load_data("data/MONTHLY_SALES_COMBINED.csv")
st.dataframe(visual_data)

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
full_data['month'] = pd.Categorical(full_data['month'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Tampilkan chart penjualan berdasarkan tahun yang dipilih
st.line_chart(full_data.set_index('month')[sales_column])


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


# QUESTTION 3

st.header('Top 10 Product Revenue')

def load_data(url):
    visual_data2 = pd.read_csv(url)  # �� Download the data
    return visual_data2

visual_data2 = load_data("data/top10revenue.csv")

# Streamlit app
st.title('Product Categories and Prices')

# Display the DataFrame
st.write("Here is the data:")
st.dataframe(visual_data2)

st.subheader('Bar Chart of Product Categories and Prices')
st.bar_chart(visual_data2.set_index('product_category_name')['price'])

# QUESTION 3
st.header('Most Used Payment Methods')
def load_data(url):
    visual_data3 = pd.read_csv(url)
    return visual_data3
visual_data3 = load_data("data/payment_counts.csv")

st.bar_chart(visual_data3.set_index('payment_type')['count'])  # Display the bar chart
# data3 = st.dataframe(visual_data3.set_index('payment_type')['count'])

# Buat DataFrame dari data
df = pd.DataFrame(visual_data3)

# Step 2: Buat Chart Pie
fig = px.pie(df, 
             values='count', 
             names='payment_type', 
             title='Distribusi Tipe Pembayaran',
             )  # Menampilkan persentase dan label

# Step 3: Tampilkan Chart di Streamlit
st.title('Distribusi Tipe Pembayaran')
st.plotly_chart(fig)

# QUESTION 4
def load_data(url):
    mapdata = pd.read_csv(url)
    return mapdata
mapdata = load_data("data/geolocation_dataset.csv")
st.dataframe(mapdata)

# st.map(data=mapdata, latitude=mapdata['geolocation_lat'], longitude=mapdata['geolocation_lng'], use_container_width=True)
# DEFAULT MAP STREAMLIT
df = pd.DataFrame(
    mapdata,
    columns=["lat", "lon"],
)
st.map(df)

def load_data(url):
    visual_data4 = pd.read_csv(url)
    return visual_data4
visual_data4 = load_data("data/avg_delivery_time_state.csv")
st.dataframe(visual_data4)


