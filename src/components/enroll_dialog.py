import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time

@st.dialog("Enroll in Subject")
def enroll_dialog(student_id):
  st.write("Enter the subject code provided by your teacher to enroll")
  sub_code = st.text_input("Subject Code", placeholder="Eg. CS101")
  
  if st.button("Enroll Now", type="primary", width="stretch"):
    if sub_code:
      response = supabase.table("subjects").select("*").eq('subject_code', sub_code).execute()
      
      if response.data:
        subject = response.data[0]
        check = supabase.table("subjects_students").select("*").eq("subject_id", subject["subject_id"]).eq("student_id", student_id).execute()
        
        if check.data:
          st.info('You are already enrolled in the subject')
          
        else:
          enroll_student_to_subject(subject["subject_id"], student_id)
          st.success("Sucessfully Enrolled")
          time.sleep(1)
          st.rerun()
          
      else:
        st.info(f"Subject Code: {sub_code} Doesn't Exists")
      
    else:
      st.warning("Please Enter the subject code")
  