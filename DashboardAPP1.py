import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#data
data = pd.read_csv("inibenar.csv",sep=";")

#Title
with st.container() :
    st.markdown("<h1 style='color: green; font-size: 100px; text-align: center;'>O-LIST STORE</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: green; font-size: 29px; text-align: center;margin-top: -50px'> THE LARGEST DEPARTMENT STORE IN BRAZILIAN</h2>", unsafe_allow_html=True)
    st.markdown("<div style='width: 730px; height: 100px;text-align: justify'>Olist connects small businesses from all over Brazil to channels without hassle and with a single contract. Those merchants are able to sell their products through the Olist Store and ship them directly to the customers using Olist logistics partners.</div>", unsafe_allow_html=True)


#Pengubahan
datetime_columns = ["order_appr", "order_deli","order_estimated_delivery_date","review_creation_date"]
data.sort_values(by="order_appr", inplace=True)
data.reset_index(inplace=True)
 
for column in datetime_columns:
    data[column] = pd.to_datetime(data[column])
    
    
#Membuat Filter
min_date = data["order_appr"].min()
max_date = data["order_appr"].max()
 
# Mengambil start_date & end_date dari date_input
start_date, end_date = st.date_input(
    label='Rentang Waktu',min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date])

#databantuan
main_data = data[(data["order_appr"] >= str(start_date)) & (data["order_appr"] <= str(end_date))]

#data bantuan
datareview = main_data[['review_id',"review_score","review_creation_date"]]
datageo = main_data[['customer_id','customer_state','seller_id','seller_state']]
datapembelian = data[['payment_type','payment_value']]
datapembelian1 = main_data[['order_id', 'payment_type','payment_value']]


tab1, tab2, tab3 , tab4 = st.tabs(["Total Transactions","Services & Benefit","Merchant & associate","Our Review"])
 
with tab1:
    st.subheader("Seize opportunities for prosperity and growth.")
    st.markdown("<div style='width: 730px; height: 100px;text-align: justify'>Stay informed and empowered as you observe the fluid dynamics of total transactions over time, complemented by a nuanced breakdown of the percentage distribution of transaction amounts, fostering a deeper understanding and facilitating more informed decision-making.</div>", unsafe_allow_html=True)
    
    total = datapembelian1.groupby(by = 'payment_type').order_id.nunique().reset_index()
    fig, ax = plt.subplots(figsize=(15, 6))
    colors = ["#72BCD4","#D3D3D3", "#D3D3D3", "#D3D3D3"]
    barplot = sns.barplot(y='order_id',x='payment_type',data=total,palette = colors,
                     order = ['credit_card','boleto','voucher','debit_card'])
    for p in barplot.patches:
        barplot.annotate(format(p.get_height(), '.0f'), 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha = 'center', va = 'top', 
                     xytext = (0, 9), 
                     textcoords = 'offset points')
        barplot.set_xticklabels(['Kartu Kredit', 'Boleto', 'Voucher','Kartu Debit'])
        plt.title('Metode Pembayaran konsumen tahun 2018')
    plt.ylabel('Jumlah Pembayaran')
    plt.xlabel('Metode Pembayaran')
    plt.show()
    st.pyplot(fig)
    
    x = datapembelian1.groupby(by='payment_type')['payment_value'].sum()
    y = ['Boleto','Kartu Kredit','Kartu Debit','Voucher']
    
    fig, ax = plt.subplots(figsize=(15, 6))
    color = ('#ce7e00','#fff2cc','#ffd966','#bf9000')
    exp = (0.0,0.1,0.0,0.0)
    pie = plt.pie(x, autopct='%1.1f%%',colors=color,explode=exp)
    plt.title('Jumlah Nominal transaksi berdasarkan metode pembayaran')
    plt.legend(pie[0],y,loc="upper left",bbox_to_anchor=(1,1))
    plt.show()
    st.pyplot(fig)
    
 
with tab2:
    st.subheader('Join for exclusive Benefit')
    st.markdown("<div style='width: 730px; height: 100px;text-align: justify'>Experience the convenience and flexibility of our platform with our diverse range of four payment methods, ensuring you can choose the option that best suits your preferences and needs, making your transactions effortless and seamless.</div>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(15, 6))
    x = datapembelian.groupby(by='payment_type')['payment_value'].sum()
    y = ['Boleto','Kartu Kredit','Kartu Debit','Voucher']
    color = ('#ce7e00','#fff2cc','#ffd966','#bf9000')
    exp = (0.0,0.1,0.0,0.0)
    pie = plt.pie(x,colors=color,explode=exp)
    plt.legend(pie[0],y,loc="upper left",bbox_to_anchor=(1,1))
    plt.show()
    st.pyplot(fig)
    
    st.markdown("<div style='width: 730px; height: 100px;text-align: justify'>At the heart of our mission is a commitment to prioritize the satisfaction of our customers, treating each member of our community like family and endeavoring to create an environment where everyone feels valued, supported, and appreciated.</div>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(15, 10))
    
    total = data.groupby(by = 'review_score').order_id.nunique().reset_index()
    colors = ["#d9ead3","#b6d7a8", "#93c47d", "#6aa84f","#27c50f"]
    barplot = sns.barplot(y='order_id',x='review_score',data=total,palette=colors)

    plt.title('Review Score pelanggan')
    plt.ylabel('Jumlah pelanggan')
    plt.xlabel('Review score')
    plt.show()
    st.pyplot(fig)
    
    
with tab3:
    st.subheader("Join our large community today!")
    st.markdown("<div style='width: 730px; height: 100px;text-align: justify'>Welcome to our expansive community, which boasts members hailing from hundreds of cities and spanning across dozens of states. Whether you're seeking advice, support, or simply a friendly conversation, our diverse and vibrant community is here to lend a helping hand and ensure your needs are met. With such a wide range of backgrounds and experiences, you'll find a wealth of knowledge and assistance available at your fingertips. Join us today and become part of our dynamic network of individuals dedicated to mutual support and growth.</div>", unsafe_allow_html=True)
    
    data_geoseller = datageo.groupby(['seller_state']).agg({'seller_id': 'nunique'}).reset_index()
    datageografi_sorted = data_geoseller.sort_values(by='seller_id', ascending=False)
    datageografi_sorted = datageografi_sorted[:10]
   
    fig, ax = plt.subplots(figsize=(15, 6))
    bars = plt.bar(data=datageografi_sorted, x='seller_state', height='seller_id', width=0.5)
    
    plt.title('Jumlah Seller Pada rentang waktu {} dan {}'.format(start_date,end_date))
    plt.ylabel('Jumlah seller')
    plt.xlabel('State seller')
    plt.show()
    
    st.pyplot(fig)
    st.markdown("<div style='width: 730px; height: 100px;text-align: justify'>Join our extensive community of buyers, where individuals from hundreds of cities and spanning across dozens of states converge to offer support and guidance tailored to your shopping needs. Whether you're seeking recommendations, advice on products, or simply a platform to share your experiences, our diverse community is here to assist you every step of the way. With members representing various backgrounds and preferences, you'll find a wealth of insights and assistance to enhance your shopping journey. Join us today and connect with fellow buyers committed to enriching your shopping experience</div>", unsafe_allow_html=True)
    
    data_geocus = datageo.groupby(['customer_state']).agg({'customer_id': 'nunique'}).reset_index()
    datageografi_sorted1 = data_geocus.sort_values(by='customer_id', ascending=False)
    datageografi_sorted1 = datageografi_sorted1[:10]

    fig, ax = plt.subplots(figsize=(15, 6))
    bars = plt.bar(data=datageografi_sorted1,x='customer_state',height='customer_id',width = 0.5)

    plt.title('Jumlah Konsumen Pada rentang waktu {} dan {}'.format(start_date,end_date))
    plt.ylabel('Jumlah Konsumen')
    plt.xlabel('State konsumen')
    plt.show()   
    st.pyplot(fig)
    
    
with tab4:
    st.subheader("Review from our's customer make us improve better")
    st.markdown("<div style='width: 730px; height: 100px;text-align: justify'>We greatly appreciate your contribution in providing very beneficial reviews for us. Through the reviews you provide, we can continually improve our services to better meet your needs. With the evaluation system we implement, you can see the level of satisfaction in real-time, ensuring that your experience with us is always maintained at an optimal level. We are committed to continuously improving ourselves to provide even better services, and your reviews are one of the main pillars in this improvement process.</div>", unsafe_allow_html=True)
    
    fig,ax=plt.subplots(figsize=(15, 6))

    total = datareview.groupby(by = 'review_score').review_id.nunique().reset_index()
    colors = ["#d9ead3","#b6d7a8", "#93c47d", "#6aa84f","#27c50f"]
    barplot = sns.barplot(y='review_id',x='review_score',data=total,palette=colors)
    
    for p in barplot.patches:
        barplot.annotate(format(p.get_height(), '.0f'), 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha = 'center', va = 'top', 
                     xytext = (0, 9), 
                     textcoords = 'offset points')
    
    plt.title('Review Score pelanggan')
    plt.ylabel('Jumlah Review')
    plt.xlabel('Review score')
    plt.show()

    st.pyplot(fig)