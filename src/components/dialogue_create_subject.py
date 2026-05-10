import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialogue(teacher_id):
  st.write("Enter the details of new subject")
  sub_code = st.text_input("Subject Code", placeholder="CS101")
  sub_name = st.text_input("Subject Name", placeholder="Introduction To Computer Science")
  section = st.text_input("Section", placeholder="A")
  if st.button("Create Subject Now", type="primary", width="stretch"):
    if sub_code and sub_name and section:
      try:
        create_subject(sub_code, sub_name, section, teacher_id)
        st.toast("Subject Created Successfully")
        st.rerun()
      except Exception as e:
        st.error(f"Error {str(e)}")
    else:
      st.warning("Please fill the fields")
     
    