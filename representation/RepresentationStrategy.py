import abc  # Python's built-in abstract class library

class RepresentationStrategy(metaclass=abc.ABCMeta):
    """You do not need to know about metaclasses.
    Just know that this is how you define abstract
    classes in Python."""
    @abc.abstractmethod
    def transform(self,seq):
        """Required Method"""
