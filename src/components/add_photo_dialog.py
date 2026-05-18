import streamlit as st
from PIL import Image

@st.dialog("Capture or Upload Photos")
def add_photo_dialog():
  
  st.write("Add Classroom Photos to scan for attendance")
  
  if "photo_tab" not in st.session_state:
    st.session_state.photo_tab = "camera"
    
  if "last_cam_photo" not in st.session_state:
    st.session_state.last_cam_photo = None
    
  if "last_uploaded_files" not in st.session_state:
    st.session_state.last_uploaded_files = []
    
    
  t1, t2 = st.columns(2)
  
  with t1:
    type_camera = "primary" if st.session_state.photo_tab == "camera" else "tertiary"
    if st.button("Camera", type=type_camera, width="stretch"):
      st.session_state.photo_tab = "camera"
    
  with t2:
    type_upload = "primary" if st.session_state.photo_tab == "upload" else "tertiary"
    if st.button("Upload Photos", type=type_upload, width="stretch"):
      st.session_state.photo_tab = "upload"
      
  if st.session_state.photo_tab == "camera":
    cam_photo = st.camera_input("Take SnapShot", key="dialog_cam")
    
    if cam_photo and cam_photo != st.session_state.last_cam_photo:
      st.session_state.attendance_images.append(Image.open(cam_photo))
      st.session_state.last_cam_photo = cam_photo
      st.toast("📸 Image Captured Successfully")
      
      
  if st.session_state.photo_tab == "upload":
    files_uploaded = st.file_uploader("Upload Photos", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    
    if files_uploaded:
      new_files = [f for f in files_uploaded if f.name not in st.session_state.last_uploaded_files]
      for file in new_files:
        st.session_state.attendance_images.append(Image.open(file))
      if new_files:
        st.session_state.last_uploaded_files += [f.name for f in new_files]
        st.toast(f" 🖼️ {len(new_files)} Photos Uploaded Successfully")
         
  st.divider()
    
  if st.button("Done", type="primary", width="stretch"):
      st.rerun()
       
  
    
    
    