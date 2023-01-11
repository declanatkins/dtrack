from typing import Callable, Iterable
from ..context import ApplicationContext
from .arguments import PipelineArgument


class PipelineStep:
    """A callable object that can be used in a pipeline. Instead of creating this class
        directly, use the pipeline_step decorator.

    """

    def __init__(self, name: str, function: Callable, *args: Iterable[PipelineArgument]):
        self.name = name
        self.function = function
        self.args = args
    
    def __call__(self, context: ApplicationContext):
        args = [arg.evaluate(context) for arg in self.args]
        return self.function(*args)


def pipeline_step(name: str, *args: Iterable[PipelineArgument]):
    """A decorator that can be used to create a pipeline step.
    """
    def wrapper(function):
        return PipelineStep(name, function, *args)
    return wrapper
