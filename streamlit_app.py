import streamlit as st

# Configure page
st.set_page_config(
    page_title="Streamlit",
    page_icon="⚙️",
    layout="wide",
    # initial_sidebar_state="expanded",
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
        st.Page("pages/basic_example.py", title="Ejemplo Básico", icon="🐍"),
        st.Page("pages/forms_demo.py", title="Forms Demo", icon="📝"),
        st.Page("pages/video_camera.py", title="Efectos Webcam", icon="🎥"),
        st.Page("pages/chat_interface.py", title="Chat con IA", icon="🤖"),
    ]
)

pg.run()
