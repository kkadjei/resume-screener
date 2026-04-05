#  ResumeRank — AI-Powered Resume Screener

> Rank PDF resumes by relevance to a job description using semantic embeddings. Runs as a CLI tool or a web app.

---

##  Features

-  Accepts multiple PDF resumes at once
-  Uses `sentence-transformers` (MiniLM) for semantic similarity, not just keyword matching
-  CLI mode for fast terminal usage
-  Web UI for drag-and-drop screening
-  Scores range from 0–100% with a ranked output

---

##  Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/kkadjei/resume-screener.git
cd resume-screener
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

##  CLI Usage
```bash
python cli.py --job job.txt --resumes ./resumes/
```

---

##  Web UI Usage
```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

##  How It Works

1. Extracts text from each PDF using `pdfplumber`
2. Encodes the job description and each resume into vector embeddings using `all-MiniLM-L6-v2`
3. Computes cosine similarity between the job description and each resume
4. Ranks resumes from highest to lowest match

---

##  Tech Stack

- [sentence-transformers](https://www.sbert.net/) — semantic embeddings
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction
- [Flask](https://flask.palletsprojects.com/) — web server
- [Click](https://click.palletsprojects.com/) — CLI framework
