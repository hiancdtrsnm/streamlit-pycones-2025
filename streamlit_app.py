import streamlit as st

# Configure page
st.set_page_config(
    page_title="Streamlit",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# st.markdown(
#     """
#     <style>
#         .stAppDeployButton {display:none;}
#     </style>
# """,
#     unsafe_allow_html=True,
# )

# Navigation
pg = st.navigation(
    [
        st.Page("pages/welcome.py", title="Welcome", icon="📊"),
        st.Page("pages/schedule.py", title="PyConES 2025", icon="📅"),
        st.Page("pages/iva_calculator.py", title="Calculadora IVA", icon="💰"),
        st.Page("pages/user_profiles.py", title="Perfiles de Usuario", icon="👥"),
    ]
)

pg.run()
