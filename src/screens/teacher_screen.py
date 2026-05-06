import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard, background_style_layout


def teacher_screen():
  
  if "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
    teacher_screen_login()
  elif st.session_state["teacher_login_type"] == "register":
    teacher_screen_register()
    
  
def teacher_screen_login():
   
   
  style_base_layout()
  style_background_dashboard()
  
  col1, col2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
  
  with col1:
    header_dashboard()
    
  with col2:
    if st.button("Go Back To Home", shortcut="control+backspace", width="stretch"):
      st.session_state["login_type"] = None
      st.rerun()

  st.header("Login Using Password", text_alignment="center")
  
  st.space()
  
  username = st.text_input("Enter Username", placeholder="@Harry")
  
  password = st.text_input("Enter Password", type="password", placeholder="Enter Your Password")
  
  
  st.divider()
  
  col1, col2 = st.columns(2)
  
  with col1:
    st.button("Login", shortcut="control+Enter", width="stretch", type="primary")
  with col2:
    if st.button("Register Instead", width="stretch"):
      st.session_state["teacher_login_type"] = "register"
      st.rerun()
    
  footer_dashboard()
  
  

def teacher_screen_register():
   
  style_base_layout()
  style_background_dashboard()
  
  col1, col2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
  
  with col1:
    header_dashboard()
    
  with col2:
    if st.button("Go Back To Home", shortcut="control+backspace", width="stretch"):
      st.session_state["login_type"] = None
      st.rerun()

  st.header("Register Your Teacher Profile")
  
  st.space()
  
  username = st.text_input("Enter Username", placeholder="Harry")
  
  name = st.text_input("Enter Name", placeholder="Harry Potter")
  
  password = st.text_input("Enter Password", type="password", placeholder="Enter your Password")
  
  conf_pass = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
  
  st.divider()
  
  col1, col2 = st.columns(2)
  
  with col1:
    st.button("Register Now", shortcut="control+Enter", width="stretch", type="primary")
  with col2:
    if st.button("Login Instead", width="stretch"):
      st.session_state["teacher_login_type"] = "login"
      st.rerun()
    
  footer_dashboard()
  
  

  
  