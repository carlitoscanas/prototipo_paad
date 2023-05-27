# Solución Analítica TB500

El presente proyecto se enfoca en la optimización de un portafolio de activos utilizando datos predichos (corto plazo) e históricos de precios de acciones. Este modelo utiliza técnicas de análisis y algoritmos de optimización para determinar la combinación óptima de activos en un portafolio, maximizando el rendimiento esperado y minimizando el riesgo.

## Estructura del proyecto

El proyecto se organiza en la siguiente estructura de carpetas y archivos:

- **data**: Contiene la data de la solución organizada como un lago de datos (Bronze, Silver, Gold).
- **documents**: Documentos relacionados con el desarrollo del proyecto y un manual de uso de la solución.
- **etl**: Código fuente del proceso ETL (Extracción, Transformación y Carga) para cargar y preparar los datos.
- **notebooks**: Notebooks utilizados en el proyecto en las etapas de experimentación y pruebas.
- **portfolio_optimization**: Código del modelo de optimización consumido desde un API REST.
- **stock_price_prediction**: Código de modelos predictivos para predecir el precio de acciones.

Además de las carpetas mencionadas, el proyecto también incluye los siguientes archivos:

- **Dockerfile**: Archivo utilizado para construir una imagen de Docker para el proyecto.
- **requirements.txt**: Archivo que lista las dependencias del proyecto para facilitar su instalación.

## Consumo

La solución puede ser utilizada y consumida a través del siguiente endpoint: http://ec2-18-217-18-255.us-east-2.compute.amazonaws.com:5000/api

Es importante revisar el manual de usuario (disponible en la carpeta de documentos) para hacer un uso apropiado del API.