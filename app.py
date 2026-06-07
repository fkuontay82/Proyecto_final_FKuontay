import streamlit as st
st.title("Franklin Kuontay Pizarro")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página de Streamlit (esto debe ir al principio)
st.set_page_config(
    page_title="Dashboard de Analítica de Talento Humano",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
