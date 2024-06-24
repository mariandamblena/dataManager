Este programa proporciona a nuestra empresa la capacidad de procesar conjuntos de datos generados por diversos dispositivos, como sensores y incubadoras. Está diseñado para facilitar la gestión y análisis de datos procedentes de múltiples fuentes, permitiendo:

Procesamiento de Datos: Importar y combinar datos desde archivos de texto y hojas de cálculo Excel, generando un archivo combinado que facilita su análisis posterior.

Visualización Interactiva: Explorar y visualizar los datos de manera interactiva a través de gráficos dinámicos y estadísticas resumidas, facilitando la interpretación y la toma de decisiones informadas.

Este software está desarrollado en Python utilizando las bibliotecas Pandas, Streamlit y Plotly Express, ofreciendo una solución robusta y escalable para el manejo eficiente de grandes volúmenes de datos de dispositivos científicos.

Instalación y Ejecución:

Para instalar y ejecutar la aplicación, sigue estos pasos:

Instalar Poetry:

Poetry es un gestor de dependencias y entornos virtuales para Python. Si aún no tienes Poetry instalado, puedes hacerlo siguiendo las instrucciones en Poetry Installation Guide.
Activar el Entorno Virtual:

Una vez instalado Poetry, navega hasta el directorio del proyecto y activa el entorno virtual con el siguiente comando:
Copiar código
poetry shell
Instalar Dependencias:

Dentro del entorno virtual, instala las dependencias necesarias ejecutando:
Copiar código
poetry install
Esto instalará automáticamente las bibliotecas requeridas como Pandas, Plotly y Streamlit.
Ejecutar la Aplicación:

Con todas las dependencias instaladas, puedes ejecutar la aplicación con el siguiente comando:
arduino
Copiar código
streamlit run app.py
Asegúrate de estar en el directorio donde se encuentra tu archivo app.py. La aplicación se ejecutará localmente y podrás acceder a ella desde tu navegador web.
