import streamlit as st
from PIL import Image

@st.dialog("Capture or Upload Photos")
def add_photo_dialog():
  
  st.write("Add Classroom Photos to scan for attendance")
  
  if "photo_tab" not in st.session_state:
    st.session_state.photo_tab = "camera"
    
  t1, t2 = st.columns(2)
  
  with t1:
    type_camera = "primary" if st.session_state.photo_tab == "camera" else "tertiary"
    if st.button("Camera", type=type_camera, width="stretch"):
      st.session_state.photo_tab = "camera"
    
  with t2:
    type_camera = "primary" if st.session_state.photo_tab == "upload" else "tertiary"
    if st.button("Upload Photos", type=type_camera, width="stretch"):
      st.session_state.photo_tab = "upload"
      
  if st.session_state.photo_tab == "camera":
    cam_photo = st.camera_input("Take SnapShot", key="dialog_cam")
    
    if cam_photo:
      st.session_state.attendance_images.append(Image.open(cam_photo))
      st.toast("Image Captured Sucessfully")
      st.rerun()
      
  if st.session_state.photo_tab == "upload":
    files_uploaded = st.file_uploader("Upload Photos", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    
    if files_uploaded:
      for file in files_uploaded:
        st.session_state.attendance_images.append(Image.open(file))
        st.toast("Photos Uploaded Sucessfully")
        st.rerun()
    
  st.divider()  
  if st.button("Done", type="primary", width="stretch"):
      st.rerun()
       
  
    
    
    