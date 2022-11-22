from dataclasses import dataclass
import json
import numpy as np
from .box import Box


@dataclass
class Detection:
    """
    Detection of an object in an image.
    """
    label: str
    confidence: float
    box: Box
    mask: np.ndarray

    def __post_init__(self):
        self.mask = self.mask.astype(np.bool)

    def __str__(self):
        return f"{self.label} ({self.confidence:.2f})"

    def __repr__(self):
        return f"Detection({self.label}, {self.confidence}, {self.box}, {self.mask})"

    def to_dict(self):
        return {
            "label": self.label,
            "confidence": self.confidence,
            "box": self.box.to_dict(),
            "mask": self.mask.tolist()
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            d["label"],
            d["confidence"],
            Box.from_dict(d["box"]),
            np.array(d["mask"])
        )

    @classmethod
    def from_json(cls, s: str):
        return cls.from_dict(json.loads(s))

    def to_coco(self, image_id: int, category_id: int, segmentation_id: int):
        return {
            "image_id": image_id,
            "category_id": category_id,
            "segmentation_id": segmentation_id,
            "bbox": self.box.to_coco(),
            "score": self.confidence,
            "segmentation": self.mask_to_coco()
        }

    def mask_to_coco(self):
        return [self.mask.flatten().tolist()]
    
    def __eq__(self, other):
        return self.label == other.label and self.confidence == other.confidence and self.box == other.box and np.array_equal(self.mask, other.mask)
    