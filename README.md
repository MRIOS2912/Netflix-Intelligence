# Netflix Intelligence

## Proyecto académico de análisis cuantitativo

**Netflix Intelligence** es un proyecto académico de análisis
exploratorio y estadístico desarrollado con Python. Utiliza un conjunto
de datos sintético inspirado en una plataforma de streaming para
practicar inspección, limpieza, análisis descriptivo, visualización e
interpretación de datos.

> **Alcance:** los archivos son sintéticos. Los resultados describen
> únicamente el conjunto analizado y no representan información oficial
> de Netflix ni el comportamiento real de sus usuarios.

## 1. Objetivo

Explorar los datos de usuarios, catálogo, reproducciones, reseñas y
búsquedas; identificar problemas de calidad; calcular estadísticas
descriptivas y comunicar los hallazgos mediante gráficas y paneles en
español.

## 2. Datos utilizados

Los archivos CSV se encuentran en `data/`.

  ------------------------------------------------------------------------------
  Archivo                     Contenido                         Filas originales
  --------------------------- --------------------- ----------------------------
  `users.csv`                 Usuarios: edad, país,                       10.300
                              suscripción y         
                              dispositivo           

  `movies.csv`                Catálogo de                                  1.040
                              películas, series y   
                              otros contenidos      

  `watch_history.csv`         Historial de                               105.000
                              reproducciones        

  `reviews.csv`               Reseñas,                                    15.450
                              calificaciones y      
                              sentimiento           

  `search_logs.csv`           Consultas y actividad                       26.500
                              de búsqueda           

  `recommendation_logs.csv`   Registros de                                52.000
                              recomendaciones       
  ------------------------------------------------------------------------------


## 3. Metodología

1.  Cargar los archivos CSV y revisar sus dimensiones, columnas y tipos
    de datos.
2.  Auditar datos faltantes, duplicados exactos y valores fuera de rango
    cuando corresponda.
3.  Excluir duplicados exactos de los análisis descriptivos mediante
    `drop_duplicates()`.
4.  Validar las variables relevantes para cada análisis; por ejemplo,
    edades entre 0 y 100 años, duraciones no negativas y porcentajes de
    avance entre 0 y 100.
5.  Calcular estadísticas descriptivas y frecuencias.
6.  Generar gráficas y paneles con Matplotlib.
7.  Guardar las salidas en `resultados/` y revisar las interpretaciones.

### Criterio de limpieza

Los duplicados exactos son filas cuyos valores coinciden en todas las
columnas de un mismo archivo. Se excluyen en memoria de los análisis
descriptivos, pero **los CSV originales no se sobrescriben ni se
modifican**. No se elimina una fila solo por compartir un identificador
con otra y no se imputan valores faltantes automáticamente. Las
auditorías deben ejecutarse sobre los archivos originales para que los
problemas de calidad sigan siendo verificables.

  ------------------------------------------------------------------------------------
  Archivo                       Filas originales Duplicados exactos   Filas después de
                                                                    excluir duplicados
  --------------------------- ------------------ ------------------ ------------------
  `users.csv`                             10.300                300             10.000

  `movies.csv`                             1.040                 40              1.000

  `watch_history.csv`                    105.000              5.000            100.000

  `reviews.csv`                           15.450                450             15.000

  `search_logs.csv`                       26.500              1.500             25.000

  `recommendation_logs.csv`               52.000              2.000             50.000
  ------------------------------------------------------------------------------------

## 4. Herramientas

-   **Python 3:** lenguaje utilizado para los análisis.
-   **pandas:** carga, limpieza y resumen de los datos.
-   **NumPy:** operaciones numéricas cuando se requieren.
-   **Matplotlib:** creación de gráficas y paneles.
-   **Visual Studio Code:** edición y ejecución de los scripts.
-   **GitHub:** publicación del código y documentación del proyecto.

## 5. Estructura del proyecto

``` text
Netflix-Intelligence/
├── data/
│   ├── users.csv
│   ├── movies.csv
│   ├── watch_history.csv
│   ├── reviews.csv
│   ├── search_logs.csv
│   └── recommendation_logs.csv
├── resultados/
│   ├── galeria_graficos.html
│   ├── archivos PNG de las gráficas y paneles
│   ├── archivos PDF de los informes
│   └── informes CSV de auditoría y estadísticas
├── analisis_busquedas.py
├── analisis_edades.py
├── analisis_peliculas.py
├── analisis_resenas.py
├── analisis_usuarios.py
├── analisis_visualizacion.py
├── auditoria_usuarios.py
├── dashboard.py
├── dashboard_edades.py
├── panel_busquedas.py
├── panel_peliculas.py
├── panel_resenas.py
├── panel_visualizacion.py
└── README.md
```

La carpeta `resultados/` puede contener salidas adicionales generadas al
ejecutar los scripts.

## 6. Instalación y ejecución

Abre la carpeta raíz del proyecto en Visual Studio Code. En la terminal
instala las bibliotecas necesarias:

``` bash
python -m pip install pandas matplotlib numpy
```

Para generar el dashboard general:

``` bash
python dashboard.py
```

El dashboard de edades se puede generar con:

``` bash
python dashboard_edades.py
```

Los paneles temáticos se pueden ejecutar desde la misma carpeta raíz:

``` bash
python panel_peliculas.py
python panel_resenas.py
python panel_busquedas.py
python panel_visualizacion.py
```

Los análisis y las auditorías se ejecutan con
`python nombre_del_archivo.py`, sustituyendo el nombre por el script
deseado. Las imágenes y los documentos se guardan en `resultados/`.

## 7. Cómo abrir la galería de gráficas

La galería reúne visualizaciones en una sola página HTML.

**Desde el Explorador de archivos:** 
1. Abre la carpeta `resultados/`.
2. Haz doble clic en `galeria_graficos.html`. 
3. Si alguna imagen no aparece, verifica que el PNG correspondiente esté en `resultados/` y que
su nombre coincida con la ruta indicada en el HTML.

**Desde la terminal de PowerShell de VS Code**, estando en la carpeta
raíz del proyecto:

``` powershell
Start-Process .\resultados\galeria_graficos.html
```

Este comando solo abre el archivo HTML existente; no genera ni actualiza
las gráficas. Para actualizar la galería después de regenerar un panel,
vuelve a ejecutar el script correspondiente y recarga la página del
navegador. Si el HTML usa nombres de imágenes guardadas, comprueba que
esos archivos se hayan actualizado y que las rutas sigan siendo válidas.

## 8. Resultados e interpretación

Las interpretaciones siguientes son descriptivas. No permiten
generalizar los resultados a Netflix real ni establecer relaciones
causales.

###  Edades de los usuarios

El archivo original contiene 10.300 filas; después de excluir 300
duplicados exactos quedan 10.000 filas para el análisis. La edad se
convierte a variable numérica y se excluyen de las estadísticas de edad
los valores faltantes/no numéricos y los valores fuera del rango de 0 a
100 años.

La media y la mediana observadas durante el desarrollo se sitúan
aproximadamente alrededor de los 35 años. El histograma permite observar
en qué intervalos se concentran las edades válidas; el diagrama de caja
ayuda a reconocer la dispersión y posibles valores atípicos. La
presencia de edades faltantes y la naturaleza sintética de los datos
requieren cautela.

###  Catálogo de contenidos

El catálogo contiene 1.040 filas originales, de las cuales 40 son
duplicados exactos; el panel analiza 1.000 filas tras la limpieza. En la
gráfica revisada, las categorías mostradas incluyen 444 películas, 254
series, 136 documentales, 115 registros de comedia en vivo y 51
miniseries. Por tanto, las películas son la categoría más numerosa
dentro de este conjunto depurado.

La gráfica de géneros compara los géneros más frecuentes; el histograma
de calificaciones IMDb muestra cómo se distribuyen las puntuaciones, y
la línea por año de estreno permite observar la frecuencia registrada en
cada año. En la ejecución revisada, el promedio IMDb mostrado es 6,28.
Estas cantidades describen el CSV sintético, no el catálogo oficial de
Netflix.

###  Historial de visualización

El historial original contiene 105.000 filas, incluidas 5.000 duplicadas
exactas. Los paneles analizan 100.000 filas después de excluir esas
repeticiones. El histograma de duración permite estudiar cómo se
distribuyen los minutos de visualización; el histograma de porcentaje de
avance muestra la distribución del progreso de reproducción; las
gráficas de acciones y dispositivos comparan la frecuencia de los
registros por categoría.

Los valores negativos de duración y los porcentajes fuera del intervalo
de 0 a 100 no se incluyen en las distribuciones correspondientes. Los
resultados no demuestran qué dispositivos prefieren los clientes reales
de Netflix.

###  Reseñas y calificaciones

El archivo original contiene 15.450 filas y 450 duplicados exactos; el
panel trabaja con 15.000 filas únicas por contenido de fila. Las
gráficas resumen las calificaciones, los sentimientos, los dispositivos
y otros atributos disponibles en las reseñas. La calificación promedio
observada en el desarrollo fue aproximadamente 3,66 sobre 5 y se
registró predominio de reseñas etiquetadas como positivas.

Los valores faltantes y las categorías sin clasificar deben tenerse en
cuenta al leer porcentajes. Las etiquetas de sentimiento son datos del
conjunto sintético y no una medición de la opinión de clientes reales.

###  Búsquedas

El archivo original contiene 26.500 filas, incluidas 1.500 duplicadas
exactas. Tras excluirlas, el panel analiza 25.000 filas. La gráfica de
frecuencias ayuda a identificar las consultas que más aparecen y permite
explorar categorías, dispositivos y patrones de escritura. Algunas
consultas se conservan en inglés porque así figuran en el CSV; las
etiquetas explicativas de las gráficas se traducen cuando corresponde.

Las frecuencias indican qué valores se repiten en este conjunto, no
cuáles son las búsquedas más comunes en Netflix real.

###  Perfil general de usuarios

El panel de usuarios compara atributos como plan de suscripción, país,
dispositivo principal y estado de actividad. Las frecuencias permiten
ver qué categorías tienen más registros y comparar la composición del
archivo. Como se trata de datos sintéticos, no se deben interpretar como
proporciones reales de suscriptores.

## 9. Calidad de los datos y limitaciones

-   Se detectaron duplicados exactos en los seis CSV; los paneles
    descriptivos los excluyen en memoria y las fuentes se conservan.
-   Los valores faltantes pueden reducir el número de observaciones
    disponibles para una estadística concreta.
-   Las variables deben validarse según su significado: por ejemplo,
    porcentaje de avance entre 0 y 100 y edad entre 0 y 100 años para el
    análisis de edades.
-   No se deben sumar filas de archivos diferentes como si fueran
    individuos únicos.
-   Los resultados dependen de la estructura y calidad del conjunto
    sintético.
-   La galería HTML local necesita las imágenes PNG referenciadas en sus
    rutas para mostrarlas correctamente.

## 10. Conclusiones

1.  La inspección y la limpieza son pasos necesarios antes de
    interpretar resultados estadísticos.
2.  Excluir duplicados exactos evita contar repetidamente filas
    idénticas en los análisis, sin destruir los archivos originales.
3.  Las estadísticas descriptivas y las gráficas permiten resumir las
    edades, comparar categorías del catálogo y explorar patrones en
    reproducciones, reseñas y búsquedas.
4.  Los datos faltantes y los valores fuera de rango deben documentarse
    porque pueden afectar las estadísticas.
5.  Las visualizaciones facilitan comunicar los hallazgos, pero deben
    acompañarse de explicaciones y del contexto de los datos.
6.  Las conclusiones se limitan a los archivos sintéticos utilizados; no
    representan el comportamiento real de Netflix ni permiten establecer
    causalidad.

## 11. Referencias bibliográficas

Sayeeduddin. (s. f.). *Netflix 2025: User Behavior Dataset (210K+
Records)* \[Conjunto de datos\]. Kaggle.
https://www.kaggle.com/datasets/sayeeduddin/netflix-2025user-behavior-dataset-210k-records

Matplotlib Development Team. (s. f.). *Matplotlib documentation*.
https://matplotlib.org/stable/

NumPy Developers. (s. f.). *NumPy documentation*. https://numpy.org/doc/

pandas development team. (s. f.). *pandas documentation*.
https://pandas.pydata.org/docs/

Python Software Foundation. (s. f.). *Python documentation*.
https://docs.python.org/3/

------------------------------------------------------------------------

