import re
import csv
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from io import StringIO

# Configuración de Streamlit para hacer el contenido de la derecha ancho completo
st.set_page_config(layout="wide")

# Función para procesar las URLs
def process_urls(urls):
    regex_published = r'"datePublished":"([^"]+)"'
    regex_modified = r'"dateModified":"([^"]+)"'
    
    results = []
    
    for url in urls:
        try:
            # Obtener el contenido HTML de la página
            response = requests.get(url)
            response.raise_for_status()  # Para lanzar un error si la respuesta no es exitosa
            html = response.text

            # Buscar las fechas usando regex
            published_dates = re.findall(regex_published, html)
            modified_dates = re.findall(regex_modified, html)

            # Considerando solo la primera coincidencia si hay varias
            published_date = published_dates[0] if published_dates else "No encontrado"
            modified_date = modified_dates[0] if modified_dates else "No encontrado"

            # Añadir los resultados a la lista
            results.append({"URL": url, "Fecha de Publicación": published_date, "Fecha de Modificación": modified_date})
        
        except Exception as e:
            # En caso de error, añadir un mensaje de error en los resultados
            results.append({"URL": url, "Fecha de Publicación": "Error", "Fecha de Modificación": "Error"})
            st.write(f"Error procesando la URL {url}: {e}")
    
    return results

# Configuración del Sidebar
st.sidebar.title("Descripción")
st.sidebar.write("""
Esta herramienta permite extraer las fechas de **publicación** y **modificación** de URLs que contienen datos estructurados en formato JSON-LD. 

### Stack:
- **Python**
- **Streamlit**
- **Requests**
- **Pandas**
- **Regex**
""")

# Interfaz de usuario de Streamlit
st.title("🤖 Extractor de 'DatePublished' y 'DateModified' JSON-LD")

# Campo de texto para ingresar las URLs
url_input = st.text_area("Ingresa las URLs (una por línea)")

# Botón para lanzar el proceso
if st.button("Procesar URLs"):
    # Convertir el input en una lista de URLs
    urls = [url.strip() for url in url_input.splitlines() if url.strip()]
    
    if urls:
        # Procesar las URLs
        result_data = process_urls(urls)
        
        # Convertir los resultados en un DataFrame de pandas
        df = pd.DataFrame(result_data)
        
        # Filtrar las filas que no tienen error
        df_filtered = df[(df['Fecha de Publicación'] != "Error") & (df['Fecha de Publicación'] != "No encontrado")]

        # Convertir las fechas a formato datetime
        df_filtered['Fecha de Publicación'] = pd.to_datetime(df_filtered['Fecha de Publicación'], errors='coerce')
        df_filtered['Fecha de Modificación'] = pd.to_datetime(df_filtered['Fecha de Modificación'], errors='coerce')
        
        # Mostrar la tabla en la interfaz
        st.write("Resultados:")
        st.dataframe(df)
        
        # Convertir el DataFrame a CSV para descarga
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Botón para descargar el CSV
        st.download_button(
            label="Descargar CSV",
            data=csv_data,
            file_name="fechas_publicacion_modificacion.csv",
            mime="text/csv",
        )

        # Visualización 1: Número de artículos publicados y modificados por año
        st.subheader("Número de artículos publicados y modificados por año")
        col1, col2, col3 = st.columns(3)

        # Gráfico de publicaciones por año
        with col1:
            st.write("Número de artículos publicados por año")
            df_filtered['Año de Publicación'] = df_filtered['Fecha de Publicación'].dt.year
            articles_per_year = df_filtered.groupby('Año de Publicación').size().reset_index(name='Número de Artículos')
            
            chart1 = alt.Chart(articles_per_year).mark_bar().encode(
                x='Año de Publicación:O',
                y='Número de Artículos:Q',
            ).properties(width=250)  # Ajuste de ancho para caber en la columna

            st.altair_chart(chart1)

        # Gráfico de modificaciones por año
        with col2:
            st.write("Número de artículos modificados por año")
            df_filtered['Año de Modificación'] = df_filtered['Fecha de Modificación'].dt.year
            modifications_per_year = df_filtered.groupby('Año de Modificación').size().reset_index(name='Número de Artículos Modificados')

            chart_modifications = alt.Chart(modifications_per_year).mark_bar(color='orange').encode(
                x='Año de Modificación:O',
                y='Número de Artículos Modificados:Q',
            ).properties(width=250)  # Ajuste de ancho para caber en la columna

            st.altair_chart(chart_modifications)

        # Gráfico de la evolución acumulada de artículos publicados a lo largo del tiempo
        with col3:
            st.write("Evolución acumulada de artículos publicados")
            
            # Ordenar por fecha de publicación
            df_filtered = df_filtered.sort_values(by='Fecha de Publicación')  
            
            # Generar la columna de acumulado
            df_filtered['Artículos Acumulados'] = range(1, len(df_filtered) + 1)

            articles_time_series = df_filtered[['Fecha de Publicación', 'Artículos Acumulados']]

            # Crear el gráfico de línea
            chart_cumulative = alt.Chart(articles_time_series).mark_line(color='green').encode(
                x='Fecha de Publicación:T',
                y='Artículos Acumulados:Q',
            ).properties(width=250)  # Ajuste de ancho para caber en la columna

            st.altair_chart(chart_cumulative)




    else:
        st.write("Por favor, ingresa al menos una URL.")
