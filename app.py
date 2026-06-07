import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
st.title("PROYECTO FINAL")

st.set_page_config(
    page_title="Dashboard de Analítica de Talento Humano",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# --- 1. CARGA Y LIMPIEZA INICIAL DE DATOS ---
# Usamos st.cache_data para que no recargue el archivo con cada clic del usuario
@st.cache_data
def cargar_datos():
    # 1. Cargamos el dataset de forma limpia
    df = pd.read_csv("Base_proyecto_final.csv")
    
    # 2. EL PASO CRUCIAL: Eliminamos espacios ocultos en los nombres de TODAS las columnas
    df.columns = df.columns.str.strip()
    
    # 3. Ahora que las columnas están limpias, ya podemos usar 'Desc Puesto' sin errores
    df['Desc Puesto'] = df['Desc Puesto'].astype(str).str.strip()
    
    # 4. Limpiamos también la columna de sueldos (quitando espacios y convirtiendo a número)
    df['Sueldo Actual'] = pd.to_numeric(df['Sueldo Actual'], errors='coerce')
    
    return df

# Ejecutamos la función para tener nuestro dataframe listo
df = cargar_datos("Base_proyecto_final")


# --- 2. CONFIGURACIÓN DE LA BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("🎛️ Filtros de Búsqueda")

# Obtenemos la lista única de puestos ordenados alfabéticamente para el componente
lista_puestos = sorted(df['Desc Puesto'].unique())

# Creamos el componente de multi-selección en la barra lateral
puestos_seleccionados = st.sidebar.multiselect(
    "Selecciona uno o varios Puestos:",
    options=lista_puestos,
    default=[]  # Inicialmente vacío o puedes poner lista_puestos[:3] para que muestre algunos por defecto
)


# --- 3. LÓGICA DE FILTRADO Y DESPLIEGUE DE RESULTADOS ---
st.title("📊 Análisis de Sueldos por Puesto")

if puestos_seleccionados:
    # Filtrar el dataframe según la selección del usuario
    df_filtrado = df[df['Desc Puesto'].isin(puestos_seleccionados)]
    
    # Calcular el promedio de sueldo (omitiendo valores nulos si los hay)
    promedio_sueldo = df_filtrado['Sueldo Actual'].mean()
    total_empleados = len(df_filtrado)
    
    # Presentar los resultados en la pantalla principal usando métricas atractivas
    st.subheader(f"Resultados para los puestos seleccionados:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Promedio de Sueldo Actual", 
            value=f"${promedio_sueldo:,.2f}" if not np.isnan(promedio_sueldo) else "$0.00"
        )
    with col2:
        st.metric(
            label="Total de Colaboradores", 
            value=f"{total_empleados} personas"
        )
        
    # Mostrar una vista previa de los datos filtrados
    st.write("### Vista previa de los datos filtrados:")
    st.dataframe(df_filtrado[['Nombres Completos', 'Desc Puesto', 'Sueldo Actual', 'Estatus']])

else:
    # Mensaje inicial o cuando no hay nada seleccionado
    st.info("💡 Por favor, selecciona al menos un puesto en la barra lateral izquierda para calcular el promedio de sueldos.")
    
    # Opcional: Mostrar el promedio general de toda la compañía si no hay filtro activo
    promedio_general = df['Sueldo Actual'].mean()
    st.metric(label="Promedio de Sueldo General (Toda la Empresa)", value=f"${promedio_general:,.2f}")
