from abc import ABC, abstractmethod

class ModelBase(ABC):
    """
    Abstract Base Class for Anomaly Detection Models.
    Enforces a standard interface for different model types.
    """
    
    @abstractmethod
    def build(self, input_dim):
        """Build the model architecture."""
        pass

    @abstractmethod
    def train(self, data, epochs=10, batch_size=32):
        """Train the model on normal data."""
        pass

    @abstractmethod
    def predict(self, data):
        """Return reconstruction error or anomaly score."""
        pass

    @abstractmethod
    def save(self, path):
        """Save model to disk."""
        pass

    @abstractmethod
    def load(self, path):
        """Load model from disk."""
        pass
