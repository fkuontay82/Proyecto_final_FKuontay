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
# 2. BARRA LATERAL (SIDEBAR)
st.sidebar.image("Logo_Compe.png")
st.sidebar.title("Filtros Globales")

# 3. FUNCIÓN PARA CARGAR LOS DATOS
@st.cache_data
def cargar_datos():
    # Cargamos el archivo específico
    df = pd.read_csv("Base_proyecto_final.csv")
    
    # Limpieza fundamental: quitar espacios en blanco de los nombres de columnas
    df.columns = [col.strip() for col in df.columns]
    
    # Limpieza de datos en columnas clave
    if 'Desc Puesto' in df.columns:
        df['Desc Puesto'] = df['Desc Puesto'].astype(str).str.strip()
    
    if 'Sueldo Actual' in df.columns:
        # Convertimos a numérico por si hay símbolos de moneda o espacios
        df['Sueldo Actual'] = pd.to_numeric(df['Sueldo Actual'], errors='coerce')
        
    return df

# Ejecución de la carga
try:
    df = cargar_datos()
      
    # 4. CUERPO PRINCIPAL
    st.title("🚀 PROYECTO FINAL: Analítica de Datos")
    st.markdown("---")
    
    # Lógica de la Barra Lateral para filtrar puestos
    lista_puestos = sorted(df['Desc Puesto'].unique())
    puestos_seleccionados = st.sidebar.multiselect(
        "Selecciona Puestos para el análisis:",
        options=lista_puestos
    )

    # 5. ANÁLISIS DINÁMICO
    if puestos_seleccionados:
        df_filtrado = df[df['Desc Puesto'].isin(puestos_seleccionados)]
        
        # Métricas
        promedio = df_filtrado['Sueldo Actual'].mean()
        conteo = len(df_filtrado)
        
        col1, col2 = st.columns(2)
        col1.metric("Sueldo Promedio", f"${promedio:,.2f}")
        col2.metric("Colaboradores en selección", conteo)
        
        # Mostrar tabla
        st.write("### Detalle de empleados seleccionados")
        st.dataframe(df_filtrado)
    else:
        st.info("Selecciona uno o más puestos en la barra lateral para comenzar el análisis.")
        
        # Mostrar una vista general del dataset si no hay filtro
        st.write("### Vista previa general del Dataset")
        st.dataframe(df.head(10))

except FileNotFoundError:
    st.error("No se encontró el archivo 'Base_proyecto_final.csv'. Asegúrate de que el nombre sea exacto y esté en la raíz de tu repositorio.")
except Exception as e:
    st.error(f"Error al procesar los datos: {e}")
