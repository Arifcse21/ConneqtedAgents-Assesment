import requests
import time
import random
from datetime import datetime

API_URL = "http://localhost:8000/traffic"

LOCATIONS = ["LOC-001", "LOC-002", "LOC-003", "LOC-004", "LOC-005"]
CONGESTION_LEVELS = ["low", "medium", "high"]

def generate_traffic_data():
    return {
        "location_id": random.choice(LOCATIONS),
        "vehicle_count": random.randint(0, 200),
        "average_speed": round(random.uniform(10.0, 100.0), 2),
        "congestion_level": random.choice(CONGESTION_LEVELS),
        "timestamp": datetime.utcnow().isoformat()
    }

def main():
    print("Starting real-time traffic data ingestion...")
    while True:
        try:
            data = generate_traffic_data()
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                print(f"[{datetime.now()}] Ingested data for {data['location_id']}: level {data['congestion_level']}")
            else:
                print(f"[{datetime.now()}] Failed to ingest data: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")
        
        # Ingest every 1-5 seconds as per requirements
        time.sleep(random.randint(1, 5))

if __name__ == "__main__":
    main()
