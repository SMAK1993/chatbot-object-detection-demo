import json
from enum import Enum

import cv2 as cv
import numpy as np
import requests

OBJECT_DETECTION_ENDPOINT = "http://10.152.183.182:8000/api/v0.1/predictions"
CHATBOT_ENDPOINT = "http://10.152.183.11:8000/api/v0.1/predictions"


def detect_humans(img):
    body = {
        "data": {
            "ndarray": np.asarray(img).tolist()
        }
    }
    results = requests.post(OBJECT_DETECTION_ENDPOINT, json=body)
    print(f"Result code {results.status_code}")
    res = json.loads(results.text)

    for r in res['data']['ndarray']:
        if r['score'] > 0.9:
            print(
                f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
            )

    return [r['box'] for r in res['data']['ndarray'] if
            (r['score'] > 0.9 and r['label'] == "person")]


def chatbot(text):
    body = {
        "data": {
            "ndarray": text
        }
    }
    response = requests.post(CHATBOT_ENDPOINT, json=body)
    print(response.status_code, response.content)
    return json.loads(response.content)["strData"]


def print_boxes(canvas, boxes, color=(0, 255, 0)):
    for (xA, yA, xB, yB) in boxes:
        cv.rectangle(canvas, (int(xA), int(yA)), (int(xB), int(yB)), color, 2)


class JellyfishMode(Enum):
    WAIT = 1
    ATTRACT = 2
    TALK = 3


class CameraOperation:

    def __enter__(self):
        cv.startWindowThread()
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Cannot open camera")
        return self.cap

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()
        cv.destroyAllWindows()
        cv.waitKey(1)


if __name__ == '__main__':

    with CameraOperation() as cap:
        mode = JellyfishMode.WAIT

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            frame = cv.resize(frame, (800, 600))

            res = detect_humans(frame)
            print_boxes(frame, res)
            cv.imshow('frame', frame)

            if len(res) > 0:
                mode = JellyfishMode.TALK

            if mode == JellyfishMode.TALK:
                user_input = input(">> User:")
                bot_response = chatbot(user_input)
                print(bot_response)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
