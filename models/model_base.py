from abc import ABC, abstractmethod

class ModelBase(ABC):  # Abstract base class (Abstraction)
    def __init__(self, name, description ):
        self._name = name                # Encapsulation
        self._description = description

    @abstractmethod
    def run(self, input_path ):
        pass  # Must be overridden by subclasses (Polymorphism)

    def get_info(self ):
        return f"{self._name}: {self._description}"  # Info helper