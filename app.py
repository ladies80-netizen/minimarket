import os
import pandas as pd
import streamlit as st
from datetime import datetime

# Configuración de la página para celulares
st.set_page_config(page_title="Inventario Minimarket", layout="centered")

EXCEL_FILE = "inventario_minimarket.xlsx"

# Crear el Excel con sus columnas si no existe
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Fecha y Hora", "Responsable", "Nombre", "Categoría", "Marca", "Proveedor", "Costo Unitario", "Cantidad", "Precio Venta", "Stock Mínimo"])
    df.to_excel(EXCEL_FILE, index=False)

# --- CABECERA CON LOGO ---
# Busca tu imagen 1.png guardada en el mismo repositorio
if os.path.exists("1.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("1.png", use_container_width=True)

st.markdown("<h1 style='text-align: center;'>📊 INVENTARIO MINIMARKET</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Gestión de registros e ingresos automatizados</p>", unsafe_allow_html=True)

# Usamos st.session_state para controlar las limpiezas de pantalla de forma interactiva
if "form_key" not in st.session_state:
    st.session_state.form_key = 0

# --- FORMULARIO VISUAL DE INGRESO ---
with st.form(key=f"form_{st.session_state.form_key}"):
    st.subheader("👤 RESPONSABLE")
    responsable = st.text_input("Responsable:", placeholder="Nombre de quien registra...")
    
    st.subheader("📦 DETALLES DEL PRODUCTO")
    nombre = st.text_input("Nombre del Producto:", placeholder="Ej. Arroz Grano Largo")
    categoria = st.selectbox("Categoría:", ["Abarrotes", "Lácteos", "Limpieza", "Bebidas", "Otros"])
    marca = st.text_input("Marca:", placeholder="Ej. Marca Ideal")
    proveedor = st.text_input("Proveedor:", placeholder="Ej. Distribuidora Sur")
    
    st.subheader("💰 PRECIOS E INVENTARIO")
    costo = st.number_input("Costo Unitario:", min_value=0, value=0, step=1)
    cantidad = st.number_input("Cantidad:", min_value=0, value=0, step=1)
    precio = st.number_input("Precio Venta:", min_value=0, value=0, step=1)
    stock_min = st.number_input("Stock Mínimo:", min_value=0, value=5, step=1)
    
    btn_registrar = st.form_submit_button("💾 Registrar Producto")

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
        st.success("✅ ¡Producto guardado exitosamente en la base de datos!")
        st.rerun()
    else:
        st.error("⚠️ Por favor, rellena los campos obligatorios (Responsable y Nombre del Producto).")

# --- SECCIÓN DE CONTROL Y BOTONES ADICIONALES ---
st.markdown("---")
st.subheader("🛠️ PANEL DE ACCIONES Y CONTROL")

col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    if st.button("🔄 Actualizar Tabla", use_container_width=True):
        st.toast("Tabla actualizada")
        st.rerun()

with col_b2:
    if st.button("🧹 Limpiar Formulario", use_container_width=True):
        st.session_state.form_key += 1
        st.rerun()

with col_b3:
    if st.button("🗑️ Borrar Último", use_container_width=True):
        df_actual = pd.read_excel(EXCEL_FILE)
        if not df_actual.empty:
            df_actual = df_actual.drop(df_actual.index[-1])
            df_actual.to_excel(EXCEL_FILE, index=False)
            st.warning("🗑️ El último registro ingresado fue eliminado.")
            st.rerun()
        else:
            st.error("La base de datos ya está vacía.")

# --- MOSTRAR TABLA ACTUALIZADA ---
st.markdown("### 📋 VISTA PREVIA DEL EXCEL")
df_mostrar = pd.read_excel(EXCEL_FILE)
st.dataframe(df_mostrar, use_container_width=True)

# --- BOTÓN DE DESCARGA DIRECTA ---
with open(EXCEL_FILE, "rb") as file:
    st.download_button(
        label="📥 Descargar Base de Datos en Excel",
        data=file,
        file_name="inventario_minimarket.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
