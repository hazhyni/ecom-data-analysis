import datetime
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
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
st.write(f"Data Required: `orders.csv`, `order_items.csv`, `order_payments.csv`, `order_reviews.csv`, `products.csv`, `sellers.csv`, `customers.csv`, `geolocation")
st.info(
    "As an analyst, We need to know more about sales trends and their total revenue to make the right decisions. Here's our clean and structured data to analyze.")

def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df

df = load_data(
    "data/visual1.csv")
st.dataframe(df)
# Generate data
chart_data = pd.DataFrame({
                          "Harga": df["price"],
                          "Tahun": df["order_id"]})
st.line_chart(chart_data, x="Tahun", y="Harga")


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

# Ganti NaN dengan 0 (jika ada)
full_data[sales_column] = full_data[sales_column].fillna(0)

# Atur bulan sebagai kategori untuk memastikan urutan yang benar
full_data['month'] = pd.Categorical(full_data['month'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Tampilkan chart penjualan berdasarkan tahun yang dipilih
st.line_chart(full_data.set_index('month')[sales_column])



# Ubah data ke format long untuk visualisasi
long_data = visual_data.melt(id_vars='month', 
                              value_vars=['sales_2016', 'sales_2017', 'sales_2018'],
                              var_name='year', 
                              value_name='sales')

# Ganti nama tahun untuk kemudahan
long_data['year'] = long_data['year'].str.replace('sales_', '')

# Atur bulan sebagai kategori untuk memastikan urutan yang benar
long_data['month'] = pd.Categorical(long_data['month'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Filter data to start from January
long_data = long_data[long_data['month'].isin(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])]

# Buat chart menggunakan Altair
chart = alt.Chart(long_data).mark_line(point=True).encode(
    x=alt.X('month:O', title='Bulan', sort=alt.SortOrder('ascending')), 
    y=alt.Y('sales:Q', title='Penjualan', scale=alt.Scale(domain=[0, long_data['sales'].max() * 1.1])),
    color='year:N',
    tooltip=['month', 'year', 'sales']
).properties(
    title='Penjualan Bulanan untuk Tahun 2016, 2017, dan 2018'
)

# Tampilkan chart
st.altair_chart(chart, use_container_width=True)