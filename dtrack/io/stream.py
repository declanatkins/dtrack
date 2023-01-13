from abc import ABC, abstractmethod
from ..util import Image


class ImageStream(ABC):
    """An abstract base class for image streams.
    """
    def __init__(self):
        self.current_image = None
    
    @abstractmethod
    def _advance(self) -> None:
        raise NotImplementedError
    
    def __iter__(self):
        return self

    def __next__(self) -> Image:
        self._advance()
        if self.current_image is None:
            raise StopIteration
        return self.current_image
