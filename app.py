import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser estrictamente la PRIMERA instrucción de Streamlit)
st.set_page_config(
    page_title="Dashboard de Analítica de Talento Humano",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. BARRA LATERAL (SIDEBAR)
try:
    st.sidebar.image("Logo_Compe.png")
except:
    pass  # Si no encuentra el logo localmente, continúa sin romper la app

st.sidebar.title("Filtros Globales")
st.sidebar.markdown("---")

# 3. FUNCIÓN PARA CARGAR LOS DATOS CON CODIFICACIÓN CORRECTA
@st.cache_data
def cargar_datos():
    # Usamos encoding='latin-1' para procesar eñes, tildes y caracteres especiales de Excel
    df = pd.read_csv("Base_proyecto_final.csv", encoding="latin-1")
    
    # Limpieza fundamental: quitar espacios en blanco de los nombres de columnas
    df.columns = [col.strip() for col in df.columns]
    
    # Limpieza de datos en columnas clave
    if 'Desc Puesto' in df.columns:
        df['Desc Puesto'] = df['Desc Puesto'].astype(str).str.strip()
    
    if 'Sueldo Actual' in df.columns:
        # Convertimos a numérico por si hay símbolos de moneda o espacios en blanco
        df['Sueldo Actual'] = pd.to_numeric(df['Sueldo Actual'], errors='coerce')
        
    return df

# Ejecución segura de la carga de datos
try:
    df = cargar_datos()
      
    # 4. CUERPO PRINCIPAL
    st.title("PROYECTO FINAL: Analítica de Datos")
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
        
        # Métricas principales
        promedio = df_filtrado['Sueldo Actual'].mean()
        conteo = len(df_filtrado)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sueldo Promedio", f"${promedio:,.2f}" if not np.isnan(promedio) else "$0.00")
        with col2:
            st.metric("Colaboradores en selección", f"{conteo} personas")
        
        # Mostrar tabla filtrada
        st.write("### Detalle de empleados seleccionados")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.info("💡 Selecciona uno o más puestos en la barra lateral izquierda para comenzar el análisis.")
        
        # Mostrar una vista general del dataset si no hay filtro activo
        st.write("### Vista previa general del Dataset")
        st.dataframe(df.head(10), use_container_width=True)

except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'Base_proyecto_final.csv' en el repositorio de GitHub.")
except Exception as e:
    st.error(f"❌ Error al procesar los datos: {e}")
