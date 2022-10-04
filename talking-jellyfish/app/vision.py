import json
import os

import cv2 as cv
import numpy as np
import requests

from config import SyncConfig


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


def print_boxes(canvas, boxes, color=(0, 255, 0)):
    for (xA, yA, xB, yB) in boxes:
        cv.rectangle(canvas, (int(xA), int(yA)), (int(xB), int(yB)), color, 2)


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

    OBJECT_DETECTION_ENDPOINT = os.getenv("OBJECT_DETECTION_ENDPOINT")
    config = SyncConfig("/tmp/jellyfish-sync.conf")

    with CameraOperation() as cap:
        while True:
            config.load_config()
            # Capture frame-by-frame
            ret, frame = cap.read()

            frame = cv.resize(frame, (800, 600))

            res = detect_humans(frame)
            print_boxes(frame, res)
            cv.imshow('frame', frame)

            # if not apps_config.get("chat_enabled") and not apps_config.get(
            if not config.chat and not config.cv and len(res) > 0:
                config.save_config(cv=True, chat=False)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
