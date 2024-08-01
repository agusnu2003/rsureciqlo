import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Configuración de la interfaz de Streamlit
st.title('Análisis de Cantidades por Día de la Semana, Mes y Año')

archivo_csv = st.file_uploader('Sube el archivo CSV', type=['csv'])

if archivo_csv:
    try:
        # Cargar el archivo CSV
        df = pd.read_csv(archivo_csv)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

    # Convertir 'Fecha de escaneo o entrega' a datetime con infer_datetime_format
    try:
        df['Fecha de escaneo o entrega'] = pd.to_datetime(df['Fecha de escaneo o entrega'], infer_datetime_format=True)
    except ValueError:
        # Manejar manualmente ambos formatos de fecha
        df['Fecha de escaneo o entrega'] = pd.to_datetime(df['Fecha de escaneo o entrega'], format='%m/%d/%Y', errors='coerce')
        df['Fecha de escaneo o entrega'].fillna(pd.to_datetime(df['Fecha de escaneo o entrega'], format='%d/%m/%Y', errors='coerce'), inplace=True)

    # Eliminar filas con fechas no válidas
    df.dropna(subset=['Fecha de escaneo o entrega'], inplace=True)

    # Agregar una columna para el día de la semana
    df['Día de la semana'] = df['Fecha de escaneo o entrega'].dt.day_name()

    # Agrupar por el día de la semana y sumar la 'Cantidad'
    cantidad_por_dia = df.groupby('Día de la semana')['Cantidad'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    # Crear la visualización para el día de la semana
    plt.figure(figsize=(12, 6))
    sns.barplot(x=cantidad_por_dia.index, y=cantidad_por_dia.values)
    plt.title('Cantidad por Día de la Semana')
    plt.xlabel('Día de la Semana')
    plt.ylabel('Cantidad')
    st.pyplot(plt)
    
    # Mostrar la tabla de resultados en Streamlit
    st.write("Cantidad por Día de la Semana:")
    st.write(cantidad_por_dia)

    # Convertir 'Fecha de escaneo o entrega' a datetime con el formato correcto
    df['Fecha de escaneo o entrega'] = pd.to_datetime(df['Fecha de escaneo o entrega'], format='%m/%d/%Y', errors='coerce')

    # Eliminar filas con fechas no válidas
    df.dropna(subset=['Fecha de escaneo o entrega'], inplace=True)

    # Agregar columnas para el año y el mes
    df['Año'] = df['Fecha de escaneo o entrega'].dt.year
    df['Mes'] = df['Fecha de escaneo o entrega'].dt.month

    # Filtrar para los años 2023 y 2024
    df_filtered = df[df['Año'].isin([2023, 2024])]

    # Agrupar por año y mes, y sumar la 'Cantidad'
    cantidad_por_mes_anio = df_filtered.groupby(['Año', 'Mes'])['Cantidad'].sum().unstack(fill_value=0)

    # Mostrar los resultados en Streamlit
    st.write("\nCantidad por Mes en 2023 y 2024:")
    st.write(cantidad_por_mes_anio)

    # Crear la visualización para 2023
    plt.figure(figsize=(12, 6))
    plt.bar(cantidad_por_mes_anio.columns, cantidad_por_mes_anio.loc[2023], color='skyblue')
    plt.title('Cantidad por Mes en 2023')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad')
    plt.xticks(ticks=range(1, 13), labels=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], rotation=45)
    plt.tight_layout()  # Ajustar el diseño para evitar recortes
    st.pyplot(plt)

    # Crear la visualización para 2024
    plt.figure(figsize=(12, 6))
    plt.bar(cantidad_por_mes_anio.columns, cantidad_por_mes_anio.loc[2024], color='lightgreen')
    plt.title('Cantidad por Mes en 2024')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad')
    plt.xticks(ticks=range(1, 13), labels=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], rotation=45)
    plt.tight_layout()  # Ajustar el diseño para evitar recortes
    st.pyplot(plt)
