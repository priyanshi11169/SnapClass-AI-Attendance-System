# 🎓 SnapClass — AI Attendance System

> Automated attendance using **Face Recognition** and **Voice Recognition** — built with Python, Streamlit & Supabase.

---

## 📌 What is SnapClass?

SnapClass is an AI-powered attendance system that eliminates manual roll calls. Teachers simply take a photo or record classroom audio — the AI identifies students and marks attendance automatically.

Students log in using their **face** (no passwords needed), enroll in subjects, and track their own attendance records in real time.

---

## ✨ Features

### 👩‍🏫 Teacher Portal
- Secure login & registration with username/password
- Create and manage subjects with unique codes
- Share subject enrollment codes with students
- **Face Attendance** — upload classroom photos, AI detects & marks who's present
- **Voice Attendance** — record classroom audio, AI identifies students by voice
- View attendance records per subject

### 👨‍🎓 Student Portal
- **FaceID Login** — no passwords, just look at the camera
- Auto-registration for new students via face capture
- Optional voice enrollment during registration
- Enroll/unenroll in subjects using subject codes
- View personal attendance stats per subject (total classes vs attended)

### 🤖 AI Pipelines
- **Face Recognition** — dlib + SVM classifier trained on student embeddings
- **Voice Recognition** — Resemblyzer voice encoder with cosine similarity matching
- Auto-retrains face classifier when new students register

---

## 🗂️ Project Structure

```
SnapClass/
├── src/
│   ├── components/          # UI components (dialogs, cards, header, footer)
│   │   ├── attendance_dialog.py
│   │   ├── dialog_voice_attendance.py
│   │   ├── enroll_dialog.py
│   │   ├── subject_card.py
│   │   └── ...
│   ├── database/
│   │   ├── config.py        # Supabase client setup
│   │   └── db.py            # All database queries
│   ├── pipelines/
│   │   ├── face_pipelines.py   # dlib face recognition
│   │   └── voice_pipelines.py  # Resemblyzer voice recognition
│   ├── screens/
│   │   ├── home_screen.py
│   │   ├── student_screen.py
│   │   └── teacher_screen.py
│   └── ui/
│       └── base_layout.py   # Global styles & background
├── app.py                   # Entry point
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend & UI | Streamlit |
| Backend & Auth | Supabase (PostgreSQL) |
| Face Detection | dlib, face_recognition_models |
| Face Classification | scikit-learn SVM |
| Voice Recognition | Resemblyzer, librosa |
| Language | Python 3.11 |

---

## 🗄️ Supabase Tables

| Table | Description |
|---|---|
| `students` | Student profiles with face & voice embeddings |
| `teachers` | Teacher accounts with hashed passwords |
| `subjects` | Subjects created by teachers |
| `subjects_students` | Student-subject enrollment mapping |
| `attendance` | Attendance logs with timestamp & presence status |

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/snapclass.git
cd snapclass
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Supabase
- Create a project at [supabase.com](https://supabase.com)
- Create the tables listed above
- Copy your project URL and anon key

### 5. Create `.env` file
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### 6. Run the app
```bash
streamlit run app.py
```

---

## 🚀 How It Works

### Face Attendance Flow
1. Teacher selects a subject and uploads classroom photos
2. dlib detects faces and extracts 128-d embeddings
3. SVM classifier matches embeddings to registered students
4. Attendance is logged automatically to Supabase

### Voice Attendance Flow
1. Teacher records classroom audio
2. Resemblyzer splits audio into speech segments
3. Each segment is compared to stored student voice embeddings via cosine similarity
4. Matched students are marked present

### Student Login Flow
1. Student opens camera → dlib detects face
2. Embedding compared against database
3. If matched → logged in instantly
4. If new → registration form appears with optional voice enrollment

- Built by **Priyanshi Tiwari**

## 📄 License

MIT License — feel free to use, modify, and share.
