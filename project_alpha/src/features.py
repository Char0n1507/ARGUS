import numpy as np
from scapy.all import IP, TCP, UDP
import logging

logger = logging.getLogger(__name__)

class FeatureExtractor:
    """
    Extracts numerical features from raw packets for ML processing.
    """
    def __init__(self, vector_dim=4):
        self.vector_dim = vector_dim

    def extract(self, packet):
        """
        Extract features from a single Scapy packet.
        Returns a numpy array of shape (1, vector_dim).
        Features: [Size, Protocol, DstPort, TCP_Flags]
        """
        try:
            # 1. Packet Size
            size = len(packet)

            # 2. Protocol (TCP=6, UDP=17, Others=0)
            proto = 0
            if IP in packet:
                proto = packet[IP].proto
            
            # 3. Destination Port
            dport = 0
            if TCP in packet:
                dport = packet[TCP].dport
            elif UDP in packet:
                dport = packet[UDP].dport
            
            # 4. TCP Flags (bitmask)
            flags = 0
            if TCP in packet:
                # Scapy flags are string 'SA', 'PA', etc. 
                # We can cast to int if we want the byte value, but for simplicity let's just use the int value
                flags = int(packet[TCP].flags)
            
            # Create vector
            vector = np.array([size, proto, dport, flags], dtype=np.float32)
            
            # Basic Min-Max Scalling (Crucial for Neural Networks)
            # Size [0-1500], Proto [0-255], Dport [0-65535], Flags [0-255]
            normalized_vector = vector / np.array([1500.0, 255.0, 65535.0, 255.0], dtype=np.float32)

            return normalized_vector.reshape(1, -1)
            
        except Exception as e:
            logger.debug(f"Error extracting features: {e}")
            return np.zeros((1, self.vector_dim), dtype=np.float32)
