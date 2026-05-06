import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import background_style_layout, style_base_layout


def home_screen():
  
  background_style_layout()
  style_base_layout()
  header_home()
  
  st.space()
  st.space()
  col1, col2 = st.columns(2)
  
  with col1:
    st.header("I'm Student")
    st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
    if st.button("Student Portal", type="primary",icon=":material/arrow_outward:"):
      st.session_state["login_type"] = "student"
      st.rerun()
    
  with col2:
    st.header("I'm Teacher")
    st.image("https://i.ibb.co/CsmQQV6X/mascot-student.png", width=145)
    if st.button("Teacher Portal", type="primary",icon=":material/arrow_outward:"):
      st.session_state["login_type"] = "teacher"
      st.rerun()
      
  
      
  footer_home()
      
