import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')

# Limpiar los datos
df = df.drop_duplicates()
df = df.dropna()
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# Extraer el fabricante del modelo
df['manufacturer'] = df['model'].str.split(' ').str[0]

st.header('Data Viewer')

include_small_manufacturers = st.checkbox('Include manufacturers with less than 1000 ads')

if not include_small_manufacturers:
    manufacturer_counts = df['manufacturer'].value_counts()
    df = df[df['manufacturer'].isin(manufacturer_counts[manufacturer_counts >= 1000].index)]
    
st.dataframe(df)

# Agrupar los datos por fabricante y tipo de vehículo, luego contar
df_grouped = df.groupby(['manufacturer', 'type']).size().reset_index(name='count')

# Gráfico de tipos de vehículos por fabricante
st.header('Vehicle Types by Manufacturer')

fig = px.bar(df_grouped, 
             x='manufacturer', 
             y='count', 
             color='type', 
             title='Vehicle Types by Manufacturer',
             width=1200,  # Ajustar ancho para mostrar más fabricantes
             height=600)

# Ajustar el layout y los ejes
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.update_xaxes(tickangle=90)  # Mostrar nombres de fabricantes verticalmente

st.plotly_chart(fig, use_container_width=True)

# histograma de condition vs model year
st.header('Histogram of Condition vs Model Year')

fig = px.histogram(df, x='model_year', color='condition', title='Histogram of Condition vs Model Year', nbins=20)
st.plotly_chart(fig, use_container_width=True)

# comparar la distribucion de precios entre fabricantes
st.header('Compare Price Distribution Between Manufacturers')

manufacturer1 = st.selectbox('Select manufacturer 1', df['manufacturer'].unique())
manufacturer2 = st.selectbox('Select manufacturer 2', df['manufacturer'].unique())

normalize_histogram = st.checkbox('Normalize histogram')

df_filtered = df[df['manufacturer'].isin([manufacturer1, manufacturer2])]

fig = px.histogram(df_filtered,
                   x='price',
                   color='manufacturer',
                   title=f'Price Distribution: {manufacturer1} vs {manufacturer2}',
                   barmode='overlay' if normalize_histogram else 'group',
                   histnorm='percent' if normalize_histogram else None)

st.plotly_chart(fig, use_container_width=True)