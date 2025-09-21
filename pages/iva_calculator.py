import streamlit as st

st.title("💰 Calculadora de IVA")

st.markdown("""
Calcula fácilmente el precio con IVA incluido o sin IVA según tus necesidades.
""")

# Tipo de cálculo
calculation_type = st.radio(
    "¿Qué quieres calcular?",
    ["Añadir IVA al precio", "Extraer IVA del precio"],
    horizontal=True,
)

col1, col2 = st.columns(2)

with col1:
    # Input del precio
    if calculation_type == "Añadir IVA al precio":
        price = st.number_input(
            "Precio sin IVA (€)", min_value=0.0, value=100.0, step=0.01, format="%.2f"
        )
    else:
        price = st.number_input(
            "Precio con IVA (€)", min_value=0.0, value=121.0, step=0.01, format="%.2f"
        )

with col2:
    # Selector de tipo de IVA
    iva_options = {
        "IVA General (21%)": 21,
        "IVA Reducido (10%)": 10,
        "IVA Superreducido (4%)": 4,
        "Personalizado": "custom",
    }

    iva_type = st.selectbox("Tipo de IVA", list(iva_options.keys()))

    if iva_options[iva_type] == "custom":
        iva_rate = st.number_input(
            "Porcentaje de IVA (%)",
            min_value=0.0,
            max_value=100.0,
            value=21.0,
            step=0.1,
        )
    else:
        iva_rate = iva_options[iva_type]

# Cálculos
if calculation_type == "Añadir IVA al precio":
    iva_amount = price * (iva_rate / 100)
    final_price = price + iva_amount

    st.markdown("---")
    st.subheader("📊 Resultado")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Precio sin IVA", f"{price:.2f} €")

    with col2:
        st.metric("IVA", f"{iva_amount:.2f} €", f"{iva_rate}%")

    with col3:
        st.metric("Precio final", f"{final_price:.2f} €")

else:  # Extraer IVA del precio
    price_without_iva = price / (1 + iva_rate / 100)
    iva_amount = price - price_without_iva

    st.markdown("---")
    st.subheader("📊 Resultado")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Precio con IVA", f"{price:.2f} €")

    with col2:
        st.metric("IVA", f"{iva_amount:.2f} €", f"{iva_rate}%")

    with col3:
        st.metric("Precio sin IVA", f"{price_without_iva:.2f} €")
