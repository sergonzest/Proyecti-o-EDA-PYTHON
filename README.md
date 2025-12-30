# Proyecti-o-EDA-PYTHON
1.Se ha realizado un análisis que tiene como objetivo explorar y unificar los datos de la última campaña de marketing captación de préstamos. Se han integrado datos demográficos de clientes (años 2012, 2013 y 2014) con indicadores económicos y resultados de contacto para identificar el perfil de cliente con mayor probabilidad de éxito.

2. Proceso de Transformación y Limpieza
-Unificación de fuentes: Se unieron tres archivos anuales de detalles de clientes con la base de datos principal mediante el identificador único (ID).
Gestión de nulos: Se detectó una falta de datos significativa en la Edad (12%) y el Euribor (21%), la cual fue corregida mediante la imputación por la mediana.
-Variables categóricas como job y education con valores faltantes fueron etiquetadas como "unknown" para no perder registros.
Estandarización: Se limpiaron etiquetas de texto para evitar duplicados por errores de escritura.

3. Análisis Descriptivo (Hallazgos Principales)
Tras procesar los datos, se extrajeron las siguientes estadísticas clave:
-Perfil Demográfico: El cliente promedio tiene 40 años. El sector profesional más frecuente es el administrativo.
-Situación Económica: Los ingresos medios se sitúan en 93,241 unidades, aunque existe una alta dispersión (desviación típica de 50,498).
-Tasa de Conversión: La campaña tuvo un éxito del 11% (clientes que aceptaron el producto), frente a un 89% de rechazos.

4. Visualización y Conclusiones del EDA
A través de la exploración gráfica, se identificaron patrones críticos:
-Impacto de la Edad: La mayoría de las conversiones exitosas se concentran en el rango de 30 a 45 años.
-Influencia del Contacto: El Mapa de Calor reveló que la variable con mayor correlación positiva con el éxito es la duración de la llamada. Cuanto más tiempo se logra retener al cliente al teléfono, mayor es la probabilidad de aceptación.
-Contexto Económico: Se observa que el éxito de la campaña es inversamente proporcional al Euribor. En periodos de tipos de interés altos, la disposición de los clientes a contratar nuevos préstamos disminuye notablemente.

En cuanto a la matriz de correlación, se puede ver como afectan a las distinas variables el tipo de correlación
Valores cercanos a 1: Indican una correlación positiva fuerte. Si una variable sube, la otra también.
Valores cercanos a -1: Indican una correlación negativa fuerte. Si una sube, la otra baja.
Valores cercanos a 0: No hay relación lineal entre ellas.

En cuanto a la relación cruzada con el éxito de campaña, se puede apreciar cuales son las variables que mejoran, empeoran o se quedan igual según su correlación cruzada

-Correlación Positiva Alta (Cercana a 1): Son los "impulsores". Por ejemplo, si duration tiene un valor alto (ej: 0.40), significa que a más duración, mucho más éxito.
-Correlación Cercana a 0: Son variables que no afectan al resultado. Podrías sugerir al banco que deje de fijarse en ellas (ej: quizás la edad no influye tanto como pensaban).
-Correlación Negativa (Cercana a -1): Son los "frenos". Por ejemplo, si campaign es negativa, significa que llamar demasiadas veces a un cliente reduce las posibilidades de que acepte.
