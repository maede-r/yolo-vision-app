from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import threading
import pyttsx3

app = Flask(__name__)
model = YOLO("yolov8n.pt")  # بارگذاری مدل

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_threaded(text):
    threading.Thread(target=speak, args=(text,)).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()
    encoded_image = data["image"].split(",")[1]
    img_data = base64.b64decode(encoded_image)
    np_array = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    results = model(frame)
    boxes = results[0].boxes
    names = results[0].names
    labels = []

    if boxes:
        for i in range(len(boxes)):
            cls = int(boxes.cls[i])
            label = names[cls]
            labels.append(label)
            x1, y1, x2, y2 = map(int, boxes.xyxy[i])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if labels:
        speak_threaded(" and ".join(labels) + " detected")

    _, buffer = cv2.imencode(".jpg", frame)
    result_image = base64.b64encode(buffer).decode("utf-8")

    return jsonify({"image": f"data:image/jpeg;base64,{result_image}", "labels": labels})

if __name__ == "__main__":
    app.run(debug=True)
