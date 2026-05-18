import streamlit as st
from src.database.config import supabase
from src.pipelines.voice_pipelines import process_bulk_audio
from datetime import datetime
import pandas as pd
from src.components.attendance_dialog import show_attendance_results

@st.dialog('Voice Attendance')
def voice_attendance_dialog(subject_id):
  
  st.write("Record audio of students saying that I am present. Then AI will recognize the students.")
  
  audio_data = None
  audio_data = st.audio_input("Record Classroom Audio")
  
  if st.button('Analyze Audio', type="secondary", width="stretch"):
    with st.spinner("Analyzing Voice Audio.."):
      
      response = supabase.table("subjects_students").select("*, students(*)").eq("subject_id", subject_id).execute()
      enrolled_students = response.data
      
      if not enrolled_students:
        st.warning("No student has enrolled in this course!")
        return
        
      else:
        
        candidate_dict = { s["students"]["student_id"] : s["students"]["voice_embedding"]
          for s in enrolled_students if s["students"].get("voice_embedding")
        }
        
        if not candidate_dict:
          st.error("No enrolled students have voice profiles.")
          return
        
        audio_bytes = audio_data.read()
        
        detected_scores = process_bulk_audio(audio_bytes, candidate_dict)
        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        results, attendance_to_log = [], []
        
        for node in enrolled_students:
          student = node["students"]
          
          score = detected_scores.get(student['student_id'], 0.0)
          is_present = bool(score > 0)
          
          results.append({
            "Name": student["name"],
            "ID": student["student_id"],
            "Source": score if is_present else "-",
            "Status": "✅ Present" if is_present else "❌ Absent"
          })
          
          
          attendance_to_log.append({
            "student_id": student["student_id"],
            "subject_id": subject_id,
            "timestamp": current_timestamp,
            "is_present": bool(is_present)
          })
        
        st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)
        
  if st.session_state.get("voice_attendance_results"):
    df, logs = st.session_state.get("voice_attendance_results")
    show_attendance_results(df, logs)
    
    
          
          
        
        
        