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
    "As a analyst, We need to know more about sales trends and their total revenue to make the right decisions. Here's our clean and structured data to analyze.")

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
