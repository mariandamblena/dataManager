import os
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import time  # Para simular un proceso de carga

# Función para convertir fechas y horas al formato correcto
def convertir_fecha_hora(fecha, hora):
    try:
        if pd.isna(fecha) or pd.isna(hora):
            raise ValueError("Fecha o hora es NaN")
        # Convertir fecha y hora al objeto datetime
        dt = datetime.strptime(str(fecha) + ' ' + str(hora), '%d.%m.%y %H:%M:%S')
        # Formatear el datetime al formato requerido
        return '[' + dt.strftime('%d-%m %H:%M:%S.%f')[:-3] + ']'
    except Exception as e:
        st.warning(f"Error al procesar fila con Date: {fecha} y Time: {hora} -> {e}")
        return None

# Función para simular el procesamiento de datos
def procesar_datos(input_file, incubadora_file, output_folder):
    try:
        # Simular un proceso de carga
        with st.spinner('Procesando archivos. Por favor, espera...'):
            time.sleep(5)  # Simular un proceso de 5 segundos
            
            # Leer el archivo de texto
            lines = input_file.getvalue().decode("utf-8").splitlines()
            
            # Procesar cada línea y extraer los datos necesarios
            data_rows = []
            for line in lines:
                if 'INFO  co2sens' in line:
                    try:
                        # Obtener timestamp
                        timestamp = line.split()[0] + ' ' + line.split()[1]
                        
                        # Obtener número de sensor (co2sens9, co2sens11, co2sens13)
                        co2sens = line.split()[3]
                        
                        # Obtener mediciones de CO2 y temperaturas
                        parts = line.split()
                        co2_1 = float(parts[4].split('=')[1]) / 10000  # Dividir por 10000 para convertir a %
                        co2_3 = float(parts[6].split('=')[1])  # Mantener sin cambios
                        
                        # Crear la fila de datos en el formato requerido
                        data_row = (timestamp, co2sens, co2_1, co2_3)
                        data_rows.append(data_row)
                    except (IndexError, ValueError) as e:
                        st.warning(f"Error procesando la línea: {line.strip()} -> {e}")
            
            # Crear un DataFrame con los datos del archivo de texto
            datos_df = pd.DataFrame(data_rows, columns=['Timestamp', 'Número de Sensor', 'Concentración CO2 (%)', 'Temperatura (°C)'])
            
            # Leer el archivo Excel de incubadora
            incubadora_df = pd.read_excel(incubadora_file)
            
            # Eliminar filas vacías
            incubadora_df.dropna(subset=['Date', 'Time'], inplace=True)
            
            # Asegurarse de que todas las entradas sean cadenas
            incubadora_df['Date'] = incubadora_df['Date'].astype(str)
            incubadora_df['Time'] = incubadora_df['Time'].astype(str)
            
            # Crear la columna 'Timestamp' con el formato requerido
            incubadora_df['Timestamp'] = incubadora_df.apply(lambda row: convertir_fecha_hora(row['Date'], row['Time']), axis=1)
            
            # Agregar la columna 'Número de Sensor' con valor 'Incubadora'
            incubadora_df['Número de Sensor'] = 'Incubadora'
            
            # Seleccionar y reordenar las columnas de incubadora_formateado
            incubadora_df_reordered = incubadora_df[['Timestamp', 'Número de Sensor', incubadora_df.columns[4], incubadora_df.columns[3]]]
            
            # Renombrar las columnas para que coincidan con datos_df
            incubadora_df_reordered.columns = ['Timestamp', 'Número de Sensor', 'Temperatura (°C)', 'Concentración CO2 (%)']
            
            # Concatenar los datos
            combined_df = pd.concat([datos_df, incubadora_df_reordered], ignore_index=True)
            
            # Guardar el DataFrame combinado en un nuevo archivo Excel
            output_file = os.path.join(output_folder, 'datos_combinado.xlsx')
            combined_df.to_excel(output_file, index=False)
        
        # Mostrar mensaje de éxito
        st.success(f'Archivo combinado generado correctamente: {output_file}')
    except Exception as e:
        # Mostrar mensaje de error
        st.error(f"Error procesando los archivos: {e}")

# Función para la aplicación de visualización
def aplicacion_visualizacion():
    # Título de la aplicación de visualización
    st.title("Visualización Interactiva de Datos Excel")

    # Subir el archivo Excel
    uploaded_file = st.file_uploader("Elige un archivo Excel", type="xlsx")

    if uploaded_file is not None:
        # Leer el archivo Excel
        df = pd.read_excel(uploaded_file, header=0)  # header=0 indica que la primera fila son los encabezados
        
        # Mostrar el dataframe
        st.write("Datos del archivo Excel:")
        st.write(df)
        
        # Mostrar los nombres de las columnas para verificar
        st.write("Nombres de las columnas:")
        st.write(df.columns.tolist())
        
        # Asegurarse de que el DataFrame tiene una columna de fecha y hora
        date_column = st.selectbox("Selecciona la columna de fecha y hora", df.columns)
        
        # Convertir la columna de fecha y hora al formato correcto
        df[date_column] = pd.to_datetime(df[date_column], format='[%d-%m %H:%M:%S.%f]')
        
        # Selección de rango de fecha y hora
        min_date = df[date_column].min()
        max_date = df[date_column].max()
        start_date = st.date_input("Fecha de inicio", min_date)
        end_date = st.date_input("Fecha de fin", max_date)
        start_time = st.time_input("Hora de inicio", min_date.time())
        end_time = st.time_input("Hora de fin", max_date.time())
        
        start_datetime = pd.to_datetime(f"{start_date} {start_time}")
        end_datetime = pd.to_datetime(f"{end_date} {end_time}")
        
        # Filtrar el DataFrame por el rango de fecha y hora seleccionado
        mask = (df[date_column] >= start_datetime) & (df[date_column] <= end_datetime)
        df_filtered = df[mask]
        
        # Mostrar el dataframe filtrado
        st.write("Datos filtrados del archivo Excel:")
        st.write(df_filtered)
        
        # Selección de columnas para graficar
        columns = df_filtered.columns.tolist()
        x_axis = date_column
        y_axes = st.multiselect("Selecciona las columnas para el eje Y", columns, default=columns[2:])
        
        # Crear gráficos combinados por Número de Sensor
        for y_axis in y_axes:
            df_filtered = df_filtered[pd.to_numeric(df_filtered[y_axis], errors='coerce').notnull()]
            df_filtered[y_axis] = df_filtered[y_axis].astype(float)
        
        # Graficar usando Plotly Express
        st.write("Gráfico combinado con Plotly Express:")
        fig_plotly = px.line(df_filtered, x=x_axis, y=y_axes, color="Número de Sensor", title="Variables vs Tiempo", labels={"value": "Valor", "variable": "Variable"})
        st.plotly_chart(fig_plotly)
        
        # Mostrar estadísticas para cada columna Y seleccionada en una tabla
        for y_axis in y_axes:
            st.write(f"### Estadísticas de {y_axis}:")
            stats_df = df_filtered.groupby("Número de Sensor")[[y_axis]].describe().transpose()
            st.write(stats_df)

# Lógica para ejecutar la aplicación principal
if __name__ == "__main__":
    # Título de la aplicación principal
    st.title("Menú General")

    # Opciones del menú
    opciones = ["Procesamiento de Datos", "Visualización de Datos"]
    opcion_seleccionada = st.radio("Selecciona una opción:", opciones)

    if opcion_seleccionada == "Procesamiento de Datos":
        st.subheader("Procesamiento de Datos")

        # Sección para seleccionar los archivos de entrada y la carpeta de salida
        st.sidebar.header("Configuración de Archivos")
        input_file = st.sidebar.file_uploader("Selecciona el archivo de texto", type="txt")
        incubadora_file = st.sidebar.file_uploader("Selecciona el archivo Excel de la incubadora", type="xlsx")
        output_folder = st.sidebar.text_input("Selecciona la carpeta de salida", value=os.getcwd())

        if st.sidebar.button("Procesar Archivos"):
            if input_file is not None and incubadora_file is not None:
                procesar_datos(input_file, incubadora_file, output_folder)
            else:
                st.sidebar.warning("Por favor, selecciona ambos archivos de entrada.")

    elif opcion_seleccionada == "Visualización de Datos":
        st.subheader("Visualización de Datos")

        # Llamar directamente a la aplicación de visualización
        aplicacion_visualizacion()
