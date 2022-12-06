import threading


class Singleton(type):
    """
    Singleton metaclass. This class is thread-safe.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        with cls._instances_lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
