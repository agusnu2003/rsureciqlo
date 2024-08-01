import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# CSS personalizado para colores verdes
st.set_page_config(page_title="Análisis de Datos Verdes", page_icon=":chart_with_upwards_trend:")
st.markdown("""
    <style>
    .main {
        background-color: #e8f5e9; /* Fondo verde claro */
        color: #1b5e20; /* Texto verde oscuro */
    }
    .stButton>button {
        background-color: #2e7d32; /* Botón verde */
        color: white;
    }
    .stDownloadButton>button {
        background-color: #2e7d32; /* Botón de descarga verde */
        color: white;
    }
    .stTextInput>div>input {
        background-color: #c8e6c9; /* Campo de texto verde claro */
        color: #1b5e20;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar datos CSV
uploaded_file = st.file_uploader('Sube tu archivo CSV', type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convertir 'Fecha de escaneo o entrega' a datetime con infer_datetime_format
    try:
        df['Fecha de escaneo o entrega'] = pd.to_datetime(df['Fecha de escaneo o entrega'], infer_datetime_format=True)
    except ValueError:
        df['Fecha de escaneo o entrega'] = pd.to_datetime(df['Fecha de escaneo o entrega'], format='%m/%d/%Y', errors='coerce')
        df['Fecha de escaneo o entrega'].fillna(pd.to_datetime(df['Fecha de escaneo o entrega'], format='%d/%m/%Y', errors='coerce'), inplace=True)

    df.dropna(subset=['Fecha de escaneo o entrega'], inplace=True)

    df['Día de la semana'] = df['Fecha de escaneo o entrega'].dt.day_name()

    cantidad_por_dia = df.groupby('Día de la semana')['Cantidad'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(x=cantidad_por_dia.index, y=cantidad_por_dia.values, palette='Greens')
    plt.title('Cantidad por Día de la Semana')
    plt.xlabel('Día de la Semana')
    plt.ylabel('Cantidad')
    st.pyplot(plt)

    # Convertir 'Fecha de escaneo o entrega' a datetime con el formato correcto
    df['Fecha de escaneo o entrega'] = pd.to_datetime(df['Fecha de escaneo o entrega'], format='%m/%d/%Y', errors='coerce')
    df.dropna(subset=['Fecha de escaneo o entrega'], inplace=True)
    df['Año'] = df['Fecha de escaneo o entrega'].dt.year
    df['Mes'] = df['Fecha de escaneo o entrega'].dt.month

    df_filtered = df[df['Año'].isin([2023, 2024])]
    cantidad_por_mes_anio = df_filtered.groupby(['Año', 'Mes'])['Cantidad'].sum().unstack(fill_value=0)

    plt.figure(figsize=(12, 6))
    plt.bar(cantidad_por_mes_anio.columns, cantidad_por_mes_anio.loc[2023], color='#66bb6a')
    plt.title('Cantidad por Mes en 2023')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad')
    plt.xticks(ticks=range(1, 13), labels=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    plt.figure(figsize=(12, 6))
    plt.bar(cantidad_por_mes_anio.columns, cantidad_por_mes_anio.loc[2024], color='#388e3c')
    plt.title('Cantidad por Mes en 2024')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad')
    plt.xticks(ticks=range(1, 13), labels=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

 st.subheader('Top 11 de los que más recolectaron')
    top_11 = df.groupby('Recolector')['Cantidad'].sum().nlargest(11).reset_index()
    st.write(top_11)

    # Gráfico de top 11 recolectores
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Cantidad', y='Recolector', data=top_11, palette='Greens')
    plt.title('Top 11 de los que más recolectaron')
    plt.xlabel('Cantidad')
    plt.ylabel('Recolector')
    st.pyplot(plt)
