#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_csv('data.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.title('Análisis Visual de Ventas de Tienda de Conveniencia')
st.sidebar.header('Filtros')

# Filtro por Sucursal
branches = df['Branch'].unique()
selected_branch = st.sidebar.selectbox('Seleccionar Sucursal', ['Todas'] + list(branches))
if selected_branch != 'Todas':
    df_filtered = df[df['Branch'] == selected_branch]
else:
    df_filtered = df.copy()

# Filtro por Línea de Producto
product_lines = df_filtered['Product line'].unique()
selected_product_line = st.sidebar.selectbox('Seleccionar Línea de Producto', ['Todas'] + list(product_lines))
if selected_product_line != 'Todas':
    df_filtered = df_filtered[df_filtered['Product line'] == selected_product_line]

st.subheader('Evolución de las Ventas Totales')
sales_over_time = df_filtered.groupby('Date')['Total'].sum().reset_index()
fig_sales_time, ax_sales_time = plt.subplots(figsize=(10, 5))
sns.lineplot(x='Date', y='Total', data=sales_over_time, ax=ax_sales_time)
ax_sales_time.set_title('Evolución de las Ventas Totales a lo Largo del Tiempo')
ax_sales_time.set_xlabel('Fecha')
ax_sales_time.set_ylabel('Ventas Totales')
plt.xticks(rotation=45)
st.pyplot(fig_sales_time)

st.subheader('Ingresos por Línea de Producto')
product_line_sales = df_filtered.groupby('Product line')['Total'].sum().sort_values(ascending=False)
fig_product_sales, ax_product_sales = plt.subplots(figsize=(10, 5))
sns.barplot(x=product_line_sales.index, y=product_line_sales.values, ax=ax_product_sales)
ax_product_sales.set_title('Ingresos por Línea de Producto')
ax_product_sales.set_xlabel('Línea de Producto')
ax_product_sales.set_ylabel('Ingresos Totales')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig_product_sales)

st.subheader('Distribución de la Calificación de Clientes')
fig_rating, ax_rating = plt.subplots(figsize=(8, 5))
sns.histplot(df_filtered['Rating'], bins=10, kde=True, ax=ax_rating)
ax_rating.set_title('Distribución de la Calificación de Clientes')
ax_rating.set_xlabel('Calificación')
ax_rating.set_ylabel('Frecuencia')
st.pyplot(fig_rating)

st.subheader('Comparación del Gasto por Tipo de Cliente')
fig_customer_type, ax_customer_type = plt.subplots(figsize=(8, 5))
sns.boxplot(x='Customer type', y='Total', data=df_filtered, ax=ax_customer_type)
ax_customer_type.set_title('Comparación del Gasto por Tipo de Cliente')
ax_customer_type.set_xlabel('Tipo de Cliente')
ax_customer_type.set_ylabel('Gasto Total')
st.pyplot(fig_customer_type)

st.subheader('Relación entre Costo y Ganancia Bruta')
fig_cogs_income, ax_cogs_income = plt.subplots(figsize=(8, 5))
sns.scatterplot(x='cogs', y='gross income', data=df_filtered, ax=ax_cogs_income)
ax_cogs_income.set_title('Relación entre Costo de Bienes Vendidos e Ingreso Bruto')
ax_cogs_income.set_xlabel('Costo de Bienes Vendidos (cogs)')
ax_cogs_income.set_ylabel('Ingreso Bruto (gross income)')
st.pyplot(fig_cogs_income)

st.subheader('Métodos de Pago Preferidos')
payment_counts = df_filtered['Payment'].value_counts()
fig_payment, ax_payment = plt.subplots(figsize=(8, 5))
ax_payment.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=140)
ax_payment.set_title('Métodos de Pago Preferidos')
st.pyplot(fig_payment)

st.subheader('Composición del Ingreso Bruto por Sucursal y Línea de Producto')
branch_product_income = df_filtered.groupby(['Branch', 'Product line'])['gross income'].sum().unstack()
fig_branch_product, ax_branch_product = plt.subplots(figsize=(10, 6))
branch_product_income.plot(kind='bar', stacked=True, ax=ax_branch_product)
ax_branch_product.set_title('Composición del Ingreso Bruto por Sucursal y Línea de Producto')
ax_branch_product.set_xlabel('Sucursal')
ax_branch_product.set_ylabel('Ingreso Bruto')
ax_branch_product.tick_params(axis='x', rotation=0)
ax_branch_product.legend(title='Línea de Producto')
st.pyplot(fig_branch_product)


# In[ ]:




