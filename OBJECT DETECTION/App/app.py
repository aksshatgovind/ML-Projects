from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Load the model
config_file = 'OBJECT DETECTION/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'OBJECT DETECTION/frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)
classLabels = []
file_name = 'OBJECT DETECTION/labels.txt'

with open(file_name, 'rt') as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')

model.setInputSize(320, 320)
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

# Open a video capture object
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        ClassIndex, confidence, bbox = model.detect(frame, confThreshold=0.6)
        
        if len(ClassIndex) != 0:
            for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
                if ClassInd <= 80:
                    cv2.rectangle(frame, boxes, (255, 0, 0), 2)
                    cv2.putText(frame, classLabels[ClassInd - 1], (boxes[0] + 10, boxes[1] + 40), 
                                cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(0, 255, 0), thickness=3)

        # Convert the image to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break

        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


