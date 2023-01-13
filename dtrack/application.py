from typing import Any, Dict, List, Generator, Type, Union
from tqdm import tqdm
from .context import ApplicationContext
from .io.stream import ImageStream
from .pipeline import Pipeline
from .pipeline.arguments import PipelineArgument
from .pipeline.step import PipelineStep
from .tracking.trackable import TrackableObject
from .tracking.trackable.default_object import DefaultTrackableObject
from .util import Detection, Image
from .util.formatter import ResultFormatter, DefaultResultFormatter


class DTrackApplication:
    """A DTrack Application. When configured and fed your stream of images, it will
        execute your pipeline at each frame, and provide you with the results.
    """

    def __init__(
            self,
            tracked_class: str=None,
            tracked_classes: List[str]=None,
            application_name: str='DTrack Application',
            pipeline: Pipeline=None,
            tracked_object_class: Type[TrackableObject]=DefaultTrackableObject,
            tracked_object_classes: Union[
                List[Type[TrackableObject]],
                Dict[str, Type[TrackableObject]],
                Type[TrackableObject]
            ]=DefaultTrackableObject,
            tracking_attributes: Dict[str, Any]=None,
            result_formatter: ResultFormatter=DefaultResultFormatter()
    ):
        """Creates a new DTrack Application.

        Args:
            tracked_class (str, optional): The name of the class of objects to track. 
                Defaults to None. Either this or tracked_classes must be specified.
            tracked_classes (List[str], optional): The names of the classes of objects to track. 
                Defaults to None. Either this or tracked_class must be specified.
            application_name (str, optional): The name of the application. Defaults to 'DTrack Application'.
            pipeline (Pipeline, optional): The pipeline to execute. Defaults to None.
            tracked_object_class (Type[TrackableObject], optional): The class of tracked objects to use. 
                Used if tracked_class is specified. Defaults to DefaultTrackableObject.
            tracked_object_classes (Union[List[Type[TrackableObject]], Dict[str, Type[TrackableObject]], Type[TrackableObject]], optional): 
                The classes of tracked objects to use. Used if tracked_classes is specified. Defaults to None.
        """
        self.pipeline = pipeline
        self.application_name = application_name
        self.tracking_attributes = tracking_attributes or {}
        self.tracked_objects = {}
        self.frame_number = 0
        self.result_formatter = result_formatter

        if tracked_class is not None and tracked_classes is not None:
            raise ValueError('Only one of tracked_class or tracked_classes can be specified')
        elif tracked_class is not None:
            self.tracked_classes = [tracked_class]
            self.tracked_object_classes = {tracked_class: tracked_object_class}
        elif tracked_classes is not None:
            self.tracked_classes = tracked_classes
            if isinstance(tracked_object_classes, list):
                self.tracked_object_classes = {
                    tracked_class: tracked_object_class
                    for tracked_class, tracked_object_class in zip(tracked_classes, tracked_object_classes)
                }
            elif isinstance(tracked_object_classes, dict):
                self.tracked_object_classes = tracked_object_classes
            else:
                self.tracked_object_classes = {
                    tracked_class: tracked_object_classes
                    for tracked_class in tracked_classes
                }
        else:
            raise ValueError('One of tracked_class or tracked_classes must be specified')
    
    def process_image_stream(self, image_stream: ImageStream, progress_bar: bool=True) -> Generator[Dict[str, Any]]:
        """Processes the given image stream.

        Args:
            image_stream (ImageStream): The image stream to process.
            progress_bar (bool, optional): Whether to show a progress bar. Defaults to True.

        Yields:
            Generator[Dict[str, Any]]: The results of the pipeline steps at each frame.
        """
        if not self.pipeline:
            raise ValueError('No pipeline specified')

        if progress_bar:
            image_stream = tqdm(image_stream)

        for frame_image in image_stream:
            context = ApplicationContext(
                frame_image=frame_image,
                frame_number=self.frame_number,
                object_detections=[],
                trackable_objects=self.tracked_objects,
                matched_keys=[],
                unmatched_keys=[],
                new_keys=[],
                deleted_keys=[],
                tracking_attributes=self.tracking_attributes,
                pipeline_step_results={}
            )
            context = self.pipeline.run(context)
            self.frame_number += 1
            self.tracking_attributes = context.tracking_attributes
            yield self.result_formatter.format(context)

    def register_tracking_attribute(self, name: str, value: Any):
        """Registers a tracking attribute.

        Args:
            name (str): The name of the attribute.
            value (Any): The value of the attribute.
        """
        if name in self.tracking_attributes:
            raise ValueError(f'Tracking attribute {name} already registered')

        self.tracking_attributes[name] = value

    def get_tracking_attribute(self, name: str):
        """Gets a tracking attribute.

        Args:
            name (str): The name of the attribute.

        Returns:
            Any: The value of the attribute.
        """
        if name not in self.tracking_attributes:
            raise ValueError(f'Tracking attribute {name} not registered')

        return self.tracking_attributes[name]
    
    def set_tracking_attribute(self, name: str, value: Any):
        """Sets a tracking attribute.

        Args:
            name (str): The name of the attribute.
            value (Any): The value of the attribute.
        """
        if name not in self.tracking_attributes:
            raise ValueError(f'Tracking attribute {name} not registered')

        self.tracking_attributes[name] = value