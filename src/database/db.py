from src.database.config import supabase
import bcrypt

def hash_password(password):
  return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
   
def check_teacher_exists(username):
  response = supabase.table("teachers").select("username").eq("username", username).execute()
  return len(response.data) > 0

def create_teacher(username, password, name):
  data = {"username": username, "password": hash_password(password), "name": name}
  response = supabase.table("teachers").insert(data).execute()
  return response.data

def check_pw(password, hashed_pswrd):
  return bcrypt.checkpw(password.encode(), hashed_pswrd.encode())

def teacher_login(username, password):
  response = supabase.table("teachers").select("*").eq("username", username).execute()
  if response.data:
    teacher = response.data[0]
    if check_pw(password, teacher["password"]):
      return teacher
  return None

def get_all_students():
  response = supabase.table("students").select("*").execute()
  return response.data

def create_student(name, face_embedding=None, voice_embedding=None):
  data = {'name':name, "face_embedding": face_embedding, "voice_embedding":voice_embedding}
  response = supabase.table('students').insert(data).execute()
  return response.data

def create_subject(subject_code, name, section, teacher_id):
  data = {"subject_code": subject_code, "name":name, "section":section, "teacher_id":teacher_id}
  response = supabase.table("subjects").insert(data).execute()
  return response.data

def get_teacher_subjects(teacher_id):
  response = supabase.table('subjects').select("*, subjects_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
  
  subjects = response.data
  
  for sub in subjects:
    sub["total_students"] = sub.get("subjects_students", [{}])[0].get("count", 0) if sub.get("subjects_students") else 0
    attendance = sub.get("attendance_logs", [])
    
    unique_sessions = len(set(log["timestamp"] for log in attendance))
    
    sub["total_classes"] = unique_sessions
    
    sub.pop("subjects_students", None)
    sub.pop("attendance_logs", None)
    
  return subjects

def enroll_student_to_subject(subject_id, student_id):
  data = {"subject_id" : subject_id, "student_id" : student_id}
  response = supabase.table("subjects_students").insert(data).execute()
  
  return response.data

def get_student_subjects(student_id):
  response = supabase.table("subjects_students").select("*, subjects(*)").eq("student_id", student_id).execute()
  
  return response.data
  
def get_student_attendence(student_id):
  response = supabase.table("attendance_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
  
  return response.data

def unenroll_student_from_subject(subject_id, student_id):
  response = supabase.table("subjects_students").delete().eq("subject_id", subject_id).eq("student_id", student_id).execute()
  
  return response.data
  
def create_attendance(logs):
  response = supabase.table("attendance_logs").insert(logs).execute()
  return response.data
