import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración general del dashboard
st.set_page_config(page_title='Dashboard de Ventas', layout='wide')

# 1. Introducción del Caso
st.title('📊 Dashboard de Ventas - Tiendas de Conveniencia')
st.markdown("""
Una cadena de tiendas de conveniencia busca mejorar su estrategia de marketing analizando sus datos de ventas y comportamiento de clientes.

**Objetivo:** Aplicar técnicas de visualización para identificar patrones clave que faciliten la toma de decisiones.

**Datos disponibles:**
- Variables de cliente: `Branch`, `Customer type`, `Gender`, `Payment`
- Variables de producto: `Product line`, `Unit price`, `Quantity`, `Total`, `cogs`, `gross income`
- Evaluación del servicio: `Rating`
- Variables temporales: `Date`, `Time`
""")

# Cargar datos
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

uploaded_file = st.file_uploader("📁 Subí el archivo data.csv", type="csv")

if uploaded_file is not None:
    df = load_data(uploaded_file)
    # mostrar el dashboard si hay archivo
    st.success("✅ Archivo cargado correctamente.")
else:
    st.warning("⚠️ Esperando que subas el archivo CSV.")
    st.stop()

# Sidebar: Filtros
st.sidebar.header('🔍 Filtros')
branches = df['Branch'].unique()
product_lines = df['Product line'].unique()

selected_branch = st.sidebar.selectbox('Sucursal', ['Todas'] + list(branches))
selected_product = st.sidebar.selectbox('Línea de Producto', ['Todas'] + list(product_lines))

# Aplicar filtros
df_filtered = df.copy()
if selected_branch != 'Todas':
    df_filtered = df_filtered[df_filtered['Branch'] == selected_branch]
if selected_product != 'Todas':
    df_filtered = df_filtered[df_filtered['Product line'] == selected_product]

# Tabs por secciones
seccion = st.selectbox("Ir a la sección:", [
    "Visión General",
    "Análisis por Producto",
    "Clientes",
    "Finanzas",
    "Correlación"
])

if seccion == "Visión General":
    st.subheader('📈 Evolución de las Ventas Totales')
    ventas = df_filtered.groupby('Date')['Total'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=ventas, x='Date', y='Total', ax=ax)
    ax.set_title('Ventas Totales a lo Largo del Tiempo')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Total de Ventas')
    st.pyplot(fig)

elif seccion == "Análisis por Producto":
    st.subheader('🧾 Ingresos por Línea de Producto')
    prod_sales = df_filtered.groupby('Product line')['Total'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x=prod_sales.index, y=prod_sales.values, ax=ax)
    ax.set_title('Ingresos por Línea de Producto')
    ax.set_ylabel('Ingreso Total')
    ax.set_xlabel('Línea de Producto')
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif seccion == "Clientes":
    st.subheader('⭐ Distribución de Calificación de Clientes')
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df_filtered['Rating'], bins=10, kde=True, ax=ax)
    ax.set_title('Distribución de Calificaciones')
    ax.set_xlabel('Calificación')
    st.pyplot(fig)

    st.subheader('👤 Comparación de Gasto por Tipo de Cliente')
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.boxplot(x='Customer type', y='Total', data=df_filtered, ax=ax2)
    ax2.set_title('Gasto Total según Tipo de Cliente')
    st.pyplot(fig2)

elif seccion == "Finanzas":
    st.subheader('📊 Relación entre Costo y Ganancia Bruta')
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(x='cogs', y='gross income', data=df_filtered, ax=ax)
    ax.set_title('Costo vs Ingreso Bruto')
    ax.set_xlabel('Costo (cogs)')
    ax.set_ylabel('Ingreso Bruto')
    st.pyplot(fig)

    st.subheader('💳 Métodos de Pago Preferidos')
    payment_counts = df_filtered['Payment'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%')
    ax2.set_title('Distribución de Métodos de Pago')
    st.pyplot(fig2)

    st.subheader('🏬 Ingreso Bruto por Sucursal y Producto')
    pivot = df_filtered.groupby(['Branch', 'Product line'])['gross income'].sum().unstack()
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    pivot.plot(kind='bar', stacked=True, ax=ax3)
    ax3.set_title('Ingreso Bruto por Sucursal y Línea de Producto')
    st.pyplot(fig3)

elif seccion == "Correlación":
    st.subheader('📉 Correlación entre Variables Numéricas')
    corr = df_filtered[["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Mapa de Calor de Correlaciones')
    st.pyplot(fig)

# Reflexión final
st.markdown("""
---
### 🧠 Reflexión Final
Gracias a la visualización interactiva, el negocio puede:
- Identificar líneas de productos más rentables.
- Reconocer patrones de consumo por tipo de cliente.
- Optimizar métodos de pago ofrecidos.
- Ajustar promociones según sucursal o fecha.
""")