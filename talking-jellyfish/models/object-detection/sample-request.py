import time

import requests
import numpy as np
import json

from PIL import Image

from ObjectDetection import ObjectDetection

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
cat_image = Image.open(requests.get(url, stream=True).raw)
image_list = np.asarray(cat_image).tolist()

body = {
    "data": {
        "ndarray": image_list
    }
}

MODEL_ENDPOINT = "http://10.1.110.162:9000/api/v0.1/predictions"

start=time.time()
results = requests.post(MODEL_ENDPOINT, json=body)
print(f"Request time: {time.time()-start}")

print(f"Result code {results.status_code}")
res = json.loads(results.text)

print(res)
for r in res['data']['ndarray']:
    if r['score'] > 0.9:
        print(
            f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
        )

# Local model execution
# model = ObjectDetection(
#     feature_extractor_path="./build/",
#     model_path="./build/"
# )
# # res = model.predict(image_list, [])
# start=time.time()
# res = model.predict(image_list, [])
# print(f"Request time: {time.time()-start}")
#
# for r in res:
#     if r['score'] > 0.9:
#         print(
#             f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
#         )
