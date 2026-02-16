import sqlite3
import json
import time
from datetime import datetime

class ForensicDB:
    def __init__(self, db_path="forensics.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create Anomalies Table
        c.execute('''CREATE TABLE IF NOT EXISTS anomalies
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp REAL,
                      human_time TEXT,
                      src_ip TEXT,
                      dst_ip TEXT,
                      protocol TEXT,
                      score REAL,
                      threshold REAL,
                      country TEXT,
                      city TEXT,
                      lat REAL,
                      lon REAL,
                      raw_summary TEXT)''')
        
        conn.commit()
        conn.close()

    def log_anomaly(self, alert_json):
        """
        Parses the alert JSON and stores structured data.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Parse basic fields from summary string (Simple heuristic)
        # Summary format: "Ether / IP / TCP 1.2.3.4:443 > 5.6.7.8:80 ..."
        # This is a bit fragile, but works for PoC. In prod, we'd pass raw fields.
        
        src_ip = "Unknown"
        dst_ip = "Unknown"
        proto = "Unknown"
        
        try:
            parts = alert_json['summary'].split()
            if "IP" in parts:
                ip_idx = parts.index("IP")
                # Scapy summary varies, but let's try to extract if possible
                pass
        except:
            pass

        # For now, we will store the raw summary and the enriched GeoIP data
        # GeoIP enrichment happens before calling this, or we can do it here?
        # Let's assume enrichment is passed in alert_json if available
        
        country = alert_json.get('country', 'Unknown')
        city = alert_json.get('city', 'Unknown')
        lat = alert_json.get('lat', 0.0)
        lon = alert_json.get('lon', 0.0)
        
        human_time = datetime.fromtimestamp(alert_json['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

        c.execute("INSERT INTO anomalies (timestamp, human_time, score, threshold, country, city, lat, lon, raw_summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (alert_json['timestamp'], human_time, alert_json['score'], alert_json['threshold'], country, city, lat, lon, alert_json['summary']))
        
        conn.commit()
        conn.close()

    def get_recent(self, limit=50):
        conn = sqlite3.connect(self.db_path)
        import pandas as pd
        df = pd.read_sql_query(f"SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT {limit}", conn)
        conn.close()
        return df
