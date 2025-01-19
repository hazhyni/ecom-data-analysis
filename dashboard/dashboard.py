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
from datetime import datetime, timedelta
from datetime import date
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
        options = ["Dashboard","Sales Trend", "Top Product Revenue", "Top Payment Method", "Delivery Time & Map", "Negative Review on Sales"]
    )

# ------------------------------------------ QUESTION 1------------------------------
if selected == "Dashboard":
   
    def load_data(url):
        daily_sales = pd.read_csv(url) 
        return daily_sales

    daily_sales = load_data("data/daily_sales.csv")

    df = pd.DataFrame(daily_sales)

    
    df["Tanggal"] = pd.to_datetime(df["order_date"])

    start_date = df["Tanggal"].min()
    end_date = df["Tanggal"].max()

    selected_date_range = st.date_input(
        "**Pilih rentang tanggal:**",
        value=(start_date, end_date),
        min_value=start_date,
        max_value=end_date,
        key="date_range"
    )

    # Filter data berdasarkan rentang tanggal
    if isinstance(selected_date_range, tuple):
        start_date_selected = selected_date_range[0]
        end_date_selected = selected_date_range[1]

        # Filter DataFrame berdasarkan rentang tanggal
        filtered_df = df[
            (df["Tanggal"] >= pd.to_datetime(start_date_selected)) &
            (df["Tanggal"] <= pd.to_datetime(end_date_selected))
        ]

        if not filtered_df.empty:
            # Calculate total orders by summing the 'price' column
            total_revenue = filtered_df["price"].sum()
            total_orders = filtered_df["id"].count() 

            col1,col2 = st.columns(2)

            # Display the result with formatting (optional)
            with col1:
                st.header(f"**Total Orders**")
                st.info(f"{total_orders:.0f}")

            with col2:
                st.header(f"**Total Revenue**")
                st.success(f"{total_revenue:,.2f}")
                                    
            st.header(f"**Daily Sales**")
            # Group by date to calculate total sales per day
            daily_sales = filtered_df.groupby("Tanggal")["price"].sum().reset_index()

            fig = px.line(
                daily_sales,
                x="Tanggal",
                y="price",
                title="Sales Visualization",
                labels={"Tanggal": "Date", "price": "Total Sales"},
                markers=True,
            )
            fig.update_layout(title_font_size=16, xaxis_title="Date", yaxis_title="Total Sales")
            st.plotly_chart(fig)
            
            st.header("**Best Worst Performing Products**")
            def load_data(url):
                top_products = pd.read_csv(url) 
                return top_products
            top_products = load_data("data/top_products.csv")

            col1,col2 = st.columns(2)

            unique_top_sales = top_products.groupby('product_category_name')['count'].nunique().reset_index()
            top_10_best_products = unique_top_sales.sort_values(by='count').head(10)

            with col1:
                fig = px.bar(top_10_best_products, x='count', y='product_category_name', title='Best Products')
                fig.update_layout(title_font_size=16, xaxis_title="Total Sales", yaxis_title="Products")
                st.plotly_chart(fig)

            def load_data(url):
                worst_products = pd.read_csv(url) 
                return worst_products
            worst_products = load_data("data/worst_products.csv")

            unique_worst_sales = worst_products.groupby('product_category_name')['count'].nunique().reset_index()
            top_10_worst_products = unique_worst_sales.sort_values(by='count').head(10)

            with col2:
                fig = px.bar(top_10_worst_products, x='count', y='product_category_name', title='Worst Products')
                fig.update_layout(title_font_size=16, xaxis_title="Total Sales", yaxis_title="Products")
                st.plotly_chart(fig)

            st.header("**Customer Demographics**")
            
            def load_data(url):
                custbysales = pd.read_csv(url) 
                return custbysales
            custbysales = load_data("data/customerbysales.csv")
            
            fig = px.bar(custbysales, x='count', y='customer_state', title='Jumlah Pengguna Tiap Daerah')
            fig.update_layout(title_font_size=16, xaxis_title="Jumlah Pelanggan", yaxis_title="Kode Daerah")
            st.plotly_chart(fig)
            
            st.header("**Best Customer Based on RFM Analysis**")
            col1, col2, col3 = st.columns(3)
        
            def load_data(url):
                recency_data = pd.read_csv(url)  # Mengunduh data
                return recency_data
            recency_data = load_data("data/recency_data.csv")

            recency_data['last_order_date'] = pd.to_datetime(recency_data['last_order_date'])
            
            filtered_df = recency_data[
                (recency_data["last_order_date"] >= pd.to_datetime(start_date_selected)) &
                (recency_data["last_order_date"] <= pd.to_datetime(end_date_selected))
            ]
            
            # Menghitung rata-rata recency per hari
            average_total_recency = filtered_df.groupby('last_order_date')['recency'].mean().reset_index()
            total_recency_per_day = average_total_recency['recency'].sum()
            with col1:
                st.subheader("**Recency (Days)**")
                st.info(f"{round(total_recency_per_day):.0f}")

                customer_recency = filtered_df.groupby('customer_id')['recency'].sum().reset_index()
                
                unique_recency = customer_recency.drop_duplicates(subset='recency')
                
                top_5_customers_rec = unique_recency.nlargest(5, 'recency')

                figrec = px.bar(top_5_customers_rec, x='recency', y='customer_id', title='Recency Statistics')
                figrec.update_layout(title_font_size=16, xaxis_title="Recency(Days)", yaxis_title="Customer ID")
                st.plotly_chart(figrec)

            with col2:
                st.subheader("**Frequency**")

                def load_data(url):
                    freq_data = pd.read_csv(url)  # Membaca data dari file CSV
                    return freq_data

                freq_data = load_data("data/frequency_data.csv")

                freq_data['order_purchase_timestamp'] = pd.to_datetime(freq_data['order_purchase_timestamp'], errors='coerce')

                filtered_df = freq_data[
                    (freq_data["order_purchase_timestamp"] >= pd.to_datetime(start_date_selected)) &
                    (freq_data["order_purchase_timestamp"] <= pd.to_datetime(end_date_selected))
                ]

                # Hitung frekuensi transaksi per customer_id
                customer_frequency = filtered_df.groupby('customer_id').size().reset_index(name='frequency')
                total_frequency = customer_frequency['frequency'].sum()
                st.info(f"{round(total_frequency):.0f}")

                # Menghapus duplikat berdasarkan nilai frequency
                unique_frequency = customer_frequency.drop_duplicates(subset='frequency')

                # Ambil 5 pelanggan dengan frekuensi tertinggi
                top_5_customers_freq = unique_frequency.nlargest(10, 'frequency')

                figfreq = px.bar(
                    top_5_customers_freq,
                    x='customer_id',
                    y='frequency',
                    title='Frequency Statistics'
                )
                figfreq.update_layout(
                    title_font_size=16,
                    xaxis_title="Customer ID",
                    yaxis_title="Frequency"
                )
                st.plotly_chart(figfreq)

            with col3:
                st.subheader("**Monetary**")
                def load_data(url):
                    monetary_data = pd.read_csv(url) 
                    return monetary_data
                monetary_data = load_data("data/monetary_daily.csv")

                monetary_data['purchase_date'] = pd.to_datetime(monetary_data['purchase_date'], errors='coerce')

                filtered_df = monetary_data[
                    (monetary_data["purchase_date"] >= pd.to_datetime(start_date_selected)) &
                    (monetary_data["purchase_date"] <= pd.to_datetime(end_date_selected))
                ]

                average_total_monetary = filtered_df.groupby('purchase_date')['total_spent'].mean().reset_index()
                total_monetary_per_day = average_total_monetary['total_spent'].sum()
                st.info(f"{round(total_monetary_per_day):.0f}")
                
                unique_monetary = monetary_data.drop_duplicates(subset='total_spent')
                
                top_5_customers_mon = unique_monetary.nlargest(5, 'total_spent')

                figmon = px.bar(
                    top_5_customers_mon,
                    x='total_spent',
                    y='customer_id',
                    title='Monetary Statistics'
                )
                figmon.update_layout(
                    title_font_size=16,
                    xaxis_title="Monetary",
                    yaxis_title="Customer ID"
                )                
                st.plotly_chart(figmon)
        else:
            st.info("No data available for the selected date range.")
    else:
        st.warning("Pilih rentang tanggal yang valid!")
    
    
    

if selected == "Sales Trend":
    st.title('Q1: Sales Trend Over Time')
    st.divider()
    st.header("***Pertanyaan 1: Bagaimana tren penjualan setiap tahunnya (2016 2017 2018)?***")
    st.write(
    "Kita perlu mengetahui tren penjualan dan total pendapatannya untuk membuat keputusan yang tepat. Maka dari itu, dilakukan analisis berdasarkan dataset yang ada dengan menggabungkan data `orders` untuk mengetahui daftar penjualan dan `order_items` untuk mengetahui history produk yang terjual. Berikut adalah hasil data yang akan kita visualisasikan setelah melalui proses analisis (Gathering, Assessing dan EDA).")

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

    # st.dataframe(visual_data, use_container_width=True)

    st.info("Untuk memudahkan analisis, berikut adalah visualisasi data tren penjualan setiap tahunnya")


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
        title='Tren Penjualan Setiap Tahunnya (2016 2017 2018)'
    )

# Menampilkan chart di Streamlit
    st.altair_chart(chart, use_container_width=True)


    st.info("Berikut adalah visualisasi untuk menampilkan data berdasarkan tahun penjualan")

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
    
    st.header('Hasil analisis grafik')
    if selected_year == 2016:
        st.info("Berdasarkan data penjualan di tahun 2016 hampir tidak ada penjualan yang signifikan dibandingkan dengan tahun lainnya, hal ini menunjukkan bahwa pada tahun ini merupakan tahun awal operasi sehingga aktivitas penjualan masih minim.")
    if selected_year == 2017:
        st.info("Namun pada penjualan 2017 terjadi peningkatan penjualan secara bertahap dari awal hingga akhir tahun, menunjukkan pertumbuhan yang stabil selama tahun tersebut.")
    if selected_year == 2018:
        st.info("Hal ini berlaku juga pada penjualan 2018 yang berada pada tingkat yang tinggi dan stabil hingga bulan September. Namun, terjadi penurunan drastis pada bulan September dan aktivitas hampir berhenti pada kuartal terakhir (Oktober-Desember).")
    st.header("***Summary***")
    st.info("Dengan mengidentifikasi alasan penurunan drastis pada 2018 adalah adanya penurunan pada kuartal terakhir 2018 bisa disebabkan oleh faktor internal atau eksternal seperti penurunan permintaan pasar yang dikarenakan respon negatif pengguna terhadap perusahaan. Namun berdasarkan hasil evaluasi strategi pada tahun 2017 menunjukkan adanya peningkatan yang konsisten sehingga menunjukkan adanya strategi untuk meningkatkan penjualan dapat diterapkan dengan baik. Tren penjualan yang rendah pada 2016 bisa menjadi disebabkan oleh pemahaman atau pembelajaran terhadap tantangan awal penjualan.")
    
    # -------------------------------------- QUESTION 2 ----------------------------------------------------------
    
if selected == "Top Product Revenue":
    st.title('Q2: Top 10 Product Revenue')
    st.divider()
    st.header("***Pertanyaan 2: Jenis produk apa yang memiliki kontribusi terhadap total revenue?***")
    st.write("Setelah mengetahui hasil trend penjualan produk, perlu di analisis juga jenis produk apa yang paling laris dalam beberapa tahun ini yang berperan terhadap peningkatan total revenue seperti yang sudah kita visualisasikan sebelumnya pada Q1.")

    def load_data(url):
        visual_data2 = pd.read_csv(url)  # �� Download the data
        return visual_data2
    
    visual_data2 = load_data("data/top10revenue_vis.csv")

# Display the DataFrame
    visual2_data = visual_data2.loc[:, ['product_category_name', 'price']]

# Mengganti nama kolom
    visual2_data = visual2_data.rename(columns={
        'product_category_name': 'Kategori Produk',
        'price': 'Harga'
    })
# Mengatur ulang indeks dan menambahkan 1
    visual2_data.reset_index(drop=True, inplace=True)
    visual2_data.index += 1  # agar dimulai dari 1
    
    st.subheader('Top 10 Kategori Produk Berdasarkan Total Revenue')
    st.bar_chart(visual_data2.set_index('product_category_name')['price'])
    
    # st.dataframe(visual2_data)
    st.header("Hasil Analisis Grafik")
    st.info("Berdasarkan data kategori produk, terlihat bahwa beleza_saude (Kesehatan dan Kecantikan) menjadi kategori dengan pendapatan tertinggi sebesar Rp1.258.681,34, diikuti oleh relogios_presentes (Jam dan Hadiah) sebesar Rp1.205.005,68, dan cama_mesa_banho (Perlengkapan Rumah Tangga) sebesar Rp1.036.988,68. Ketiga kategori ini mendominasi total pendapatan, menunjukkan permintaan yang tinggi atau harga produk yang relatif mahal. Sementara itu, kategori seperti informatica_acessorios (Aksesoris Komputer) dan esporte_lazer (Olahraga dan Hiburan) berada di posisi menengah dengan pendapatan masing-masing Rp911.954,32 dan Rp988.048,97, yang masih cukup menjanjikan. Namun, kategori seperti ferramentas_jardim (Peralatan Taman) memiliki pendapatan terendah sebesar Rp485.256,46, yang mungkin disebabkan oleh niche market atau rendahnya permintaan.")
    st.header("***Summary***")
    st.info("Dari analisis ini, disarankan untuk memprioritaskan kategori dengan pendapatan tinggi seperti beleza_saude dan relogios_presentes melalui strategi pemasaran yang lebih intensif dan pengelolaan stok barang yang optimal. Selain itu, kategori menengah seperti esporte_lazer dan informatica_acessorios perlu dioptimalkan untuk meningkatkan daya tariknya di pasar. Terakhir, kategori dengan pendapatan rendah seperti ferramentas_jardim dapat dievaluasi lebih lanjut untuk memahami apakah promosi tambahan atau diversifikasi produk dapat meningkatkan penjualannya.")    

# ------------------------------------------QUESTION 3--------------------------------------------------------
if selected == "Top Payment Method":
    st.title('Q3: Most Used Payment Methods')
    st.divider()
    st.header("***Pertanyaan 3: Apa saja jenis metode pembayaran yang paling sering digunakan pengguna dalam bertransaksi?***")
    st.info("Setelah mengetahui jenis produk yang paling laris, dalam transaksi lalu metode pembayaran apa yang paling sering digunakan pengguna untuk bertransaksi?")
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
    st.header("Hasil Analisis Grafik")
    st.info("Berdasarkan diagram mengenai metode pembayaran yang paling sering digunakan, terlihat bahwa kartu kredit mendominasi transaksi dengan porsi sebesar 73,7% atau sejumlah 87.286 transaksi. Metode ini jauh lebih banyak digunakan dibandingkan metode lainnya. Boleto berada di posisi kedua dengan kontribusi sebesar 19,5%, diikuti oleh voucher dengan 5,41%. Sementara itu, metode kartu debit dan kategori lainnya hanya memiliki kontribusi yang sangat kecil, masing-masing sebesar 1,43% dan 0,0025%.")
    st.header("***Summary***")
    st.info("Hasil analisis menunjukkan bahwa pengguna lebih dominan menggunakan kartu kredit atau boleto. Oleh karena itu, sebaiknya memaksimalkan dukungan terhadap transaksi kartu kredit dan boleto, sembari mengevaluasi potensi peningkatan penggunaan metode lain, seperti menawarkan promosi untuk pengguna voucher atau kartu debit.")

# QUESTION 4
if selected == "Delivery Time & Map":
    st.title("Q4: E-commerece Delivery Services")
    st.divider()
    st.header("***Pertanyaan 4: Berapa lama rata - rata waktu pengiriman produk ke pelanggan dan persebaran geografis pengantaran?***")
    st.write("Untuk mengetahui waktu pengiriman produk maka data didapatkan dari tabel `orders` untuk mengetahui daftar pesanan, tabel `order_status` untuk memilih data yang hanya memiliki status *delivered* sehingga hanya produk yang sudah terkirim yang dapat di analisis waktu pengirimannya yang ada pada kolom ")
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
    listdata4.reset_index(drop=True, inplace=True)
    listdata4.index += 1
    st.dataframe(listdata4, use_container_width=True)
    st.write("Peta di bawah ini menggambarkan lokasi pengantaran produk untuk mengetahui kondisi geografis pengguna e-commerce")

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
            popup = f"({row['geolocation_zip_code_prefix']}) {row['customer_state_y']}: {row['avg_delivery_time_days']} hari",
            # popup=f"<b>Area:</b> {row['geolocation_zip_code_prefix']}",
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
