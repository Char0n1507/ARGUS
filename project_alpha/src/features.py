import numpy as np
from scapy.all import IP, TCP, UDP
import logging

logger = logging.getLogger(__name__)

class FeatureExtractor:
    """
    Extracts numerical features from raw packets for ML processing.
    """
    def __init__(self, vector_dim=5):
        self.vector_dim = vector_dim

    def _shannon_entropy(self, data):
        """
        Calculates Shannon Entropy of bytes.
        Returns float [0.0, 8.0]
        """
        if not data:
            return 0.0
        
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * np.log2(p_x)
        return entropy

    def extract(self, packet):
        """
        Extract features from a single Scapy packet.
        Returns a numpy array of shape (1, vector_dim).
        Features: [Size, Protocol, DstPort, TCP_Flags, Entropy]
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
            payload = b""
            if TCP in packet:
                dport = packet[TCP].dport
                payload = bytes(packet[TCP].payload)
            elif UDP in packet:
                dport = packet[UDP].dport
                payload = bytes(packet[UDP].payload)
            
            # 4. TCP Flags (bitmask)
            flags = 0
            if TCP in packet:
                flags = int(packet[TCP].flags)
                
            # 5. Payload Entropy (New for Enterprise Version)
            entropy = self._shannon_entropy(payload)
            
            # Create vector
            vector = np.array([size, proto, dport, flags, entropy], dtype=np.float32)
            
            # Normalize
            # Size [1500], Proto [255], Dport [65535], Flags [255], Entropy [8.0]
            norm_scale = np.array([1500.0, 255.0, 65535.0, 255.0, 8.0], dtype=np.float32)
            normalized_vector = vector / norm_scale

            return normalized_vector.reshape(1, -1)
            
        except Exception as e:
            logger.debug(f"Error extracting features: {e}")
            return np.zeros((1, self.vector_dim), dtype=np.float32)
