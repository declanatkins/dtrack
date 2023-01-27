from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Type
from ..context import ApplicationContext
from ..util import Detection, Image
from ..tracking.trackable import TrackableObject


class PipelineArgument(ABC):
    """An abstract base class for pipeline arguments.
    """

    @abstractmethod
    def evaluate(self, context: ApplicationContext):
        """Evaluates the argument and returns the result.
        """
        raise NotImplementedError

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class PipelineArgumentWithSpecification(PipelineArgument):
    """An abstract base class for pipeline arguments that require a specification.
    """

    def __init__(self, specification: str):
        self.specification = specification

    def __repr__(self):
        return f'{self.__class__.__name__}({self.specification!r})'


class Image(PipelineArgument):
    """A pipeline argument that represents the current frame image.
    """

    def evaluate(self, context) -> Image:
        return context.frame_image


class AllDetections(PipelineArgument):
    """A pipeline argument that represents all object detections in the current frame.
    """

    def evaluate(self, context) -> List[Detection]:
        return context.object_detections


class AllTrackedObjects(PipelineArgument):
    """A pipeline argument that represents all tracked objects in the current frame.
    """

    def evaluate(self, context) -> List[TrackableObject]:
        return list(context.trackable_objects.values())


class AllTrackedObjectsWithKeys(PipelineArgument):
    """A pipeline argument that represents all tracked objects in the current frame with their keys.
    """

    def evaluate(self, context) -> List[Tuple[str, TrackableObject]]:
        return list(context.trackable_objects.items())


class MatchedTrackedObjects(PipelineArgument):
    """A pipeline argument that represents all tracked objects that were matched in the current frame.
    """

    def evaluate(self, context):
        return [context.trackable_objects[key] for key in context.matched_keys]


class MatchedTrackedObjectsWithKeys(PipelineArgument):
    """A pipeline argument that represents all tracked objects that were matched in the current frame with their keys.
    """

    def evaluate(self, context):
        return [(key, context.trackable_objects[key]) for key in context.matched_keys]


class UnmatchedTrackedObjects(PipelineArgument):
    """A pipeline argument that represents all tracked objects that were not matched in the current frame.
    """

    def evaluate(self, context):
        return [context.trackable_objects[key] for key in context.unmatched_keys]


class UnmatchedTrackedObjectsWithKeys(PipelineArgument):
    """A pipeline argument that represents all tracked objects that were not matched in the current frame with their keys.
    """

    def evaluate(self, context):
        return [(key, context.trackable_objects[key]) for key in context.unmatched_keys]


class NewTrackedObjects(PipelineArgument):
    """A pipeline argument that represents all tracked objects that were newly created in the current frame.
    """

    def evaluate(self, context):
        return [context.trackable_objects[key] for key in context.new_keys]


class NewTrackedObjectsWithKeys(PipelineArgument):
    """A pipeline argument that represents all tracked objects that were newly created in the current frame with their keys.
    """

    def evaluate(self, context):
        return [(key, context.trackable_objects[key]) for key in context.new_keys]


class DeletedTrackedObjects(PipelineArgument):
    """A pipeline argument that represents all tracked objects that were deleted in the current frame.
    """

    def evaluate(self, context):
        return [context.trackable_objects[key] for key in context.deleted_keys]


class DeletedTrackedObjectsWithKeys(PipelineArgument):
    """A pipeline argument that represents all tracked objects that were deleted in the current frame with their keys.
    """

    def evaluate(self, context):
        return [(key, context.trackable_objects[key]) for key in context.deleted_keys]


class FrameNumber(PipelineArgument):
    """A pipeline argument that represents the current frame number.
    """

    def evaluate(self, context) -> int:
        return context.frame_number


class TrackingAttribute(PipelineArgumentWithSpecification):
    """A pipeline argument that represents a tracking attribute.
    """

    def evaluate(self, context) -> Any:
        if self.specification not in context.tracking_attributes:
            raise ValueError(f'Tracking attribute {self.specification!r} does not exist')
        return context.tracking_attributes[self.specification]


class PipelineStepResult(PipelineArgumentWithSpecification):
    """A pipeline argument that represents a result from a previous pipeline step.
    """

    def evaluate(self, context) -> Any:
        if self.specification not in context.pipeline_results:
            raise ValueError(f'Pipeline result {self.specification!r} does not exist')
        return context.pipeline_results[self.specification]


class DetectionsOfClass(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all object detections of a specific class in the current frame.
    """

    def evaluate(self, context) -> List[Detection]:
        return [detection for detection in context.object_detections if detection.class_name == self.specification]


class TrackedObjectsOfClass(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class in the current frame.
    """

    def evaluate(self, context) -> List[TrackableObject]:
        return [trackable_object for trackable_object in context.trackable_objects.values() if trackable_object.class_name == self.specification]


class TrackedObjectsOfClassWithKeys(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class in the current frame with their keys.
    """

    def evaluate(self, context) -> List[Tuple[str, TrackableObject]]:
        return [(key, trackable_object) for key, trackable_object in context.trackable_objects.items() if trackable_object.class_name == self.specification]


class MatchedTrackedObjectsOfClass(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class that were matched in the current frame.
    """

    def evaluate(self, context):
        return [context.trackable_objects[key] for key in context.matched_keys if context.trackable_objects[key].class_name == self.specification]


class MatchedTrackedObjectsOfClassWithKeys(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class that were matched in the current frame with their keys.
    """

    def evaluate(self, context):
        return [(key, context.trackable_objects[key]) for key in context.matched_keys if context.trackable_objects[key].class_name == self.specification]


class UnmatchedTrackedObjectsOfClass(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class that were not matched in the current frame.
    """

    def evaluate(self, context):
        return [context.trackable_objects[key] for key in context.unmatched_keys if context.trackable_objects[key].class_name == self.specification]


class UnmatchedTrackedObjectsOfClassWithKeys(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class that were not matched in the current frame with their keys.
    """

    def evaluate(self, context):
        return [(key, context.trackable_objects[key]) for key in context.unmatched_keys if context.trackable_objects[key].class_name == self.specification]


class NewTrackedObjectsOfClass(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class that were newly created in the current frame.
    """

    def evaluate(self, context):
        return [context.trackable_objects[key] for key in context.new_keys if context.trackable_objects[key].class_name == self.specification]


class NewTrackedObjectsOfClassWithKeys(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class that were newly created in the current frame with their keys.
    """

    def evaluate(self, context):
        return [(key, context.trackable_objects[key]) for key in context.new_keys if context.trackable_objects[key].class_name == self.specification]


class DeletedTrackedObjectsOfClass(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class that were deleted in the current frame.
    """

    def evaluate(self, context):
        return [context.trackable_objects[key] for key in context.deleted_keys if context.trackable_objects[key].class_name == self.specification]


class DeletedTrackedObjectsOfClassWithKeys(PipelineArgumentWithSpecification):
    """A pipeline argument that represents all tracked objects of a specific class that were deleted in the current frame with their keys.
    """

    def evaluate(self, context):
        return [(key, context.trackable_objects[key]) for key in context.deleted_keys if context.trackable_objects[key].class_name == self.specification]


class TrackedObjectTypes(PipelineArgument):
    """A pipeline argument that gives the types for tracked objects of different classes.
    """

    def evaluate(self, context) -> Dict[str, Type[TrackableObject]]:
        return context.tracked_object_classes


class TrackedObjectTypeForClass(PipelineArgumentWithSpecification):
    """A pipeline argument that gives the type for tracked objects of a specific class.
    """

    def evaluate(self, context) -> Type[TrackableObject]:
        return context.tracked_object_classes[self.specification]
