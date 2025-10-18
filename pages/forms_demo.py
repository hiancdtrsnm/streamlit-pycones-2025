import streamlit as st
import time
import pandas as pd
from datetime import datetime

st.title("📝 Forms Demo")

# Initialize session state
if 'form_submissions' not in st.session_state:
    st.session_state.form_submissions = []
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'performance_data' not in st.session_state:
    st.session_state.performance_data = {'with_form': [], 'without_form': []}


st.header("Basic Forms Demo")

col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ Without Form (Constant Reruns)")
    st.markdown("*Every input change triggers a rerun*")
    
    # Counter to show reruns
    st.session_state.counter += 1
    st.info(f"🔄 Page rerun count: {st.session_state.counter}")
    
    # Regular widgets (no form)
    name_no_form = st.text_input("Your name", key="name_no_form")
    age_no_form = st.number_input("Your age", min_value=0, max_value=120, key="age_no_form")
    favorite_color_no_form = st.selectbox(
        "Favorite color", 
        ["Red", "Blue", "Green", "Yellow"], 
        key="color_no_form"
    )
    
    if name_no_form:
        st.success(f"Hello {name_no_form}! You are {age_no_form} years old and love {favorite_color_no_form.lower()}.")
    
    with col2:
        st.subheader("✅ With Form (Batched Input)")
        st.markdown("*Changes only applied when form is submitted*")
        
        # Form widgets
        with st.form("basic_form", clear_on_submit=False):
            name_form = st.text_input("Your name", key="name_form")
            age_form = st.number_input("Your age", min_value=0, max_value=120, key="age_form")
            favorite_color_form = st.selectbox(
                "Favorite color", 
                ["Red", "Blue", "Green", "Yellow"], 
                key="color_form"
            )
            submit_basic = st.form_submit_button("Submit")
        
        if submit_basic and name_form:
            st.success(f"Hello {name_form}! You are {age_form} years old and love {favorite_color_form.lower()}.")
            st.balloons()
