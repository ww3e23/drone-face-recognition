from flask import Flask, request, jsonify
from deepface import DeepFace
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return '👋 Drone Face Recognition Ready!'

@app.route('/verify', methods=['POST'])
def verify():
    if 'img1' not in request.files or 'img2' not in request.files:
        return jsonify({'error': 'Two images required (img1 and img2)'}), 400

    img1 = np.frombuffer(request.files['img1'].read(), np.uint8)
    img2 = np.frombuffer(request.files['img2'].read(), np.uint8)
    img1 = cv2.imdecode(img1, cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(img2, cv2.IMREAD_COLOR)

    result = DeepFace.verify(img1, img2, enforce_detection=False)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
