from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
  return VoiceEncoder()

def get_voice_embedding(audio_bytes):
  try:
    encoder = load_voice_encoder()
    
    audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
    wav = preprocess_wav(audio)
    embedding = encoder.embed_utterance(wav)
    return embedding.tolist()
  
  except Exception as e:
    st.error("Voice recog error")
    return None
  
def identify_speaker(new_embedding, candidate_dict, threshold=0.65):
  if new_embedding is None or not candidate_dict:
    return None
  
  best_stu_id = None
  best_match_score = -1
  
  for sid, stored_embedding in candidate_dict.items():
    if stored_embedding:
      similarity = np.dot(new_embedding, stored_embedding)
      
      if similarity > best_match_score:
        best_match_score = similarity
        best_stu_id = sid
        
  if best_match_score >= threshold:
          return best_stu_id, best_match_score
  
  return None, best_match_score
      
def process_bulk_audio(audio_bytes, candidate_dict, threshold=0.65):
  
  try:
    encoder = VoiceEncoder()
    audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
    segments = librosa.effects.split(audio, top_db=30)
    
    identified_results = {}
    
    for start, end in segments:
      if (end-start) < sr * 0.5:
        continue
      
      segment_audio = audio[start:end]
      wav = preprocess_wav(segment_audio)
      embedding = encoder.embed_utterance(wav)
      
      sid, score = identify_speaker(embedding, candidate_dict, threshold)
      
      if sid:
          if sid not in identify_speaker or score > identified_results[sid]:
            identified_results[sid] = score
            
    return identified_results
  except Exception as e:
    st.error("Bulk Process error")
            
        
      
      
    
    