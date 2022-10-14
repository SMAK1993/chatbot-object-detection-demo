import base64
import json
import logging
import os

import cv2 as cv
import requests
from PIL import Image

from config import SyncConfig

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
log = logging.getLogger("VisionApp")


def detect_humans(img):
    files = {
        "mode": img.mode,
        "size": f"{img.size[0]}x{img.size[1]}",
        "media": base64.b64encode(img.tobytes())
    }
    log.debug(f"Files: mode={files['mode']} size={files['size']}")
    results = requests.post(OBJECT_DETECTION_ENDPOINT, files=files)
    log.debug(
        f"Object detection endpoint call result code {results.status_code}")
    res = json.loads(results.text)

    for r in res:
        if r['score'] > 0.9:
            log.debug(
                f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
            )

    return [r['box'] for r in res if
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
            log.debug("Sync config loaded.")
            # Capture frame-by-frame

            ret, frame = cap.read()
            log.info("Frame captured")

            frame = cv.resize(frame, (800, 600))
            log.debug("Frame resized")

            frame_image = Image.fromarray(frame)
            humans = detect_humans(frame_image)
            log.info(f"Number of humans detected: {len(humans)}")

            print_boxes(frame, humans)
            log.debug("Boxes printed on the frame.")

            cv.imshow('frame', frame)
            log.debug("Frame updated in the Window")

            if not config.chat and not config.cv and len(humans) > 0:
                config.save_config(cv=True, chat=False)
                log.info(f"Update the sync config to {config}")

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
