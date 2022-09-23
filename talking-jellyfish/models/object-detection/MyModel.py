import numpy as np
from transformers import DetrFeatureExtractor, DetrForObjectDetection
import torch
import PIL
from pathlib import Path
import logging

MODEL_DIR = "/app/build/"


class MyModel(object):

    def __init__(self,
                 feature_extractor_path=MODEL_DIR,
                 model_path=MODEL_DIR
                 ):
        print("Initializing")
        self.feature_extractor = DetrFeatureExtractor.from_pretrained(
            Path(feature_extractor_path))
        self.model = DetrForObjectDetection.from_pretrained(Path(model_path),
                                                            cache_dir=MODEL_DIR)
        self.log = logging.getLogger()
        self.log.info("Initialized!")

    def predict(self, X, features_names):
        """
        Return a prediction.
        Parameters
        ----------
        X : array-like
        feature_names : array of feature names (optional)
        """
        self.log.info(f"Predict invoked!")
        image = PIL.Image.fromarray(np.asarray(X, np.uint8), mode="RGB")

        self.log.info(f"Image converted")
        inputs = self.feature_extractor(images=image, return_tensors="pt")
        self.log.info(f"Features extracted")
        outputs = self.model(**inputs)

        # convert outputs (bounding boxes and class logits) to COCO API
        self.log.info("Convert results")
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.feature_extractor.post_process(
            outputs,
            target_sizes=target_sizes)[0]

        output = []
        for score, label, box in zip(results["scores"], results["labels"],
                                     results["boxes"]):
            if score.item() > 0.01:
                box = [round(i, 2) for i in box.tolist()]
                output.append({
                    "label": self.model.config.id2label[label.item()],
                    "score": score.item(),
                    "box": box
                })

        self.log.info(f"Results: {output}")
        return output
