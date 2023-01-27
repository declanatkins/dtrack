from dataclasses import dataclass
from typing import Any, Dict, List, Type
from .util import Detection, Image
from .tracking.movement.predictor import MovementPredictor
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
    deleted_objects: Dict[str, TrackableObject]
    tracking_attributes: Dict[str, Any]
    pipeline_step_results: Dict[str, Any]
    tracked_object_classes: Dict[str, Type[TrackableObject]]
    movement_predictors_by_class: Dict[str, Type[MovementPredictor]]
    delete_after_by_class: Dict[str, int]
