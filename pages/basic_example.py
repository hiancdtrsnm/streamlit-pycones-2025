import streamlit as st

st.title("Ejemplo básico de Streamlit 🐍")

nombre = st.text_input('Dime tu nombre')
st.write("Hola,", nombre or "mundo")

st.code("""
import streamlit as st

st.title("Ejemplo básico de Streamlit 🐍")

nombre = st.text_input('Dime tu nombre')
st.write("Hola,", nombre or "mundo")
""")