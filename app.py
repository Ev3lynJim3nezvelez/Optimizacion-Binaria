import streamlit as st
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

st.set_page_config(page_title="Optimización de Proyectos", page_icon="📊", layout="wide")

st.title("📊 Optimizador Binario de Proyectos (Knapsack Problem)")
st.markdown("Esta aplicación permite modificar dinámicamente los costos y beneficios de cada proyecto para encontrar la selección óptima que maximiza el beneficio total sin superar la capacidad permitida.")

# --- BARRA LATERAL: ENTRADA DE DATOS ---
st.sidebar.header("⚙️ Configuración del Problema")

# Capacidad Máxima
capacidad = st.sidebar.number_input("Capacidad Máxima (Límite)", min_value=1.0, value=9.0, step=0.5)

st.sidebar.subheader("📈 Beneficios de los Proyectos")
b1 = st.sidebar.number_input("Beneficio Proyecto 1", min_value=0.0, value=14.0, step=0.5)
b2 = st.sidebar.number_input("Beneficio Proyecto 2", min_value=0.0, value=5.0, step=0.5)
b3 = st.sidebar.number_input("Beneficio Proyecto 3", min_value=0.0, value=7.0, step=0.5)
b4 = st.sidebar.number_input("Beneficio Proyecto 4", min_value=0.0, value=3.0, step=0.5)

st.sidebar.subheader("💰 Costos de los Proyectos")
c1 = st.sidebar.number_input("Costo Proyecto 1", min_value=0.1, value=8.0, step=0.5)
c2 = st.sidebar.number_input("Costo Proyecto 2", min_value=0.1, value=3.0, step=0.5)
c3 = st.sidebar.number_input("Costo Proyecto 3", min_value=0.1, value=4.0, step=0.5)
c4 = st.sidebar.number_input("Costo Proyecto 4", min_value=0.1, value=2.0, step=0.5)

# --- PROCESAMIENTO Y OPTIMIZACIÓN ---
# Construir vectores para SciPy
beneficios = np.array([b1, b2, b3, b4])
costos = np.array([c1, c2, c3, c4])

# SciPy minimiza, por ende multiplicamos beneficios por -1 para maximizar
c_opt = -beneficios
bounds = Bounds(0, 1) # Variable binaria (0 o 1)
A = np.array([costos])
ub = np.array([capacidad])
lb = np.array([-np.inf])
constraints = LinearConstraint(A, lb, ub)
integrality = np.ones_like(c_opt) # 1 denota tipo entero

res = milp(c=c_opt, bounds=bounds, constraints=constraints, integrality=integrality)

# --- PRESENTACIÓN DE RESULTADOS ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Parámetros actuales")
    tabla_datos = {
        "Proyecto": ["Proyecto 1", "Proyecto 2", "Proyecto 3", "Proyecto 4"],
        "Beneficio": [b1, b2, b3, b4],
        "Costo": [c1, c2, c3, c4]
    }
    st.table(tabla_datos)
    st.metric(label="Capacidad Límite Disponible", value=f"{capacidad}")

with col2:
    st.subheader("🎯 Solución Óptima")
    if res.success:
        valores_optimos = [int(round(val)) for val in res.x]
        beneficio_total = sum(beneficios[i] * valores_optimos[i] for i in range(4))
        costo_total = sum(costos[i] * valores_optimos[i] for i in range(4))
        
        st.success("¡Solución óptima encontrada!")
        
        # Mostrar métricas clave
        m1, m2 = st.columns(2)
        m1.metric(label="Beneficio Total Maximizado", value=f"{beneficio_total}")
        m2.metric(label="Costo Total Utilizado", value=f"{costo_total} / {capacidad}")
        
        st.write("**Estado de selección de proyectos:**")
        for i, seleccionado in enumerate(valores_optimos):
            estado = "✅ Seleccionado" if seleccionado == 1 else "❌ No Seleccionado"
            st.write(f"* **Proyecto {i+1}**: {estado} (Beneficio: {beneficios[i]}, Costo: {costos[i]})")
    else:
        st.error(f"No se pudo encontrar una solución óptima: {res.message}")
