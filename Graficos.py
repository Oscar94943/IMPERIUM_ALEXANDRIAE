import matplotlib.pyplot as plt 
import seaborn as sns           
import pandas as pd             
import numpy as np              

# --- Sección 1: Configuración Básica y Datos de Ejemplo ---
print("--- Sección 1: Configuración Básica y Datos de Ejemplo ---")

# Configuración básica para que los gráficos se vean bien
plt.style.use('ggplot') # Un estilo predefinido que se ve bien
plt.rcParams['figure.figsize'] = (10, 6) # Tamaño por defecto de las figuras
plt.rcParams['font.family'] = 'sans-serif' # Fuente para los textos
plt.rcParams['font.sans-serif'] = ['Arial'] # Especificar Arial como fuente sans-serif

# Datos de ejemplo para los gráficos
x = np.linspace(0, 10, 100) # 100 puntos entre 0 y 10
y1 = np.sin(x)
y2 = np.cos(x)
y_scatter = np.random.rand(50) * 10
x_scatter = np.random.rand(50) * 10
sizes = np.random.rand(50) * 100 + 50 # Tamaños de puntos para scatter

categorias = ['A', 'B', 'C', 'D', 'E']
valores = [23, 45, 56, 12, 39]

datos_histograma = np.random.randn(1000) * 10 + 50 # Datos con distribución normal

print("Datos de ejemplo creados.")

# --- Sección 2: Gráfico de Líneas Básico (plt.plot()) ---
print("\n--- Sección 2: Gráfico de Líneas Básico ---")

# Creamos una figura y un eje para el gráfico
plt.figure(figsize=(8, 5)) # Tamaño específico para esta figura
plt.plot(x, y1, label='Seno(x)', color='blue', linestyle='-', linewidth=2)
plt.plot(x, y2, label='Coseno(x)', color='red', linestyle='--', linewidth=1.5)

# Añadimos título y etiquetas a los ejes
plt.title('Gráfico de Líneas de Funciones Seno y Coseno')
plt.xlabel('Eje X')
plt.ylabel('Eje Y')

# Añadimos una leyenda para identificar las líneas
plt.legend()

# Añadimos una cuadrícula para facilitar la lectura
plt.grid(True)

# Mostramos el gráfico
plt.show()
print("Gráfico de líneas básico mostrado.")

# --- Sección 3: Gráfico de Dispersión (Scatter Plot - plt.scatter()) ---
print("\n--- Sección 3: Gráfico de Dispersión ---")

plt.figure(figsize=(8, 5))
plt.scatter(x_scatter, y_scatter,
            s=sizes, # Tamaño de los puntos
            c=y_scatter, # Color basado en el valor de y_scatter
            cmap='viridis', # Mapa de colores
            alpha=0.7, # Transparencia
            edgecolors='w', # Borde blanco
            label='Puntos de Datos')

plt.title('Gráfico de Dispersión de Datos Aleatorios')
plt.xlabel('Variable X')
plt.ylabel('Variable Y')
plt.colorbar(label='Valor Y') # Barra de color si se usa 'c'
plt.legend()
plt.grid(True)
plt.show()
print("Gráfico de dispersión mostrado.")

# --- Sección 4: Gráfico de Barras (Bar Chart - plt.bar()) ---
print("\n--- Sección 4: Gráfico de Barras ---")

plt.figure(figsize=(8, 5))
plt.bar(categorias, valores, color=['skyblue', 'lightcoral', 'lightgreen', 'gold', 'plum'])

plt.title('Ventas por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Valor')
plt.show()
print("Gráfico de barras mostrado.")

# --- Sección 5: Histograma (plt.hist()) ---
print("\n--- Sección 5: Histograma ---")

plt.figure(figsize=(8, 5))
plt.hist(datos_histograma, bins=15, color='teal', edgecolor='black', alpha=0.7)

plt.title('Distribución de Datos Aleatorios')
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.show()
print("Histograma mostrado.")

# --- Sección 6: Personalización Adicional ---
print("\n--- Sección 6: Personalización Adicional ---")

plt.figure(figsize=(8, 5))
plt.plot(x, y1, color='purple', label='Función Principal')
plt.title('Gráfico Personalizado con Anotaciones', fontsize=16, color='darkblue')
plt.xlabel('Tiempo (segundos)', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.legend(loc='upper right', shadow=True, fancybox=True) # Personalizar leyenda
plt.grid(axis='y', linestyle='--', alpha=0.7) # Cuadrícula solo en eje Y

# Añadir anotaciones de texto
plt.text(2, 0.8, 'Pico Máximo', fontsize=10, color='green',
         bbox=dict(facecolor='yellow', alpha=0.5, boxstyle='round,pad=0.5'))
plt.annotate('Inicio', xy=(0, 0), xytext=(1, -0.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=10, color='black')

# Guardar el gráfico en un archivo (se guarda en la misma carpeta donde ejecutas el script)
plt.savefig('mi_primer_grafico_personalizado.png', dpi=300, bbox_inches='tight')
print("Gráfico personalizado con anotaciones guardado como 'mi_primer_grafico_personalizado.png'.")
plt.show()

# --- Sección 7: Múltiples Gráficos (Subplots - plt.subplots()) ---
print("\n--- Sección 7: Múltiples Gráficos (Subplots) ---")

# Creamos una figura con 2 filas y 2 columnas de subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Gráfico de líneas en el primer subplot (arriba izquierda)
axes[0, 0].plot(x, y1, color='blue')
axes[0, 0].set_title('Seno(x)')
axes[0, 0].set_xlabel('X')
axes[0, 0].set_ylabel('Y')

# Gráfico de dispersión en el segundo subplot (arriba derecha)
axes[0, 1].scatter(x_scatter, y_scatter, color='green', alpha=0.6)
axes[0, 1].set_title('Dispersión')
axes[0, 1].set_xlabel('X')
axes[0, 1].set_ylabel('Y')

# Histograma en el tercer subplot (abajo izquierda)
axes[1, 0].hist(datos_histograma, bins=10, color='orange', edgecolor='black')
axes[1, 0].set_title('Histograma')
axes[1, 0].set_xlabel('Valor')
axes[1, 0].set_ylabel('Frecuencia')

# Gráfico de barras en el cuarto subplot (abajo derecha)
axes[1, 1].bar(categorias, valores, color='purple')
axes[1, 1].set_title('Ventas')
axes[1, 1].set_xlabel('Categoría')
axes[1, 1].set_ylabel('Valor')

# Ajustamos el espaciado entre subplots para que no se superpongan
plt.tight_layout()
plt.show()
print("Múltiples gráficos (subplots) mostrados.")

# --- Sección 8: Graficando con Pandas DataFrames ---
print("\n--- Sección 8: Graficando con Pandas DataFrames ---")

# Creamos un DataFrame de ejemplo
data = {
    'Fecha': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']),
    'Ventas': [100, 120, 90, 150, 110],
    'Gastos': [50, 60, 45, 70, 55],
    'Empleados': [10, 11, 10, 12, 11],
    'Ciudad': ['Bogotá', 'Medellín', 'Bogotá', 'Cali', 'Medellín']
}
df = pd.DataFrame(data)
print("\nDataFrame de ejemplo:")
print(df)

# Gráfico de líneas directamente desde el DataFrame
print("\nGráfico de líneas de Ventas y Gastos a lo largo del tiempo (desde DataFrame):")
df.plot(x='Fecha', y=['Ventas', 'Gastos'], kind='line', figsize=(10, 6),
        title='Ventas y Gastos Diarios', xlabel='Fecha', ylabel='Cantidad')
plt.show()

# Gráfico de barras de Empleados por Ciudad (primero agrupamos)
print("\nGráfico de barras de Empleados por Ciudad (desde DataFrame):")
df_ciudad_empleados = df.groupby('Ciudad')['Empleados'].sum().reset_index()
df_ciudad_empleados.plot(x='Ciudad', y='Empleados', kind='bar', figsize=(8, 5),
                         title='Total de Empleados por Ciudad', xlabel='Ciudad', ylabel='Número de Empleados',
                         color='lightgreen', legend=False)
plt.xticks(rotation=45) # Rotar etiquetas del eje X
plt.tight_layout()
plt.show()

# Histograma de Ventas (desde DataFrame)
print("\nHistograma de Ventas (desde DataFrame):")
df['Ventas'].plot(kind='hist', bins=5, figsize=(8, 5),
                  title='Distribución de Ventas', xlabel='Ventas', ylabel='Frecuencia',
                  color='skyblue', edgecolor='black')
plt.show()

# --- Sección 9: Usando Seaborn para Gráficos Estadísticos y Estéticos ---
print("\n--- Sección 9: Usando Seaborn para Gráficos Estadísticos y Estéticos ---")

# Seaborn viene con algunos datasets de ejemplo, usaremos 'iris'
print("\nCargando dataset 'iris' de Seaborn:")
iris = sns.load_dataset('iris')
print(iris.head())

# Gráfico de dispersión con Seaborn (más fácil de colorear por categoría)
print("\nScatter Plot con Seaborn (coloreado por especie):")
plt.figure(figsize=(10, 7))
sns.scatterplot(x='sepal_length', y='sepal_width', hue='species', data=iris,
                s=100, alpha=0.8, palette='deep') # 'hue' para colorear por categoría
plt.title('Longitud vs Ancho del Sépalo por Especie (Iris Dataset)')
plt.xlabel('Longitud del Sépalo (cm)')
plt.ylabel('Ancho del Sépalo (cm)')
plt.show()

# Histograma con Seaborn (más avanzado, permite múltiples distribuciones)
print("\nHistograma con Seaborn (distribución de longitud de pétalo por especie):")
plt.figure(figsize=(10, 7))
sns.histplot(data=iris, x='petal_length', hue='species', kde=True, palette='viridis', bins=20)
plt.title('Distribución de Longitud del Pétalo por Especie')
plt.xlabel('Longitud del Pétalo (cm)')
plt.ylabel('Conteo')
plt.show()

# Gráfico de Barras con Seaborn (para promedios, etc.)
print("\nBar Plot con Seaborn (promedio de longitud de sépalo por especie):")
plt.figure(figsize=(8, 6))
sns.barplot(x='species', y='sepal_length', data=iris, palette='pastel', ci='sd') # 'ci' muestra la desviación estándar
plt.title('Longitud Promedio del Sépalo por Especie')
plt.xlabel('Especie')
plt.ylabel('Longitud del Sépalo Promedio (cm)')
plt.show()

# Mapa de calor (Heatmap) con Seaborn (para correlaciones, matrices)
print("\nMapa de calor de correlación (Iris Dataset):")
plt.figure(figsize=(8, 7))
correlation_matrix = iris.drop('species', axis=1).corr() # Calculamos la matriz de correlación
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Matriz de Correlación del Iris Dataset')
plt.show()
print("Tutorial de graficación finalizado.")
