import json
import time

import cv2 as cv
import numpy as np
import requests

OBJECT_DETECTION_ENDPOINT = "http://10.152.183.182:8000/api/v0.1/predictions"


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
    return [r['box'] for r in res['data']['ndarray'] if r['score'] > 0.9]



# CHATBOT_ENDPOINT = ""
# def chatbot():
#     pass


if __name__ == '__main__':

    cv.startWindowThread()

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # while True:
    for i in range(1000):
        print(f"Interation {i}")
        # Capture frame-by-frame
        ret, frame = cap.read()

        frame = cv.resize(frame, (800, 600))

        # using a greyscale picture, also for faster detection
        gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

        # start = time.time()
        res = detect_humans(frame)
        # print(f"Detect human: {time.time()-start}")

        # boxes, weights = hog.detectMultiScale(frame, winStride=(4, 4))
        # #
        # boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        # #
        # TODO
        for (xA, yA, xB, yB) in res:
            # display the detected boxes in the colour picture
            cv.rectangle(frame, (int(xA), int(yA)), (int(xB), int(yB)), (0, 255, 0), 2)
        #
        # # Display the resulting frame

        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()

    cv.destroyAllWindows()
    cv.waitKey(1)
