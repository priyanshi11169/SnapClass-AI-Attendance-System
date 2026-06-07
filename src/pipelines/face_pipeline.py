import streamlit as st
import numpy as np
import face_recognition_models 
from sklearn.svm import SVC
import dlib
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
  
  detector = dlib.get_frontal_face_detector()
  
  sp = dlib.shape_predictor(
    face_recognition_models.pose_predictor_model_location()
  )
  
  face_rec = dlib.face_recognition_model_v1(
    face_recognition_models.face_recognition_model_location()
  )
  
  return detector, sp, face_rec

@st.cache_resource
def get_face_embedding(image_np):
  detector, sp, resnec = load_dlib_models() 
  faces = detector(image_np, 1)
  
  embeddings = []
  
  for face in faces:
    shape = sp(image_np, face)
    face_descriptor = resnec.compute_face_descriptor(image_np, shape, 1)
    embeddings.append(np.array(face_descriptor))
    
  return embeddings


@st.cache_resource
def get_trained_model():
  student_db = get_all_students()
  
  X = []
  y = []
  
  if not student_db:
    return None
  
  for student in student_db:
    embedding = student.get("face_embedding")
    if embedding:
      X.append(np.array(embedding))
      y.append(student.get("student_id"))
      
  if len(X) == 0:
    return 0
  
  clf = SVC(kernel='linear', probability=True, class_weight="balanced")   
  try:
    clf.fit(X, y)  
  except Exception as e:
    print("Error: ",e)
  
  return {"clf":clf, "X":X, "y":y}

 
def train_classifier():
  st.cache_resource.clear()
  model = get_trained_model()
  return bool(model)

def predict_attendance(class_image_np):
  embeddings = get_face_embedding(class_image_np)
  
  detected_student = {}
  
  model_data = get_trained_model()
  
  if not model_data:
    return detected_student, [], len(embeddings)

  clf = model_data["clf"]
  X_train = model_data["X"]
  y_train = model_data["y"]
  
  all_students = sorted(list(set(y_train)))
  
  
  for embedding in embeddings:
    if len(all_students) >= 2:
      predicted_id = clf.predict([embedding])[0]
      
    else:
      predicted_id = int(all_students[0])
      
    student_embedding = X_train[y_train.index(predicted_id)]
    
    best_match_score = np.linalg.norm(student_embedding - embedding)
    resemblance_score = 0.4
    
    if best_match_score <= resemblance_score:
      detected_student[predicted_id] = "True"
  
  return detected_student, all_students, len(embeddings)