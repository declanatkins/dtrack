from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict
from ..context import ApplicationContext


class ResultFormatter(ABC):
    """Formatter for results at each frame.
    """

    @abstractmethod
    def format(self, context: ApplicationContext) -> Dict[str, Any]:
        """Formats the results of a pipeline step.

        Args:
            context (ApplicationContext): The application context.

        Returns:
            Dict[str, Any]: The formatted results.
        """
        pass


class DefaultResultFormatter(ResultFormatter):
    """The default result formatter.
    """

    def format(self, context: ApplicationContext) -> Dict[str, Any]:
        """Formats the results of a pipeline step.

        Args:
            context (ApplicationContext): The application context.

        Returns:
            Dict[str, Any]: The formatted results.
        """
        return {
            'frame_number': context.frame_number,
            'frame_timestamp': datetime.now().timestamp(),
            'pipeline_step_results': context.pipeline_step_results,
            'tracking_attributes': context.tracking_attributes
        }
