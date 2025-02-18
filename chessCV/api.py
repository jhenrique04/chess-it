from flask import Flask, Response, send_file
import os
import cv2
import threading
import time

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
board_svg_path = os.path.join(script_dir, "current_board.svg")

video_source = "/dev/video3"
cap = None
lock = threading.Lock()

def create_capture():
    global cap
    if cap is not None:
        cap.release()
    cap = cv2.VideoCapture(video_source, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera virtual do OBS.")
    return cap

cap = create_capture()

@app.route("/board")
def get_board():
    if os.path.exists(board_svg_path):
        return send_file(board_svg_path, mimetype="image/svg+xml")
    return "Board not found", 404

def generate_frames():
    global cap
    
    while True:
        with lock:
            success, frame = cap.read()
            if not success:
                print("Erro ao capturar frame. Tentando reiniciar a câmera...")
                cap.release()
                cap = create_capture()
                time.sleep(1)
                continue

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video")
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/reset")
def reset_camera():
    global cap
    with lock:
        cap.release()
        cap = create_capture()
    return "Câmera reiniciada com sucesso.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
