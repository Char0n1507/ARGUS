import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.losses import MeanSquaredError
import numpy as np
import logging
from .model_base import ModelBase

logger = logging.getLogger(__name__)

class AutoEncoder(ModelBase):
    def __init__(self):
        self.model = None
        self.threshold = None

    def build(self, input_dim):
        """
        Builds a simple Autoencoder network.
        Input -> Encoder -> Latent -> Decoder -> Output
        """
        input_layer = Input(shape=(input_dim,))
        
        # Encoder
        encoded = Dense(8, activation='relu')(input_layer)
        encoded = Dense(4, activation='relu')(encoded)
        
        # Latent Space (bottleneck)
        latent = Dense(2, activation='relu')(encoded)
        
        # Decoder
        decoded = Dense(4, activation='relu')(latent)
        decoded = Dense(8, activation='relu')(decoded)
        output_layer = Dense(input_dim, activation='sigmoid')(decoded) # Normalized inputs 0-1
        
        self.model = Model(inputs=input_layer, outputs=output_layer)
        self.model.compile(optimizer='adam', loss='mse')
        logger.info("Autoencoder model built.")
        return self.model

    def train(self, data, epochs=20, batch_size=32):
        """
        Train the autoencoder. 
        Data should be normalized.
        """
        if self.model is None:
            self.build(data.shape[1])
            
        logger.info(f"Training on {len(data)} samples...")
        history = self.model.fit(
            data, data,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            validation_split=0.1,
            verbose=1
        )
        
        # Calculate threshold based on training loss (e.g., max MSE on training set)
        reconstructions = self.model.predict(data)
        train_loss = tf.keras.losses.mse(reconstructions, data)
        self.threshold = np.mean(train_loss) + 2 * np.std(train_loss)
        logger.info(f"Training complete. Anomaly Threshold set to: {self.threshold:.6f}")
        return history

    def predict(self, data):
        """
        Returns the reconstruction error for the input data.
        Higher error = more likely to be an anomaly.
        """
        if self.model is None:
            logger.error("Model not loaded/trained.")
            return None
            
        reconstructions = self.model.predict(data, verbose=0)
        loss = tf.keras.losses.mse(reconstructions, data)
        return loss.numpy()

    def save(self, path):
        if self.model:
            self.model.save(path)
            # Save threshold alongside (simple text file for now, or json)
            with open(path + ".threshold", "w") as f:
                f.write(str(self.threshold))
            logger.info(f"Model saved to {path}")

    def load(self, path):
        try:
            self.model = load_model(path)
            # Load threshold
            try:
                with open(path + ".threshold", "r") as f:
                    self.threshold = float(f.read().strip())
            except:
                self.threshold = 0.05 # Default fallback
                
            logger.info(f"Model loaded from {path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
