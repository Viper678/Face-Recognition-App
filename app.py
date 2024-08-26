from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import base64
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from face_recognition_module import FaceRecognitionModule
from pymongo import MongoClient
from gridfs import GridFS
import pytz
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['face_recognition']
fs = GridFS(db)

face_recognition_module = FaceRecognitionModule(db)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_id = fs.put(file, filename=filename) 
        face_recognition_module.add_face(image_id, filename)
        return jsonify({'message': 'File uploaded successfully'}), 200
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.json
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data) 
    image_array = np.frombuffer(image_bytes, dtype=np.uint8) 
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR) 

    results = face_recognition_module.process_frame(frame)

    return jsonify(results)

@app.route('/attendance')
def attendance():
    today = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d')
    attendance_records = db.recognitions.find({'date': today}).sort('time', 1)
    records = []
    for record in attendance_records:
        # Extract only the time part
        time = datetime.strptime(record['time'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
        # Remove file extension from name
        name = os.path.splitext(record['name'])[0]
        records.append({'name': name, 'time': time})
    return render_template('attendance.html', records=records)

@app.route('/stream')
def stream():
    return render_template('stream.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
