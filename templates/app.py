from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠 (다른 카메라 연결시 1~)

def process_frame(frame): 
    alpha = 2  # 밝기 조절
    beta = 30
    brightened_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    return brightened_frame

def generate_frames_input(): # 입력 영상
    while True:
        success, frame = cap.read()
        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)

        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def generate_frames_output(): # 출력 영상
    while True:
        success, frame = cap.read()
        if not success:
            break

        processed_frame = process_frame(frame)
        ret, buffer = cv2.imencode('.jpg', processed_frame)

        if ret:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


#####################################################################################################################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_input')
def video_feed_input():
    return Response(generate_frames_input(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_output')
def video_feed_output():
    return Response(generate_frames_output(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
