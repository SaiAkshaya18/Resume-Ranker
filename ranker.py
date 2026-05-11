import pdfplumber
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    return " ".join([w for w in text.split() if w not in stop_words])

def extract_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


RESUME_PATH = r"Julakanti Sai Akshaya_Resume_CSE.pdf"
JD_PATH = "jd.txt"

print("Reading resume...")
resume_text = extract_pdf(RESUME_PATH)

print("Reading JD...")
with open(JD_PATH, 'r', encoding='utf-8') as f:
    jd_text = f.read()

print("Calculating score...")
v = TfidfVectorizer()
vecs = v.fit_transform([clean_text(resume_text), clean_text(jd_text)])
score = round(cosine_similarity(vecs[0], vecs[1])[0][0] * 100, 2)

print(f"\nMATCH SCORE: {score}%")

if score >= 70:
    print("Strong Match - Apply with confidence!")
elif score >= 50:
    print("Moderate Match - Tailor your resume more.")
else:
    print("Weak Match - Keyword gaps found.")