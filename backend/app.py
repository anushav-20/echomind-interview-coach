"""
EchoMind - AI Mock Interview Coach

Records a spoken answer to an interview question, transcribes it with
OpenAI's Whisper model, then analyzes the transcript for filler words,
speaking pace, hedging language, and overall confidence -- giving the kind
of delivery feedback a human interview coach would provide.
"""
import os
import whisper
from flask import Flask, request, jsonify
from flask_cors import CORS
from mutagen import File as AudioFile

from utils.analyzer import analyze_answer

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024

QUESTIONS = [
    "Tell me about a time you solved a difficult technical problem.",
    "Why do you want to work at this company?",
    "Describe a situation where you disagreed with a teammate. How did you handle it?",
    "What is your biggest weakness, and how are you working on it?",
]

_whisper_model = None


def get_model():
    global _whisper_model
    if _whisper_model is None:
        # "base" model balances speed and accuracy for short interview answers
        _whisper_model = whisper.load_model("base")
    return _whisper_model


@app.route("/api/questions", methods=["GET"])
def get_questions():
    return jsonify({"questions": QUESTIONS})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/evaluate-answer", methods=["POST"])
def evaluate_answer():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    filepath = os.path.join(UPLOAD_DIR, audio_file.filename)
    audio_file.save(filepath)

    try:
        model = get_model()
        result = model.transcribe(filepath)
        transcript = result["text"].strip()

        audio_meta = AudioFile(filepath)
        duration = audio_meta.info.length if audio_meta else 0

        analysis = analyze_answer(transcript, duration)
        analysis["transcript"] = transcript
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
