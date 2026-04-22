import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Rentas Excel Pro", layout="centered")
ARCHIVO_EXCEL = "gestion_rentas.xlsx"

# Función para asegurar que el Excel existe con sus columnas
def inicializar_excel():
    if not os.path.exists(ARCHIVO_EXCEL):
        columnas = ['Propietario', 'Huésped', 'Propiedad', 'Precio_Noche', 
                    'Fecha_Entrada', 'Fecha_Salida', 'Transporte', 'Total']
        df = pd.DataFrame(columns=columnas)
        df.to_excel(ARCHIVO_EXCEL, index=False)

inicializar_excel()

# --- INTERFAZ ---
st.title("🏨 Registro de Rentas (Guardado en Excel)")

menu = st.sidebar.radio("Navegación", ["📝 Nueva Reserva", "📊 Ver Registros"])

if menu == "📝 Nueva Reserva":
    st.header("Formulario de Ingreso")
    
    with st.form("registro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            dueño = st.selectbox("Asignar a:", ["Jaky", "Miriam", "Pepillo"])
            huesped = st.text_input("Nombre del Huésped")
            propiedad = st.text_input("Nombre del Depto/Casa")
        
        with col2:
            precio = st.number_input("Precio por noche ($)", min_value=0, step=10)
            entrada = st.date_input("Fecha de Entrada")
            salida = st.date_input("Fecha de Salida")
        
        transporte = st.checkbox("Transporte Internacional (+$100)")
        
        # Cálculos
        noches = (salida - entrada).days
        costo_hospedaje = noches * precio
        total_final = costo_hospedaje + (100 if transporte else 0)
        
        if noches > 0:
            st.info(f"🌙 Noches: {noches} | 💰 TOTAL: ${total_final}")
        
        btn_guardar = st.form_submit_button("GUARDAR EN EXCEL")
        
        if btn_guardar:
            if huesped and propiedad and noches > 0:
                # Preparar datos para el Excel
                nueva_data = {
                    'Propietario': dueño, 'Huésped': huesped, 'Propiedad': propiedad,
                    'Precio_Noche': precio, 'Fecha_Entrada': entrada, 
                    'Fecha_Salida': salida, 'Transporte': "Sí" if transporte else "No",
                    'Total': total_final
                }
                
                # Leer, agregar y guardar
                df_actual = pd.read_excel(ARCHIVO_EXCEL)
                df_nuevo = pd.concat([df_actual, pd.DataFrame([nueva_data])], ignore_index=True)
                df_nuevo.to_excel(ARCHIVO_EXCEL, index=False)
                
                st.success(f"✅ ¡Reserva de {huesped} guardada en el Excel!")
                st.balloons()
            else:
                st.error("⚠️ Revisa los datos. Asegúrate de que las fechas sean correctas.")

elif menu == "📊 Ver Registros":
    st.header("Historial de Reservas")
    if os.path.exists(ARCHIVO_EXCEL):
        df = pd.read_excel(ARCHIVO_EXCEL)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Botón para descargar el archivo directamente
            with open(ARCHIVO_EXCEL, "rb") as file:
                st.download_button(
                    label="📥 Descargar archivo Excel",
                    data=file,
                    file_name="gestion_rentas.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.write("No hay datos registrados todavía.")

