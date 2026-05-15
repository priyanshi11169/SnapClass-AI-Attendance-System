import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time

@st.dialog("Ouick Enrollement")
def auto_enroll_dialog(subject_code):
  response = supabase.table("subjects").select("*").eq("subject_code", subject_code).execute()
  
  if response.data:
    subject = response.data[0]
    student_id = st.session_state.student_data["student_id"]
    
    check = supabase.table("subjects_students").select("*, subjects(*)").eq("subject_id", subject["subject_id"]).eq("student_id", student_id).execute()
    if check.data:
      st.info(f"You are already enrolled in {subject['name']}!")
      if st.button("Got it"):
        st.query_params.clear()
        st.rerun()
      
    else:
      st.write(f"Would you like to enroll in {subject['name']}?")
      col1, col2 = st.columns(2)
      
      with col1:
        if st.button("No Thanks", type="secondary", width="stretch"):
          st.query_params.clear()
          st.rerun()
      with col2:
        if st.button(f"Yes enroll now!", type="primary", width="stretch"):
          enroll_student_to_subject(subject["subject_id"], student_id)
          st.success("Enrolled sucessfully")
          st.query_params.clear()
          time.sleep(2)
          st.rerun()
  else:
    st.error("Subject Code Not Found!")
    if st.button("Close"):
      st.query_params.clear()
      st.rerun()
    return 
      
      
    
    
    