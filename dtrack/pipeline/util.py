from typing import List
from uuid import uuid4
import numpy as np
from ..context import ApplicationContext
from ..detection.detector import ObjectDetector
from ..tracking.distance.distance_algorithm import DistanceAlgorithm
from ..util import Detection
from .step import PipelineStep


class ObjectDetectionStep(PipelineStep):
    """A pipeline step that detects objects in an image.
    """

    def __init__(self, detector: ObjectDetector, *prediction_args, **prediction_kwargs):
        self.detector = detector
        self.prediction_args = prediction_args
        self.prediction_kwargs = prediction_kwargs
        self.function = self.detect
        
    def detect(self, detector: ObjectDetector, context: ApplicationContext) -> None:
        """Detects objects in the image.
        """
        detections = detector.predict(context.frame_image, *self.prediction_args, **self.prediction_kwargs)
        context.object_detections = detections


class ObjectTrackingStep(PipelineStep):
    """A pipeline step that tracks objects in an image.
    """

    def __init__(self, algorithm: DistanceAlgorithm, distance_threshold: float, active_classes: List[str] or str):
        self.algorithm = algorithm
        self.distance_threshold = distance_threshold
        self.function = self.track
        if isinstance(active_classes, str):
            self.active_classes = [active_classes]
        else:
            self.active_classes = active_classes
    
    def track(self, context: ApplicationContext) -> None:
        """Tracks objects in the image.
        """
        if context.object_detections is None:
            raise ValueError('Tracking step cannot be executed before detection step')
        
        new_keys = []
        matched_keys = []
        unmatched_keys = []
        deleted_objects = {}
        for class_name in self.active_classes:
            detections_of_interest = [detection for detection in context.object_detections if detection.label == class_name]
            objects_of_interest = {key: obj for key, obj in context.trackable_objects.items() if obj.class_name == class_name}
            tracked_object_type = context.tracked_object_classes[class_name]
            movement_predictor_type = context.movement_predictors_by_class[class_name]

            if len(objects_of_interest) == 0:
                for detection in detections_of_interest:
                    key = str(uuid4())
                    new_keys.append(key)
                    context.trackable_objects[key] = tracked_object_type.from_detection(detection, movement_predictor_type(), context.frame_number)
                continue
            
            if len(detections_of_interest) == 0:
                for key, obj in objects_of_interest.items():
                    if context.frame_number - obj.last_seen > context.delete_after_by_class[class_name]:
                        deleted_objects[key] = obj
                    else:
                        unmatched_keys.append(key)
                continue
            
            keys = list(objects_of_interest.keys())
            distances = []
            for obj in objects_of_interest.values():
                obj_distances = []
                for detection in detections_of_interest:
                    obj_distances.append(self.algorithm.distance(obj, detection))
                distances.append(obj_distances)
            
            distance_matrix = np.array(distances, dtype=np.float32)
            distance_flattened = distance_matrix.flatten()
            min_indices = np.argsort(distance_flattened)

            used_rows = set()
            used_cols = set()
            for index in min_indices:
                row, col = np.unravel_index(index, distance_matrix.shape)
                if row in used_rows or col in used_cols:
                    continue
                if distance_matrix[row, col] > self.distance_threshold:
                    break
                key = keys[row]
                detection = detections_of_interest[col]
                matched_keys.append(key)
                context.trackable_objects[key].update(detection, context.frame_number)
                used_rows.add(row)
                used_cols.add(col)
            
            unused_rows = set(range(distance_matrix.shape[0])) - used_rows
            unused_cols = set(range(distance_matrix.shape[1])) - used_cols

            for row in unused_rows:
                key = keys[row]
                obj = objects_of_interest[key]
                if context.frame_number - obj.last_seen > context.delete_after_by_class[class_name]:
                    deleted_objects[key] = obj
                else:
                    unmatched_keys.append(key)
            for col in unused_cols:
                key = str(uuid4())
                new_keys.append(key)
                context.trackable_objects[key] = tracked_object_type.from_detection(detections_of_interest[col], key, context.frame_number)
        
        for key in deleted_objects:
            del context.trackable_objects[key]
        context.new_keys = new_keys
        context.matched_keys = matched_keys
        context.unmatched_keys = unmatched_keys
        context.deleted_objects = deleted_objects
