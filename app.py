from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import re
import os

app = Flask(__name__)
CORS(app)

skills_list = ["python", "java", "c++", "react", "sql", "html", "css", "javascript", "flask", "django"]

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(text):
    text = text.lower()
    return list({skill for skill in skills_list if re.search(r"\b" + re.escape(skill) + r"\b", text)})

@app.route("/extract-skills", methods=["POST"])
def extract_skills_endpoint():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    resume = request.files['resume']
    file_path = resume.filename
    resume.save(file_path)

    try:
        text = extract_text_from_pdf(file_path)
        skills = extract_skills(text)
        os.remove(file_path)
        return jsonify({"skills": skills})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
