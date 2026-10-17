import os
import pandas as pd
import streamlit as st
from datetime import datetime

# Configuración de la página para celulares
st.set_page_config(page_title="Inventario Minimarket", layout="centered")

st.title("📊 INVENTARIO PRODUCTOS MINIMARKET")
st.markdown("Formulario de registro de ingresos y egresos con base de datos en Excel.")

EXCEL_FILE = "inventario_minimarket.xlsx"

# Crear el Excel con sus columnas si no existe
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Fecha y Hora", "Responsable", "Nombre", "Categoría", "Marca", "Proveedor", "Costo Unitario", "Cantidad", "Precio Venta", "Stock Mínimo"])
    df.to_excel(EXCEL_FILE, index=False)

# --- FORMULARIO VISUAL (Se adapta automáticamente al celular) ---
with gr.form("registro_prod", clear_on_submit=True) if 'gr' in globals() else st.form("registro_prod", clear_on_submit=True):
    st.subheader("👤 RESPONSABLE")
    responsable = st.text_input("Responsable:", placeholder="Nombre de quien registra...")
    
    st.subheader("📦 DETALLES DEL PRODUCTO")
    nombre = st.text_input("Nombre del Producto:", placeholder="Ej. Arroz Grano Largo")
    categoria = st.selectbox("Categoría:", ["Abarrotes", "Lácteos", "Limpieza", "Otros"])
    marca = st.text_input("Marca:", placeholder="Ej. Marca Ideal")
    proveedor = st.text_input("Proveedor:", placeholder="Ej. Distribuidora Sur")
    
    st.subheader("💰 PRECIOS E INVENTARIO")
    costo = st.number_input("Costo Unitario:", min_value=0, value=0, step=1)
    cantidad = st.number_input("Cantidad:", min_value=0, value=0, step=1)
    precio = st.number_input("Precio Venta:", min_value=0, value=0, step=1)
    stock_min = st.number_input("Stock Mínimo:", min_value=0, value=5, step=1)
    
    btn_registrar = st.form_submit_button("Registrar Producto")

# --- LÓGICA DEL BOTÓN REGISTRAR ---
if btn_registrar:
    if responsable and nombre:
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuevo_registro = {
            "Fecha y Hora": fecha_actual, "Responsable": responsable, "Nombre": nombre,
            "Categoría": categoria, "Marca": marca, "Proveedor": proveedor,
            "Costo Unitario": costo, "Cantidad": cantidad, "Precio Venta": precio, "Stock Mínimo": stock_min
        }
        df_actual = pd.read_excel(EXCEL_FILE)
        df_actual = pd.concat([df_actual, pd.DataFrame([nuevo_registro])], ignore_index=False)
        df_actual.to_excel(EXCEL_FILE, index=False)
        st.success("✅ ¡Producto registrado con éxito!")
    else:
        st.error("⚠️ Por favor, llena los campos obligatorios (Responsable y Nombre).")

# --- TABLA Y DESCARGA ---
st.subheader("📋 TABLA DE INVENTARIO ACTUAL")
df_mostrar = pd.read_excel(EXCEL_FILE)
st.dataframe(df_mostrar)

# Botón para que tu cliente baje el archivo Excel a su celular al instante
with open(EXCEL_FILE, "rb") as file:
    st.download_button(
        label="📥 Descargar Base de Datos en Excel",
        data=file,
        file_name="inventario_minimarket.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
