import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Calculadora Estadística", layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
        .stTextInput, .stButton>button {
            border-radius: 10px;
        }
        .stApp {
            background-color: #f4f4f4;
        }
        h1 {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("📊 Calculadora Estadística con Tabla de Frecuencias")

# Entrada de datos
numeros = st.text_area("Ingrese los números separados por coma", "10,20,30,40,50,50,20,30,40,50,60,70,80,90,100")

if st.button("Calcular Estadísticas"):
    try:
        # Convertir datos a lista de números
        lista_numeros = list(map(float, numeros.split(",")))
        n = len(lista_numeros)
        df = pd.DataFrame(lista_numeros, columns=["Valores"])

        # Estadísticas básicas
        media = round(df["Valores"].mean(), 2)
        mediana = round(df["Valores"].median(), 2)
        moda = df["Valores"].mode().tolist()

        # Parámetros para intervalos de clase
        k = int(1 + 3.322 * np.log10(n))  # Regla de Sturges
        min_val = min(lista_numeros)
        max_val = max(lista_numeros)
        intervalo = round((max_val - min_val) / k)  # Tamaño del intervalo

        # Creación de intervalos
        bins = np.arange(min_val, max_val + intervalo, intervalo)
        df["Intervalo"] = pd.cut(df["Valores"], bins=bins, right=False)

        # Tabla de frecuencias
        tabla_frec = df["Intervalo"].value_counts().sort_index().reset_index()
        tabla_frec.columns = ["Intervalo", "Frecuencia Absoluta"]
        tabla_frec["Límite Inferior"] = bins[:-1]
        tabla_frec["Límite Superior"] = bins[1:]
        tabla_frec["Marca de Clase"] = (tabla_frec["Límite Inferior"] + tabla_frec["Límite Superior"]) / 2

        # Calcular frecuencia acumulada absoluta
        tabla_frec["Frecuencia Acumulada Absoluta"] = tabla_frec["Frecuencia Absoluta"].cumsum()

        # Calcular frecuencia relativa
        tabla_frec["Frecuencia Relativa"] = tabla_frec["Frecuencia Absoluta"] / n
        tabla_frec["Frecuencia Acumulada Relativa"] = tabla_frec["Frecuencia Relativa"].cumsum()

        # Redondear valores
        tabla_frec = tabla_frec.round(4)

        # Mostrar estadísticas
        st.subheader("📈 Resultados Generales")
        st.write(f"📌 **Media:** {media}")
        st.write(f"📌 **Mediana:** {mediana}")
        st.write(f"📌 **Moda:** {', '.join(map(str, moda))}")

        # Mostrar tabla de frecuencias
        st.subheader("📊 Tabla de Frecuencias")
        st.write(tabla_frec)

    except ValueError:
        st.error("❌ Error: Asegúrese de ingresar solo números separados por comas.")
