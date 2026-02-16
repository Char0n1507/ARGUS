import sqlite3
import time
import random
from datetime import datetime

DB_PATH = "forensics.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Ensure table exists (schema matches ForensicDB._init_db)
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

def populate():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    countries = ["US", "CN", "RU", "DE", "BR", "IN"]
    cities = {"US": ["New York", "Los Angeles"], "CN": ["Beijing", "Shanghai"], "RU": ["Moscow"], "DE": ["Berlin"], "BR": ["Sao Paulo"], "IN": ["Mumbai"]}
    coords = {"US": (37.0902, 95.7129), "CN": (35.8617, 104.1954), "RU": (61.5240, 105.3188), "DE": (51.1657, 10.4515), "BR": (-14.2350, -51.9253), "IN": (20.5937, 78.9629)}

    print("Populating database with sample anomalies...")
    
    for i in range(20):
        country = random.choice(countries)
        city = random.choice(cities[country])
        lat, lon = coords[country]
        # Add some jitter to coords
        lat += random.uniform(-5, 5)
        lon += random.uniform(-5, 5)
        
        timestamp = time.time() - random.randint(0, 86400) # Past 24 hours
        human_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        score = random.uniform(50, 100)
        threshold = 45.0
        
        src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        summary = f"Ether / IP / TCP {src_ip}:1234 > 192.168.1.5:80 S"

        c.execute("INSERT INTO anomalies (timestamp, human_time, src_ip, dst_ip, protocol, score, threshold, country, city, lat, lon, raw_summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (timestamp, human_time, src_ip, "192.168.1.5", "TCP", score, threshold, country, city, lat, lon, summary))
    
    conn.commit()
    conn.close()
    print("Database populated successfully.")

if __name__ == "__main__":
    init_db()
    populate()
