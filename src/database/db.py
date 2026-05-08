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
  print("Db response:", response.data)
  if response.data:
    teacher = response.data[0]
    print("Stored hash:", teacher["password"])
    print("Match:", check_pw(password, teacher["password"]))
    if check_pw(password, teacher["password"]):
      return teacher
  return None

def get_all_students():
  response = supabase.table("students").select("*").execute()
  return response.data


  
