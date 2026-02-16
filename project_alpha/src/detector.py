import numpy as np
import logging
import json
import time
from .features import FeatureExtractor
from .sniffer import PacketSniffer
from .autoencoder import AutoEncoder
from .cli_rich import print_alert
from project_alpha.src.database import ForensicDB
from project_alpha.src.geoip import GeoEnricher
import re

logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self, interface, model_path=None):
        self.interface = interface
        self.model_path = model_path
        self.db = ForensicDB()
        self.geo = GeoEnricher()
        self.sniffer = None
        self.feature_extractor = FeatureExtractor()
        self.model = AutoEncoder()
        
        # Load model if exists, else we need to train
        try:
            self.model.load(model_path)
        except:
            logger.warning(f"Model {model_path} not found. You must train first.")

    def train_mode(self, packet_count=1000):
        """
        Capture packets, extract features, and train the model.
        """
        logger.info(f"Starting Training Mode. Capturing {packet_count} packets...")
        
        captured_data = []
        
        def train_callback(packet):
            vec = self.feature_extractor.extract(packet)
            captured_data.append(vec)
            if len(captured_data) % 100 == 0:
                logger.info(f"Collected {len(captured_data)}/{packet_count} packets")

        sniffer = PacketSniffer(self.interface, callback=train_callback)
        sniffer.start()
        
        # Wait until we have enough packets
        try:
            while len(captured_data) < packet_count:
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Training interrupted by user.")
            
        sniffer.stop()
        
        if len(captured_data) > 0:
            logger.info("Processing data for training...")
            data_matrix = np.vstack(captured_data)
            self.model.train(data_matrix)
            self.model.save(self.model_path)
            logger.info("Model training complete and saved.")
        else:
            logger.error("No data collected. Training aborted.")

    def detect_mode(self):
        """
        Real-time detection loop.
        """
        if self.model.model is None:
            logger.error("Model not loaded. Please train first.")
            return

        logger.info(f"Starting Detection Mode on {self.interface}...")
        logger.info(f"Anomaly Threshold: {self.model.threshold}")
        
        def detect_callback(packet):
            vec = self.feature_extractor.extract(packet)
            loss = self.model.predict(vec)
            
            if loss[0] > self.model.threshold:
                self._alert(packet, loss[0])

        sniffer = PacketSniffer(self.interface, callback=detect_callback)
        sniffer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Detection stopped.")
            sniffer.stop()

    def _alert(self, packet, score):
        """
        Handle an anomaly alert.
        """
        alert_msg = {
            "timestamp": time.time(),
            "type": "Zero-Day Anomaly",
            "score": float(score),
            "threshold": float(self.model.threshold),
            "summary": packet.summary() if packet else "Unknown"
        }
        logger.critical(json.dumps(alert_msg))
        # Try to extract an IP address from the summary (Regex magic)
        # Finds first public-looking IP
        ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', alert_msg['summary'])
        if ip_match:
            ip = ip_match.group(0)
            location = self.geo.get_location(ip)
            alert_msg['country'] = location['country']
            alert_msg['city'] = location['city']
            alert_msg['lat'] = location.get('lat', 0.0)
            alert_msg['lon'] = location.get('lon', 0.0)
        else:
            alert_msg['country'] = "Unknown"
            alert_msg['city'] = "Unknown"
            alert_msg['lat'] = 0.0
            alert_msg['lon'] = 0.0

        # 1. Log to File (JSON)
        with open("anomalies.json", "a") as f:
            f.write(json.dumps(alert_msg) + "\n")
        
        # 2. Log to SQL Database (Enterprise Feature)
        self.db.log_anomaly(alert_msg)
            
        # 3. Rich CLI Output
        try:
            print_alert(alert_msg)
        except:
            pass
