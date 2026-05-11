import streamlit as st
import pdfplumber
import nltk
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO

nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

st.set_page_config(page_title="AI Resume Ranker Pro", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f1117 0%, #1a1f2e 100%); border-right: 1px solid #2d3748; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
.main { background-color: #0f1117; }
[data-testid="stAppViewContainer"] { background: #0f1117; }
.glass-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 28px; margin: 16px 0; }
.hero-title { font-family: 'Space Mono', monospace; font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1.1; margin-bottom: 8px; }
.hero-sub { color: #718096; font-size: 1.05rem; font-weight: 300; }
.section-label { font-family: 'Space Mono', monospace; font-size: 0.68rem; letter-spacing: 0.15em; color: #667eea; text-transform: uppercase; margin-bottom: 8px; }
.metric-card { background: rgba(102,126,234,0.08); border: 1px solid rgba(102,126,234,0.2); border-radius: 12px; padding: 20px; text-align: center; }
.metric-value { font-family: 'Space Mono', monospace; font-size: 1.9rem; font-weight: 700; color: #667eea; }
.metric-label { color: #718096; font-size: 0.82rem; margin-top: 4px; }
.skill-tag { display: inline-block; background: rgba(102,126,234,0.15); border: 1px solid rgba(102,126,234,0.3); color: #a78bfa; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; margin: 3px; font-family: 'Space Mono', monospace; }
.stButton > button { background: linear-gradient(135deg, #667eea, #764ba2) !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 1rem !important; padding: 12px 28px !important; }
.custom-divider { height: 1px; background: linear-gradient(90deg, transparent, #2d3748, transparent); margin: 20px 0; }
.about-name { font-family: 'Space Mono', monospace; font-size: 2.2rem; font-weight: 700; color: #e2e8f0; line-height: 1.1; }
.about-role { color: #667eea; font-size: 1.05rem; font-weight: 500; margin-top: 6px; }
.about-bio { color: #a0aec0; font-size: 0.95rem; line-height: 1.7; margin-top: 14px; }
.contact-link { display: block; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px 22px; margin: 10px 0; color: #e2e8f0 !important; text-decoration: none; }
#MainMenu { visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(f):
    text = ""
    try:
        with pdfplumber.open(f) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except: pass
    return text

def clean_text(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    sw = set(stopwords.words('english'))
    return " ".join([w for w in text.split() if w not in sw])

def get_score(r, j):
    cr, cj = clean_text(r), clean_text(j)
    if not cr or not cj: return 0.0
    v = TfidfVectorizer()
    vecs = v.fit_transform([cr, cj])
    return round(cosine_similarity(vecs[0], vecs[1])[0][0] * 100, 2)

def get_missing(r, j, n=5):
    try:
        v = TfidfVectorizer(max_features=50); v.fit([clean_text(j)])
        return ", ".join(list(set(v.get_feature_names_out()) - set(clean_text(r).split()))[:n])
    except: return "N/A"

def status(s):
    return "🟢 Strong" if s >= 70 else "🟡 Moderate" if s >= 40 else "🔴 Weak"

def to_excel(df):
    out = BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as w:
        df.to_excel(w, index=False, sheet_name='Rankings')
        ws = w.sheets['Rankings']
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(max(len(str(c.value or "")) for c in col) + 5, 50)
    return out.getvalue()

# SIDEBAR
with st.sidebar:
    st.markdown("<div style='padding:20px 0 10px;font-family:Space Mono,monospace;font-size:1.1rem;color:#a78bfa;font-weight:700;'>🎯 ResumeRanker</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#4a5568;font-size:0.73rem;margin-bottom:16px;'>AI-Powered Screening Tool</div>", unsafe_allow_html=True)
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    page = st.radio("Nav", ["🎯  Resume Ranker", "👤  About Me", "📬  Contact"], label_visibility="collapsed")
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#4a5568;font-size:0.76rem;line-height:1.7;padding:0 4px;'>Python • NLP • Cosine Similarity<br><br><span style='color:#667eea;'>v2.0</span> • Julakanti Sai Akshaya</div>", unsafe_allow_html=True)

# PAGE 1 — RANKER
if "Ranker" in page:
    st.markdown("<div class='glass-card'><div class='section-label'>AI-Powered Tool</div><div class='hero-title'>Resume Ranker Pro</div><div class='hero-sub'>Upload multiple resumes • Paste one JD • Get instant AI rankings • Export to Excel</div></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("<div class='section-label'>Step 1 — Upload Resumes</div>", unsafe_allow_html=True)
        files = st.file_uploader("PDFs", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
        if files:
            st.markdown(f"<div style='background:rgba(104,211,145,0.1);border:1px solid rgba(104,211,145,0.3);border-radius:10px;padding:10px 16px;color:#68d391;font-size:0.88rem;'>✅ {len(files)} resume(s) ready</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='section-label'>Step 2 — Paste Job Description</div>", unsafe_allow_html=True)
        jd = st.text_area("JD", height=200, placeholder="Paste the full job description here...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀  Analyze & Rank All Resumes", use_container_width=True):
        if not files: st.warning("⚠️ Upload at least one resume!")
        elif not jd.strip(): st.warning("⚠️ Paste a job description!")
        else:
            results = []
            prog = st.progress(0)
            stat = st.empty()
            for i, f in enumerate(files):
                stat.markdown(f"<div style='color:#667eea;font-size:0.88rem;'>⏳ Analyzing {f.name}...</div>", unsafe_allow_html=True)
                rt = extract_text_from_pdf(f)
                sc = get_score(rt, jd) if rt.strip() else 0.0
                results.append({"Rank": 0, "Candidate": f.name.replace(".pdf",""), "Score (%)": sc, "Status": status(sc) if rt.strip() else "❌ Unreadable", "Missing Keywords": get_missing(rt, jd) if rt.strip() else "N/A"})
                prog.progress((i+1)/len(files))
            stat.empty(); prog.empty()

            df = pd.DataFrame(results).sort_values("Score (%)", ascending=False).reset_index(drop=True)
            df["Rank"] = df.index + 1

            st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>Summary</div>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            for col, lbl, val in zip([m1,m2,m3,m4], ["Total Resumes","Best Score","🟢 Strong","Avg Score"], [len(df), f"{df['Score (%)'].max()}%", len(df[df['Score (%)']>=70]), f"{round(df['Score (%)'].mean(),1)}%"]):
                col.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{lbl}</div></div>", unsafe_allow_html=True)

            st.markdown("<br><div class='section-label'>Ranked Results</div>", unsafe_allow_html=True)

            def color_score(val):
                if isinstance(val, float):
                    if val >= 70: return 'background-color:#1a3a2a;color:#68d391'
                    elif val >= 40: return 'background-color:#3a3010;color:#f6e05e'
                    else: return 'background-color:#3a1a1a;color:#fc8181'
                return 'color:#e2e8f0'

            st.dataframe(df.style.applymap(color_score, subset=['Score (%)']), use_container_width=True, height=360)

            top = df.iloc[0]
            st.markdown(f"<div class='glass-card' style='border-color:rgba(104,211,145,0.3);'><div class='section-label'>🏆 Top Candidate</div><div style='font-size:1.4rem;font-weight:700;color:#68d391;font-family:Space Mono,monospace;'>{top['Candidate']}</div><div style='color:#a0aec0;margin-top:6px;'>Score: <strong style='color:#68d391;'>{top['Score (%)']}%</strong> &nbsp;•&nbsp; {top['Status']}</div></div>", unsafe_allow_html=True)

            st.download_button("⬇️  Download Results as Excel", data=to_excel(df), file_name="Resume_Rankings.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# PAGE 2 — ABOUT
elif "About" in page:
    c1, c2 = st.columns([2,1], gap="large")
    with c1:
        st.markdown("""
        <div class='glass-card'>
            <div class='section-label'>Developer & Builder</div>
            <div class='about-name'>Julakanti<br>Sai Akshaya</div>
            <div class='about-role'>AI/ML Developer • Computer Vision • NLP</div>
            <div class='about-bio'>
                BTech CSE Graduate (2026) from Tirumala Engineering College, Andhra Pradesh.
                I build AI-driven tools that solve real problems — from real-time touchless interfaces
                to automated resume screening systems.<br><br>
                I led a team of 4 to build the AI Air Canvas project, achieving 85% gesture recognition
                accuracy using MediaPipe and OpenCV. I also built this Resume Ranker — an NLP pipeline
                that automates candidate screening using TF-IDF and Cosine Similarity.<br><br>
                Actively seeking entry-level Software Engineer or AI/ML Developer roles.
            </div>
        </div>
        <div class='glass-card'>
            <div class='section-label'>Technical Skills</div>
            <div style='margin-top:10px;'>
                <span class='skill-tag'>Python</span><span class='skill-tag'>OpenCV</span>
                <span class='skill-tag'>MediaPipe</span><span class='skill-tag'>NLP</span>
                <span class='skill-tag'>Scikit-Learn</span><span class='skill-tag'>Computer Vision</span>
                <span class='skill-tag'>Streamlit</span><span class='skill-tag'>TF-IDF</span>
                <span class='skill-tag'>Cosine Similarity</span><span class='skill-tag'>SQL</span>
                <span class='skill-tag'>Git</span><span class='skill-tag'>GitHub</span>
                <span class='skill-tag'>C++</span><span class='skill-tag'>OOP</span>
                <span class='skill-tag'>Agile</span><span class='skill-tag'>DBMS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='glass-card'>
            <div class='section-label'>Projects</div>
            <div style='margin-top:14px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.06);'>
                <div style='color:#a78bfa;font-family:Space Mono,monospace;font-size:0.83rem;font-weight:700;'>🖐️ AI Air Canvas</div>
                <div style='color:#718096;font-size:0.8rem;margin-top:5px;line-height:1.5;'>Real-time touchless drawing using MediaPipe & OpenCV. 85% accuracy. Team Lead.</div>
            </div>
            <div style='margin-top:14px;'>
                <div style='color:#a78bfa;font-family:Space Mono,monospace;font-size:0.83rem;font-weight:700;'>🎯 AI Resume Ranker</div>
                <div style='color:#718096;font-size:0.8rem;margin-top:5px;line-height:1.5;'>NLP resume screening tool — ranks multiple candidates using TF-IDF & Cosine Similarity.</div>
            </div>
        </div>
        <div class='glass-card'>
            <div class='section-label'>Education</div>
            <div style='margin-top:10px;'>
                <div style='color:#e2e8f0;font-weight:600;font-size:0.88rem;'>BTech CSE</div>
                <div style='color:#718096;font-size:0.8rem;'>Tirumala Engineering College</div>
                <div style='color:#667eea;font-size:0.78rem;margin-top:2px;'>2022–2026 • 75%</div>
            </div>
        </div>
        <div class='glass-card'>
            <div class='section-label'>Certifications</div>
            <div style='color:#a0aec0;font-size:0.82rem;line-height:2;margin-top:8px;'>
                🏅 Python — NPTEL<br>
                🏅 Infosys Pragati — Cohort 5<br>
                🏅 be10X AI Tools Workshop<br>
                🏅 Introduction to IoT
            </div>
        </div>
        """, unsafe_allow_html=True)

# PAGE 3 — CONTACT
elif "Contact" in page:
    st.markdown("<div class='glass-card' style='max-width:680px;margin:0 auto 24px auto;'><div class='section-label'>Get In Touch</div><div class='hero-title' style='font-size:2.2rem;'>Let's Connect</div><div class='hero-sub'>Open to entry-level SWE and AI/ML roles.<br>Reach out for opportunities or collaborations.</div></div>", unsafe_allow_html=True)
    _, c, _ = st.columns([1,2,1])
    with c:
        st.markdown("""
        <div class='glass-card'>
            <div class='section-label'>Contact Details</div>
            <a class='contact-link' href='mailto:julakantiakshaya300@gmail.com'>
                <span style='font-size:1.2rem;'>📧</span>&nbsp;&nbsp;<strong>Email</strong><br>
                <span style='color:#718096;font-size:0.82rem;margin-left:28px;'>julakantiakshaya300@gmail.com</span>
            </a>
            <a class='contact-link' href='https://www.linkedin.com/in/julakanti-sai-akshaya' target='_blank'>
                <span style='font-size:1.2rem;'>💼</span>&nbsp;&nbsp;<strong>LinkedIn</strong><br>
                <span style='color:#718096;font-size:0.82rem;margin-left:28px;'>linkedin.com/in/julakanti-sai-akshaya</span>
            </a>
            <a class='contact-link' href='https://github.com/SaiAkshaya18' target='_blank'>
                <span style='font-size:1.2rem;'>💻</span>&nbsp;&nbsp;<strong>GitHub</strong><br>
                <span style='color:#718096;font-size:0.82rem;margin-left:28px;'>github.com/SaiAkshaya18</span>
            </a>
            <div style='margin-top:18px;padding:14px;background:rgba(102,126,234,0.08);border-radius:10px;border:1px solid rgba(102,126,234,0.2);'>
                <div style='color:#667eea;font-size:0.78rem;font-weight:600;margin-bottom:5px;'>📍 Location</div>
                <div style='color:#a0aec0;font-size:0.88rem;'>Chilakaluripet, Andhra Pradesh, India<br>
                <span style='color:#68d391;font-size:0.8rem;'>✅ Open to Relocation & Remote</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
