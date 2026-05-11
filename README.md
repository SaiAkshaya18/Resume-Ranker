# 🎯 AI Resume Ranker Pro

### Automate resume screening with AI. Upload multiple resumes, paste one JD, get instant rankings.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?style=flat-square&logo=streamlit)
![NLP](https://img.shields.io/badge/NLP-TF--IDF-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 Overview

AI Resume Ranker Pro is a web-based tool that automates the initial resume screening process for recruiters and HR teams. Upload multiple PDF resumes, paste a job description, and instantly get a ranked list of candidates based on how well their resume matches the JD — powered by NLP and Cosine Similarity.

This is the kind of tool companies like LinkedIn and Naukri charge for. Built from scratch as a final year project.

---

## ✨ Features

- 📁 **Multi-Resume Upload** — Upload 10, 20, or 50 resumes at once
- 🤖 **AI-Powered Matching** — TF-IDF vectorization + Cosine Similarity scoring
- 🏆 **Instant Rankings** — Candidates ranked from best to worst match automatically
- 🔍 **Keyword Gap Analysis** — Missing JD keywords highlighted for each candidate
- 📊 **Summary Dashboard** — Total resumes, best score, strong matches, average score
- ⬇️ **Excel Export** — Download full ranked results as .xlsx in one click
- 🎨 **Beautiful Dark UI** — Professional 3-page Streamlit app
- 👤 **Portfolio Page** — About Me and Contact sections built in

---

## 🖥️ App Pages

| Page | Description |
|---|---|
| 🎯 Resume Ranker | Main screening tool |
| 👤 About Me | Developer profile and skills |
| 📬 Contact | Email, LinkedIn, GitHub links |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.9+ |
| Web Framework | Streamlit |
| NLP | NLTK, Scikit-Learn |
| Vectorization | TF-IDF (TfidfVectorizer) |
| Similarity | Cosine Similarity |
| PDF Extraction | pdfplumber |
| Excel Export | pandas + openpyxl |
| Version Control | Git & GitHub |

---

## 📁 Project Structure

```
Resume-Ranker/
│
├── app.py                          # Main Streamlit application (3 pages)
├── ranker.py                       # Core NLP script (command-line version)
├── jd.txt                          # Sample job description for testing
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.9+ installed.

### Installation

```bash
# Clone the repository
git clone https://github.com/SaiAkshaya18/Resume-Ranker.git
cd Resume-Ranker

# Install dependencies
pip install -r requirements.txt
```

### Run the Web App

```bash
streamlit run app.py
```

Opens automatically at `http://localhost:8501`

### Run the Script Version

```bash
python ranker.py
```

---

## 📋 Requirements

```
streamlit
pdfplumber
nltk
scikit-learn
pandas
openpyxl
```

Or install all at once:
```bash
pip install streamlit pdfplumber nltk scikit-learn pandas openpyxl
```

---

## 🧠 How It Works

```
PDF Resumes Uploaded
        ↓
Text Extracted (pdfplumber)
        ↓
Text Cleaned & Preprocessed (NLTK stopword removal)
        ↓
TF-IDF Vectorization (resume + JD converted to vectors)
        ↓
Cosine Similarity Score Calculated
        ↓
Candidates Ranked (best match → worst match)
        ↓
Missing Keywords Identified
        ↓
Results Displayed + Excel Download
```

### Scoring Guide

| Score | Status | Meaning |
|---|---|---|
| 70%+ | 🟢 Strong Match | Apply / shortlist with confidence |
| 40–70% | 🟡 Moderate Match | Consider with tailoring |
| Below 40% | 🔴 Weak Match | Significant keyword gaps |

---

## 📊 Results

- ✅ Successfully screens multiple resumes simultaneously
- ✅ Ranks candidates objectively using semantic similarity
- ✅ Identifies missing keywords to help candidates improve
- ✅ Exports results to Excel for recruiter use
- ✅ Built and deployed as a fully functional web application

---

## 📸 Screenshots

> Resume Ranker Tool — Upload resumes, paste JD, get instant rankings with color-coded scores and missing keyword analysis.

---

## 🔮 Future Improvements

- [ ] Deploy on Streamlit Cloud for public access
- [ ] Add support for DOCX resume format
- [ ] Implement BERT-based semantic matching for higher accuracy
- [ ] Add candidate email notification system
- [ ] Store results in a database for history tracking

---

## 👤 Developer

**Julakanti Sai Akshaya**
- 🔗 [LinkedIn](https://www.linkedin.com/in/julakanti-sai-akshaya)
- 💻 [GitHub](https://github.com/SaiAkshaya18)
- 📧 julakantiakshaya300@gmail.com

*BTech CSE Graduate — Tirumala Engineering College (2022–2026)*

---

## 📜 Also Check Out

- 🖐️ [AI Air Canvas](https://github.com/SaiAkshaya18/Air-Canvas) — Real-time touchless drawing interface using MediaPipe & OpenCV

---

https://resume-ranker-pro.streamlit.app

⭐ *If you found this project useful, consider giving it a star!*
