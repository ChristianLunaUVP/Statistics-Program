import streamlit as st
import pandas as pd
import numpy as np

# Configurar la página con diseño minimalista
st.set_page_config(page_title="Calculadora Estadística", layout="wide")

# 💡 **CSS para estilos personalizados con Material Design y tonos rojos**
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

# Título con animación
st.title("📊 Calculadora Estadística con Tabla de Frecuencias")

# Entrada de datos (ahora separados por espacios)
numeros = st.text_area("Ingrese los números separados por espacios:", 
                       "1 3 3 4 10 11 15 16 17 17 19 21 22 23 25 26 27 29 30 33 34 36 36 36 42 42 45 47 48 50 54 54 58 61 63 65 70 73")

if st.button("Calcular Estadísticas"):
    try:
        # Convertir datos a lista de números, eliminando espacios extra
        lista_numeros = sorted(map(float, numeros.strip().split()))
        n = len(lista_numeros)

        if n < 2:
            st.error("❌ Error: Debes ingresar al menos dos valores.")
        else:
            df = pd.DataFrame(lista_numeros, columns=["Valores"])

            # 📌 **Cálculo de K, C y A sin redondear K**
            A = max(lista_numeros) - min(lista_numeros)  # Rango
            K = 1 + 3.322 * np.log10(n)  # Número de intervalos (sin redondeo)
            C = A / K  # Tamaño del intervalo

            # 📢 **Mostrar cálculos con 2 decimales**
            st.subheader("📌 Cálculos de Parámetros")
            st.write(f"🔹 **A (Rango de los datos):** {round(A, 2)}")
            st.write(f"🔹 **K (Número de Intervalos):** {round(K, 2)} (Regla de Sturges, sin redondeo)")
            st.write(f"🔹 **C (Tamaño del Intervalo):** {round(C, 2)}")

            # 📌 **Mostrar números ordenados con diseño mejorado**
            st.subheader("📊 Números Ordenados")
            st.write(f"📌 **Cantidad total de datos ingresados:** {n}")
            numbers_html = " ".join([f'<span class="number-box">{int(num)}</span>' for num in lista_numeros])
            st.markdown(f'<div style="text-align: center;">{numbers_html}</div>', unsafe_allow_html=True)

            # 📌 **Creación de Intervalos con [a - b)**
            K_int = int(np.ceil(K))  
            bins = np.arange(min(lista_numeros), max(lista_numeros) + C, C)  
            bins[-1] += 0.1  
            df["Intervalo"] = pd.cut(df["Valores"], bins=bins, right=False)  

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
