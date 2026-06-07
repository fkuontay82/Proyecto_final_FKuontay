import streamlit as st
import pandas as pd
import numpy as np

# Configuración inicial de la página
st.set_page_config(
    page_title="Dashboard de Analítica de Talento Humano",
    page_icon="📊",
    layout="wide"
)

# --- 1. CARGA Y LIMPIEZA INICIAL DE DATOS ---
@st.cache_data
def cargar_datos():
    # Cargamos el dataset
    df = pd.read_csv("Base_proyecto_final.csv")
    
    # MEDIDA DE SEGURIDAD 1: Limpiar los nombres de todas las columnas al vuelo
    df.columns = [col.strip() for col in df.columns]
    
    # MEDIDA DE SEGURIDAD 2: Limpiar los textos internos de la columna de puestos
    df['Desc Puesto'] = df['Desc Puesto'].astype(str).str.strip()
    
    # Limpiamos también la columna de sueldos
    df['Sueldo Actual'] = pd.to_numeric(df['Sueldo Actual'], errors='coerce')
    
    return df

# Ejecutamos la carga segura de datos
try:
    df = cargar_datos()
    
    # --- 2. CONFIGURACIÓN DE LA BARRA LATERAL (SIDEBAR) ---
    st.sidebar.header("🎛️ Filtros de Búsqueda")
    
    # Obtenemos la lista única de puestos ordenados
    lista_puestos = sorted(df['Desc Puesto'].unique())
    
    # Componente de selección múltiple
    puestos_seleccionados = st.sidebar.multiselect(
        "Selecciona uno o varios Puestos:",
        options=lista_puestos,
        default=[]
    )
    
    # --- 3. LÓGICA DE FILTRADO Y DESPLIEGUE DE RESULTADOS ---
    st.title("📊 Análisis de Sueldos por Puesto")
    
    if puestos_seleccionados:
        # Filtrar el dataframe según la selección del usuario
        df_filtrado = df[df['Desc Puesto'].isin(puestos_seleccionados)]
        
        # Calcular métricas dinámicas
        promedio_sueldo = df_filtrado['Sueldo Actual'].mean()
        total_empleados = len(df_filtrado)
        
        st.subheader("Resultados para los puestos seleccionados:")
        
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
            
        # Vista previa de datos
        st.write("### Vista previa de los datos filtrados:")
        st.dataframe(df_filtrado[['Nombres Completos', 'Desc Puesto', 'Sueldo Actual', 'Estatus']])
    
    else:
        st.info("💡 Por favor, selecciona al menos un puesto en la barra lateral izquierda para calcular el promedio de sueldos.")
        
        # Mostrar métrica general de la empresa por defecto
        promedio_general = df['Sueldo Actual'].mean()
        st.metric(label="Promedio de Sueldo General (Toda la Empresa)", value=f"${promedio_general:,.2f}")

except Exception as e:
    st.error(f"Ocurrió un problema inesperado al cargar el archivo: {e}")
    st.write("Columnas detectadas actualmente en el archivo:", list(pd.read_csv("Base_proyecto_final.csv").columns))
