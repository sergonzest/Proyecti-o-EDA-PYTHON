# %%
pip install openpyxl

# %%
import pandas as pd
#CARGA DE DATOS

# 1. Cargar el archivo principal (CSV)
df_bank = pd.read_csv('bank-additional.csv')

# 2. Cargar las hojas del Excel (Daba error cuando se cargaban todas a la vez)
# Usamos sheet_name=None para leer todas las hojas a la vez en un diccionario
dict_hojas = pd.read_excel('customer-details.xlsx', sheet_name=None)

# 3. Unir las hojas (2012, 2013, 2014) en un solo DataFrame
df_detalles = pd.concat(dict_hojas.values(), ignore_index=True)

# 4. Unión final con el archivo del banco
df_final = pd.merge(df_bank, df_detalles, left_on='id_', right_on='ID', how='inner')

print(f"El dataset unido tiene {df_final.shape[0]} filas y {df_final.shape[1]} columnas.")
df_final.head()

# %%
import numpy as np

# %%
#1.LIMPIEZA DE DATOS
#Corregir números con comas
cols_comas = ['cons.price.idx', 'cons.conf.idx', 'euribor3m']
for col in cols_comas:
    if col in df_final.columns:
        df_final[col] = df_final[col].astype(str).str.replace(',', '.').astype(float)

# %%
# Calcular la cantidad de nulos
nulos = df_final.isnull().sum()

# Calcular el porcentaje de nulos
porcentaje = (df_final.isnull().sum() / len(df_final)) * 100

# 3. Creamos una tabla para tener mejor visualización
tabla_nulos = pd.DataFrame({'Total Nulos': nulos, 'Porcentaje %': porcentaje})

print(tabla_nulos)

# %%
#Dado que el porcentaje de nulos en edad y euribor es muy alto, vamos a sustituir los nulos por la mediana, para tener una orientación y no entorpecer al resto de datos
# Rellenar la edad con la mediana (el valor central)
df_final['age'] = df_final['age'].fillna(df_final['age'].median())

# Rellenar el euribor con la mediana
df_final['euribor3m'] = df_final['euribor3m'].fillna(df_final['euribor3m'].median())

# %%
# Al resto de columnas con datos desconocidos, lo vamos a rellenar con "desconocido"
df_final['job'] = df_final['job'].fillna('unknown')
df_final['education'] = df_final['education'].fillna('unknown')

# %%
# Limpiar caracteres especiales en las categorías para que todo sea uniforme
df_final['education'] = df_final['education'].str.replace('.', ' ', regex=False).str.title()
df_final['job'] = df_final['job'].str.replace('.', ' ', regex=False).str.capitalize()

print(df_final['education'].unique())

# %%
# Crear una nueva columna de "Segmento de Edad", para que sea más fácil la interpretación
bins = [0, 30, 50, 100]
labels = ['Joven', 'Adulto', 'Senior']
df_final['age_group'] = pd.cut(df_final['age'], bins=bins, labels=labels)


# %%
#2.ANÁLISIS DESCRIPTIVO DE LOS DATOS
# Estadísticas generales de las variables numéricas
resumen_stats = df_final[['age', 'Income', 'campaign', 'euribor3m']].describe().round(2)
print(resumen_stats)

# %%
#Estadísticas generales de variables categóricas
# 1. Seleccionamos las columnas que son de tipo 'object' (texto) o 'category'
variables_categoricas = df_final.select_dtypes(include=['object', 'category']).columns

# 2. Calculamos las estadísticas descriptivas para estas columnas
resumen_categorico = df_final[variables_categoricas].describe()

# 3. Mostramos el resultado
print("Estadísticas de Variables Categóricas:")
display(resumen_categorico)

# %%
# Para hacerlo más completo, Comparamos el promedio de ingresos según si aceptaron o no
analisis_ingresos = df_final.groupby('y')['Income'].mean().round(2)
print("Promedio de Ingresos según éxito de campaña:")
print(analisis_ingresos)

# %%
pip install seaborn

# %%
# Guardar el DataFrame final en un nuevo archivo CSV (añadido el enconding para no tener confusión con tildes)
df_final.to_csv('datos_limpios.csv', index=False, encoding='utf-8-sig')


# %%
#3. VISUALIZACIÓN DE DATOS. Empezamos importando matplotlib.plylot para poder hacer gráficos en Python
import seaborn as sns
import matplotlib.pyplot as plt

# %%
#3.1 Análisis de distribución de clientes. ¿Como son mis clientes?
#Creamos un histograma para ver donde se concentra la mayoría
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
sns.histplot(df_final['age'], kde=True, color='skyblue')
plt.title('Distribución de la Edad')


# %%
#Creamos un gráfico de bigotes para ver los valores extraños o outliers
plt.subplot(1, 2, 2)
sns.boxplot(x=df_final['age'], color='lightcoral')
plt.title('Detección de Outliers en Edad')

# %%
#3.2 Análisis de categorias. ¿A que se dedican mis clientes?
#Utilizamos un gráfico de barras para que sea más legible y fácil de entender
plt.figure(figsize=(10, 6))
order = df_final['job'].value_counts().index
sns.countplot(data=df_final, y='job', order=order)
plt.title('Frecuencia de Tipos de Trabajo')
plt.xlabel('Cantidad de Clientes')
plt.show()

# %%
#3.3 Analisis de Relación. ¿Que hace que compren mis clientes?
# ¿Influye el nivel de ingresos en la decisión? Utlizamos un gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x='y', y='Income', data=df_final)
plt.title('Promedio de Ingresos: Usuarios que Aceptaron vs No Aceptaron')
plt.show()

# Relación entre duración de llamada y éxito. Utizamos un gráficp de violín
plt.figure(figsize=(10, 6))
sns.violinplot(x='y', y='duration', data=df_final)
plt.title('Relación entre Duración de la Llamada y Éxito')
plt.show()

# %%
#3.4 CORRELACIONES
# Mapa de calor de variables numéricas. Para ver si se "mueven juntas" o están distintas unas de las otras.
plt.figure(figsize=(12, 8))
columnas_estudio = ['age', 'Income', 'duration', 'campaign', 'euribor3m']
corr = df_final[columnas_estudio].corr()

sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Matriz de Correlación de Variables Clave')
plt.show()

# %%
#3.5 Análisis temporal .¿Como se captan más clientes?
# Evolución de ingresos o registros por año. Utilizamos un gráfico de lineas para ver el progreso durante los 3 años que tenemos registrados
df_final['año_registro'] = df_final['Dt_Customer'].dt.year
sns.lineplot(x='año_registro', y='Income', data=df_final, marker='o')
plt.title('Evolución del Ingreso Promedio por Año de Registro')
plt.xticks([2012, 2013, 2014])
plt.show()

# %%
# 3.6 Calculo de insights por aceptación según niveles ecónomicos.
# Hacemos 3 categorías según ingresos
condiciones = [
    (df_final['Income'] < 50000),
    (df_final['Income'].between(50000, 100000)),
    (df_final['Income'] > 100000)
]
etiquetas = ['Bajo', 'Medio', 'Alto']
df_final['Segmento_Socioeconomico'] = np.select(condiciones, etiquetas, default='Desconocido')

# 2. FILTRADO, AGRUPAMIENTO Y AGREGACIÓN EN CADENA (Extraer Insights)
insight_tabla = (
    df_final.groupby('Segmento_Socioeconomico')
    .agg({
        'Income': 'mean',
        'age': 'mean',
        'y': lambda x: (x == 'yes').mean() * 100  # Se calcula el porcentaje de éxito
    })
    .rename(columns={
        'Income': 'Ingreso_Promedio',
        'age': 'Edad_Promedio',
        'y': '%_Exito_Campaña'
    })
    .sort_values(by='%_Exito_Campaña', ascending=False)
    .round(2)
)

print("Tabla de Insights Estratégicos:")
display(insight_tabla)

# %%

plt.figure(figsize=(10, 6))
sns.barplot(x=insight_tabla.index, y='%_Exito_Campaña', data=insight_tabla,)
plt.title('Tasa de Conversión por Segmento Socioeconómico',)
plt.ylabel('% de Éxito (Clientes que dijeron SÍ)')
plt.xlabel('Nivel de Ingresos')
plt.show()

# %%
#4.MATRIZ DE CORRELACIÓN
# 1. Seleccionamos solo las variables numéricas que aportan valor al análisis
columnas_numericas = ['age', 'Income', 'duration', 'campaign', 'pdays', 'previous', 'euribor3m']

# 2. Calculamos la matriz de correlación
# Aplicamos .round(2) para que sea más legible
matriz_corr = df_final[columnas_numericas].corr().round(2)

# 3. Configuramos el gráfico (Heatmap)
plt.figure(figsize=(12, 8))

sns.heatmap(matriz_corr, 
            annot=True,           
            mask=mask,            
            cmap='coolwarm',      
            fmt=".2f",            
            linewidths=0.5,       
            vmin=-1, vmax=1)      

plt.title('Matriz de Correlación: Variables Numéricas', fontsize=16)
plt.show()

# %%
#6. RELACIONES CRUZADAS CON EXITO DE LA CAMPAÑA
#1. Aseguramos que la variable objetivo sea numérica (0 y 1)
df_final['exito_campaña'] = df_final['y'].map({'yes': 1, 'no': 0})

# 2. Seleccionamos solo las columnas numéricas
df_numerico = df_final.select_dtypes(include=['number'])

# 3. Calculamos la correlación de todas las variables contra 'exito_campaña'
relacion_objetivo = df_numerico.corr()['exito_campaña'].sort_values(ascending=False).to_frame().round(2)

# 4. Visualización de la relación
plt.figure(figsize=(6, 8))
sns.heatmap(relacion_objetivo, annot=True, cmap='RdYlGn', cbar=False, fmt=".2f")
plt.title('Relación de Variables vs Éxito de Campaña')
plt.show()



