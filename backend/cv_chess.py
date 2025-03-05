import cv2
import os
import numpy as np
from ultralytics import YOLO
from cv_chess_functions import yolo_to_fen, fen_to_image, map_to_fen
script_dir = os.path.dirname(os.path.abspath(__file__))


def rescale_frame(frame, dimensions=(1000, 750)):
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


board_path = "current_board.png"

if not os.path.exists(board_path):
    blank_image = 255 * np.ones((480, 480, 3), dtype=np.uint8)
    cv2.imwrite(board_path, blank_image)

model = YOLO("../yolo/runs/detect/train5/weights/best.pt")
cap = cv2.VideoCapture(2)

current_board_image = cv2.imread(board_path)
cv2.imshow('Current Board', current_board_image)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    results = model(frame)
    boxes = []
    for result in results:
        for box in result.boxes.data:
            x, y, w, h, conf, cls = box.cpu().numpy()
            cls = int(cls)
            boxes.append((x, y, w, h, cls))

            x, y, w, h = int(x), int(y), int(w), int(h)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            label = f"{yolo_to_fen.get(cls, '?')} ({conf:.2f})"
            cv2.putText(frame, label, (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    latest_fen = map_to_fen(boxes, frame.shape[:2])
    fen_to_image(latest_fen, output_path=board_path)

    resized_frame = rescale_frame(frame)
    cv2.imshow('Live Feed', resized_frame)

    board_img = cv2.imread(board_path)
    if board_img is not None:
        cv2.imshow('Current Board', board_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
