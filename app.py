import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from screener import screen_resumes

app = Flask(__name__, static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/screen", methods=["POST"])
def screen():
    job_description = request.form.get("job_description", "").strip()
    if not job_description:
        return jsonify({"error": "Job description is required."}), 400

    files = request.files.getlist("resumes")
    if not files:
        return jsonify({"error": "At least one resume PDF is required."}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        for file in files:
            if file.filename.endswith(".pdf"):
                filename = secure_filename(file.filename)
                filepath = os.path.join(tmpdir, filename)
                file.save(filepath)

        results = screen_resumes(job_description, tmpdir)

    return jsonify({"results": results})


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))