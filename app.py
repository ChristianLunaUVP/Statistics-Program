import streamlit as st
import pandas as pd
import numpy as np

# Configurar la página con diseño minimalista
st.set_page_config(page_title="Calculadora Estadística", layout="wide")

# 💡 **CSS para estilos personalizados**
st.markdown("""
    <style>
        .stApp {
            background-color: #FAFAFA;
            font-family: 'Roboto', sans-serif;
        }

        h1, h2, h3 {
            color: #B71C1C;
            text-align: center;
        }

        .stButton > button {
            background-color: #D32F2F;
            color: white;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 16px;
            border: none;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            transition: 0.3s ease-in-out;
        }

        .stButton > button:hover {
            background-color: #B71C1C;
        }

        .stTextArea textarea {
            border: 2px solid #D32F2F;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }

        .number-box {
            display: inline-block;
            background-color: #D32F2F;
            color: white;
            padding: 8px 12px;
            margin: 4px;
            border-radius: 6px;
            font-size: 14px;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
        }

        .dataframe {
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            border: 2px solid #D32F2F;
        }

        .dataframe th, .dataframe td {
            padding: 12px;
            text-align: center;
            border: 1px solid #D32F2F;
        }

        .dataframe th {
            background-color: #D32F2F;
            color: white;
            font-size: 16px;
            font-weight: bold;
        }

        .dataframe td {
            font-size: 14px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("📊 Calculadora Estadística con Decimales")

# Entrada de datos (ahora separados por espacios)
numeros = st.text_area("Ingrese los números separados por espacios:")

if st.button("Calcular Estadísticas"):
    try:
        # Convertir datos a lista de números flotantes y ordenarlos
        lista_numeros = sorted(map(float, numeros.strip().split()))
        n = len(lista_numeros)

        if n < 2:
            st.error("❌ Error: Debes ingresar al menos dos valores.")
        else:
            df = pd.DataFrame(lista_numeros, columns=["Valores"])

            # 📌 **Cálculo de Parámetros**
            A = round(max(lista_numeros) - min(lista_numeros), 2)  # Rango
            K = round(1 + 3.322 * np.log10(n), 2)  # Número de intervalos con 2 decimales
            C = round(A / K, 2)  # Tamaño del intervalo

            # 📢 **Mostrar cálculos**
            st.subheader("📌 Cálculos de Parámetros")
            st.write(f"🔹 **A (Rango de los datos):** {A}")
            st.write(f"🔹 **K (Número de Intervalos):** {K}")
            st.write(f"🔹 **C (Tamaño del Intervalo):** {C}")

            # 📌 **Mostrar números ordenados**
            st.subheader("📊 Números Ordenados")
            st.write(f"📌 **Cantidad total de datos ingresados:** {n}")
            numbers_html = " ".join([f'<span class="number-box">{num}</span>' for num in lista_numeros])
            st.markdown(f'<div style="text-align: center;">{numbers_html}</div>', unsafe_allow_html=True)

            # 📌 **Creación de Intervalos con Decimales**
            bins = np.linspace(min(lista_numeros), max(lista_numeros) + C, int(np.ceil(K)) + 1)  # Se usa linspace para intervalos con decimales
            bins[-1] += 0.01  # Asegurar que el número máximo sea incluido en el último intervalo
            df["Intervalo"] = pd.cut(df["Valores"], bins=bins, right=False)  # Se usa right=False para [a - b)

            # 📌 **Tabla de Frecuencias**
            tabla_frec = df["Intervalo"].value_counts().sort_index().reset_index()
            tabla_frec.columns = ["Intervalos de Clase", "fi"]

            # ✅ **Formatear Intervalos**
            tabla_frec["Intervalos de Clase"] = tabla_frec["Intervalos de Clase"].apply(lambda x: f"[{x.left:.2f} - {x.right:.2f})")

            # 📌 **Cálculo de la Marca de Clase (x̄)**
            tabla_frec["x̄"] = [(interval.left + interval.right) / 2 for interval in pd.cut(lista_numeros, bins=bins, right=False).categories]

            # 📌 **Cálculo de Frecuencias**
            tabla_frec["Fi"] = tabla_frec["fi"].cumsum()  
            tabla_frec["hi"] = tabla_frec["fi"] / n  
            tabla_frec["Hi"] = tabla_frec["hi"].cumsum()  

            # 📌 **Asegurar que Fi sea igual a la cantidad de datos ingresados**
            tabla_frec.loc[tabla_frec.index[-1], "Fi"] = n
            tabla_frec.loc[tabla_frec.index[-1], "Hi"] = 1.00  

            # 📌 **Reordenar columnas**
            tabla_frec = tabla_frec[["Intervalos de Clase", "x̄", "fi", "Fi", "hi", "Hi"]]
            tabla_frec = tabla_frec.round(2)

            # 📌 **Mostrar tabla de frecuencias con diseño mejorado**
            st.subheader("📊 Tabla de Frecuencias")
            st.markdown(tabla_frec.to_html(index=False, escape=False), unsafe_allow_html=True)

    except ValueError:
        st.error("❌ Error: Asegúrese de ingresar solo números separados por espacios y sin caracteres especiales.")
