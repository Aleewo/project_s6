import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')

st.header('Dashboard de Anuncios de Venta de Coches')

if st.button('Construir Histograma de Odómetro'):
    fig = px.histogram(df, x='odometer', title='Histograma de Odómetro')
    st.plotly_chart(fig, use_container_width=True)

if st.button('Gráfico de Dispersión Precio vs. Año'):
    fig = px.scatter(df, x='price', y='model_year', title='Precio vs. Año del Modelo')
    st.plotly_chart(fig, use_container_width=True)
