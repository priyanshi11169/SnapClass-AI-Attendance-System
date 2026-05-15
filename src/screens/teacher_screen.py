import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects
from src.components.dialogue_create_subject import create_subject_dialogue
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialogue

def teacher_screen():
  
  style_background_dashboard()
  style_base_layout()
  
  if "teacher_data" in st.session_state:
    teacher_dashboard()
  elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
    teacher_screen_login()
  elif st.session_state.teacher_login_type == "register":
    teacher_screen_register()
 
def login_teacher(teacher_username, teacher_pass):
  if not teacher_username or not  teacher_pass:
    return False
   
  teacher =  teacher_login(teacher_username, teacher_pass)
  if teacher:
       st.session_state.user_role = "teacher"
       st.session_state.teacher_data = teacher
       st.session_state.is_logged_in = True
       return True
    
  return False

      
def teacher_dashboard():
  col1, col2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
  with col1:
    header_dashboard()
  
  with col2:
    if st.button("Logout", type="secondary", key="loginbackbutton", shortcut="control+backspace"):
      st.session_state.is_logged_in = False
      del st.session_state.teacher_data
      st.rerun()
      
  teacher_data = st.session_state.teacher_data
  st.header(f"Welcome Back {teacher_data['username']}", text_alignment="center")
  
  if "current_teacher_tab" not in st.session_state:
    st.session_state.current_teacher_tab = "take_attendance"
  
  tab1, tab2, tab3 = st.columns(3)
  
  with tab1:
    type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
    if st.button("Take Attendance", type=type1, width="stretch"):
      st.session_state.current_teacher_tab = "take_attendance"
      st.rerun()
  
  with tab2:
    type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
    if st.button("Manage Subjects", type=type2, width="stretch"):
      st.session_state.current_teacher_tab = "manage_subjects"
      st.rerun()

  with tab3:
    type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
    if st.button("Attendance Records", type=type3, width="stretch"):
      st.session_state.current_teacher_tab = "attendance_records"
      st.rerun()
      
  st.space()
  
  if st.session_state.current_teacher_tab == "take_attendance":
    teacher_tab_take_attendance()
  if st.session_state.current_teacher_tab == "manage_subjects":
    teacher_tab_manage_subjects()
  if st.session_state.current_teacher_tab == "attendance_records":
    teacher_tab_attendance_records()
    
  st.divider()
    
  footer_dashboard()
 
def teacher_tab_take_attendance():
  st.header('Take Attendance')
  
def teacher_tab_manage_subjects():
  teacher_id = st.session_state.teacher_data["teacher_id"]
  col1, col2 = st.columns(2)
  with col1:
   st.header('Manage subjects')
  with col2:
    if st.button("Create Subject", width="stretch"):
      try:
       create_subject_dialogue(teacher_id)
      except Exception as e:
        print(f"Error: {e}")
        
  
  subjects = get_teacher_subjects(teacher_id)
  if subjects:
    for sub in subjects:
      stats = [
        ("🧑‍🎓", "Students", sub['total_students']),
        ("🕐", "Classes", sub['total_classes']),
      ]
      
      def share_btn():
        if st.button(f"Share Code: {sub['name']}", key=f"Share {sub['subject_code']}", icon=":material/share:"):
          share_subject_dialogue(sub['name'], sub['subject_code'])
          
      st.space()
      
      subject_card(
        name = sub['name'],
        code = sub['subject_code'],
        section = sub['section'],
        stats = stats,
        footer_callback = share_btn
      )
  else:
    st.info("No Subjects Found. Create one above! ")
    
  
def teacher_tab_attendance_records():
  st.header('Attendance records')


def teacher_screen_login():
  col1, col2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
  with col1:
    header_dashboard()
  
  with col2:
    if st.button("Go back to home", type="secondary", key="loginbackbutton", shortcut="control+backspace"):
      st.session_state["login_type"] = None
      st.rerun()
    
  st.header("Login using password", text_alignment="center")
  st.space()
  st.space()
  
  teacher_username = st.text_input("Enter username", placeholder="Mihika Bajaj")
  
  teacher_pass = st.text_input("Enter password", type="password", placeholder="Enter password")
  st.divider()
  
  col1, col2 = st.columns(2)
  
  with col1:
    if st.button("Login", type="secondary", shortcut="control+enter", icon=":material/passkey:", width="stretch"):
      if login_teacher(teacher_username, teacher_pass):
        st.toast("welcome back!", icon="👋")
        import time
        time.sleep(2)
        st.rerun()
      else:
        st.error("Invalid username and password combo")
        
      
  with col2:
    if st.button("Register Instead", type="primary", width="stretch", icon=":material/passkey:"):
      st.session_state.teacher_login_type = "register"
      st.rerun()
  
  footer_dashboard()
  
def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_confirm_pass):
  if not teacher_username or not teacher_name or not teacher_pass:
    return False, "ALL Fields are required!"
  if check_teacher_exists(teacher_username):
    return False, "Username is already taken"
  if teacher_pass != teacher_confirm_pass:
    return False, "Password doesn't match"
  try:
    create_teacher(teacher_username, teacher_pass, teacher_name)
    return True, "Sucessfully Created! Login Now"
  except Exception as e:
    return False, "Unexpected error"
  
def teacher_screen_register():
  col1, col2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
  with col1:
    header_dashboard()
  with col2:
    if st.button("Go back to home", type="secondary", key="loginbackbutton", shortcut="control+backspace"):
      st.session_state["login_type"] = None
      st.rerun()
  
  st.header("Register your teacher profile", text_alignment="center")
  st.space() 
  st.space()
  
  teacher_username = st.text_input("Enter username", placeholder="Mihika Bajaj")
  teacher_name = st.text_input("Enter name", placeholder="Mihika")
  
  teacher_pass = st.text_input("Enter password", type="password", placeholder="Enter password")
  teacher_confirm_pass = st.text_input("Confirm password", type="password", placeholder="Enter password")
  st.divider()
  
  col1, col2 = st.columns(2)
  
  with col1:
    if st.button("Register Now", type="secondary", shortcut="control+enter", icon=":material/passkey:", width="stretch"):
      success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_confirm_pass)
      if success:
        st.success(message)
        import time
        time.sleep(2)
        st.session_state.teacher_login_type = "login"
        st.rerun()
      else:
        st.error(message)
  with col2:
    if st.button("Login Instead", type="primary", width="stretch", icon=":material/passkey:"):
      st.session_state.teacher_login_type = "login"
      st.rerun()
  
  footer_dashboard()
  
  
  