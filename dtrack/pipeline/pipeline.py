from ..context import ApplicationContext
from .step import PipelineStep



class Pipeline:
    """A pipeline that contains a sequence of pipeline steps.
    """

    def __init__(self, name: str):
        self.name = name
        self.steps = []
    
    def add_step(self, step: PipelineStep):
        """Adds a pipeline step to the pipeline.
        """
        self.steps.append(step)
    
    def run(self, context: ApplicationContext) -> ApplicationContext:
        """Runs the pipeline.
        """
        for step in self.steps:
            context.pipeline_step_results[step.name] = step(context)
        return context
    
    def __str__(self) -> str:
        header = f'Pipeline {self.name!r}:'
        steps = '\n'.join([f'{step}' for step in self.steps])
        return f'{header}\n{steps}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name!r})'
