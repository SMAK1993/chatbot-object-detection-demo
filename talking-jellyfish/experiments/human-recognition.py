
import numpy as np

from transformers import DetrFeatureExtractor, DetrForObjectDetection
import torch
from PIL import Image
import requests

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
img = Image.open(requests.get(url, stream=True).raw)

# print(np.asarray(img).tolist())

feature_extractor = DetrFeatureExtractor.from_pretrained(
    "facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# img = Image.open("../data/frame_screenshot_06.08.2022.png")
inputs = feature_extractor(images=img, return_tensors="pt")
outputs = model(**inputs)

# convert outputs (bounding boxes and class logits) to COCO API
target_sizes = torch.tensor([img.size[::-1]])

results = feature_extractor.post_process(outputs, target_sizes=target_sizes)[0]

res = []
for score, label, box in zip(results["scores"], results["labels"],
                             results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    res.append({
        "label": model.config.id2label[label.item()],
        "score": score.item(),
        "box": box
    })

for r in res:
    if r['score'] > 0.9:
        print(
            f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}"
        )
