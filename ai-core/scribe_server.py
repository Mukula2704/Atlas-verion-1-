from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from autonomous_scribe import AutonomousScribe
import asyncio

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from the HTML dashboard

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

scribe = AutonomousScribe()

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file part"}), 400
        
    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lecture_{timestamp}.webm"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        print(f"[SCRIBE SERVER] Audio saved to {filepath}. Initiating transcription...")
        
        # Block and return the result
        notes_path = scribe.process_lecture_audio(filepath, course_name="Auto-Scribed Lecture")
        
        if notes_path:
            return jsonify({"status": "success", "notes_path": notes_path})
        else:
            return jsonify({"status": "error", "message": "Failed to generate notes"}), 500

if __name__ == '__main__':
    print("[SCRIBE SERVER] Online at http://127.0.0.1:5000")
    app.run(port=5000, debug=False)
