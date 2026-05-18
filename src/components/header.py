import streamlit as st

def header_home():
  #st.image("https://i.ibb.co/YTYGn5qV/logo.png", width=120)
  
  st.markdown("""
              <div style = "display:flex;
              flex-direction:column; align-items:center;" >
                <img src="https://i.ibb.co/YTYGn5qV/logo.png" height="120px" />
                
                <h1 style="color:#E0E3FF; text-align:center; ">Snap<br/>Class</h1>
                
              </div>
              """, unsafe_allow_html=True)
  

def header_dashboard():
  logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
  st.markdown(f"""
              <div style="display:flex;  justify-content:center; gap:10px; text-align:center; ">
                <img src={logo_url} style="height:85px;"/>
                <h2 style="color:#5865F2; text-align:left; ">Snap<br/>Class</h2>
              </div>
              """, unsafe_allow_html=True)