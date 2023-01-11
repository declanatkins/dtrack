from dataclasses import dataclass
from typing import Any, Dict, List
from .util import Detection, Image
from .tracking.trackable import TrackableObject


@dataclass
class ApplicationContext:
    """Contains contextual data for the application. Used for evaluating arguments
        in pipelines.
    """
    frame_image: Image
    frame_number: int
    object_detections: List[Detection]
    trackable_objects: Dict[str, TrackableObject]
    matched_keys: List[str]
    unmatched_keys: List[str]
    new_keys: List[str]
    deleted_keys: List[str]
    tracking_attributes: Dict[str, Any]
    pipeline_step_results: Dict[str, Any]
