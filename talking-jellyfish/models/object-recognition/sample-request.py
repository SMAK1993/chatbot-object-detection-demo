import requests
import numpy as np
import json

from PIL import Image

from MyModel import MyModel

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
cat_image = Image.open(requests.get(url, stream=True).raw)
image_list = np.asarray(cat_image).tolist()

body = {
    "data": {
        "ndarray": image_list
    }
}

results = requests.post("http://192.168.0.191:9000/api/v0.1/predictions",
                        json=body)
print(f"Result code {results.status_code}")
res = json.loads(results.text)
print(res)
for r in res['data']['ndarray']:
    # if r['score'] > 0.9:
        print(
            f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
        )

# model = MyModel(
#     feature_extractor_path="./build/",
#     model_path="./build/"
# )
# res = model.predict(image_list, [])
# res = model.predict(np.asarray(cat_image).tolist(), [])

# for r in res:
#     if r['score'] > 0.9:
#         print(
#             f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
#         )