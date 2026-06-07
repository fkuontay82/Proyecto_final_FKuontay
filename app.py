import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
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
        df['Sueldo Actual'] = pd.to_numeric(df['Sueldo Actual'], errors='coerce')
        
    if 'Anios Antiguedad' in df.columns:
        df['Anios Antiguedad'] = pd.to_numeric(df['Anios Antiguedad'], errors='coerce')
        
    if 'Edad' in df.columns:
        df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce')
        
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

    # Definir qué dataframe usar según el filtro
    if puestos_seleccionados:
        df_analisis = df[df['Desc Puesto'].isin(puestos_seleccionados)]
        st.subheader("Resultados para los puestos seleccionados:")
    else:
        df_analisis = df
        st.info("💡 Mostrando datos generales de la empresa. Selecciona puestos en la barra lateral para segmentar.")
        st.subheader("Resultados Generales de la Empresa:")

    # 5. DESPLIEGUE DE MÉTRICAS (4 Columnas)
    col1, col2, col3, col4 = st.columns(4)
    
    # Métrica 1: Sueldo Promedio
    promedio_sueldo = df_analisis['Sueldo Actual'].mean()
    col1.metric("Sueldo Promedio", f"${promedio_sueldo:,.2f}" if not np.isnan(promedio_sueldo) else "$0.00")
    
    # Métrica 2: Conteo de Personal
    conteo = len(df_analisis)
    col2.metric("Total Colaboradores", f"{conteo} pers.")
    
    # Métrica 3: Máxima Antigüedad
    max_antiguedad = df_analisis['Anios Antiguedad'].max()
    col3.metric("Max. Antigüedad", f"{max_antiguedad:.0f} Años" if not np.isnan(max_antiguedad) else "0 Años")
    
    # Métrica 4: Edad Promedio
    promedio_edad = df_analisis['Edad'].mean()
    col4.metric("Edad Promedio", f"{promedio_edad:.1f} Años" if not np.isnan(promedio_edad) else "0 Años")
    
    st.markdown("---")

    # 6. SECCIÓN DE GRÁFICOS: ANÁLISIS DE BAJAS (GRÁFICO DE PASTEL)
    st.write("### 📉 Distribución Porcentual por Motivos de Baja")
    
    # Filtramos el dataset para quedarnos solo con los registros que son 'BAJA'
    df_bajas = df_analisis[df_analisis['Estatus'].str.upper().str.strip() == 'BAJA']
    
    if not df_bajas.empty and 'Motivo Baja' in df_bajas.columns:
        # Agrupamos por motivo y contamos cuántos casos hay
        conteo_motivos = df_bajas['Motivo Baja'].value_counts().reset_index()
        conteo_motivos.columns = ['Motivo de Baja', 'Cantidad']
        
        # Crear gráfico de pastel interactivo con Plotly Express
        fig_pastel = px.pie(
            conteo_motivos,
            values='Cantidad',
            names='Motivo de Baja',
            title="Proporción de Bajas según el Motivo",
            hole=0.3,  # Convierte el gráfico de pastel en uno de dona, que es más moderno y legible
            color_discrete_sequence=px.colors.sequential.Blues_r # Colores elegantes basados en tonos azul/cálidos
        )
        
        # Ajustes visuales para mostrar texto y porcentajes dentro del gráfico
        fig_pastel.update_traces(
            textposition='inside', 
            textinfo='percent+label'
        )
        
        fig_pastel.update_layout(
            height=450,
            margin=dict(t=50, b=20, l=20, r=20)
        )
        
        # Renderizar gráfico en Streamlit
        st.plotly_chart(fig_pastel, use_container_width=True)
    else:
        st.warning("⚠️ No se registran colaboradores con estatus de 'BAJA' para la selección actual.")

    st.markdown("---")
    
    # 7. VISUALIZACIÓN DE LA TABLA
    st.write("### Detalle de los registros analizados")
    st.dataframe(df_analisis, use_container_width=True)

except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'Base_proyecto_final.csv' en el repositorio de GitHub.")
except Exception as e:
    st.error(f"❌ Error al procesar los datos: {e}")
