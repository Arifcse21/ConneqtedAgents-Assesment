import requests
import time
import random
from datetime import datetime
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
TRAFFIC_URL = f"{API_URL}/traffic"
COUNT_URL = f"{API_URL}/traffic/count"
CLEAN_URL = f"{API_URL}/clean"


LOCATIONS = ["LOC-001", "LOC-002", "LOC-003", "LOC-004", "LOC-005"]
CONGESTION_LEVELS = ["low", "medium", "high"]
MAX_DATA_POINTS = 5000

def generate_traffic_data():
    return {
        "location_id": random.choice(LOCATIONS),
        "vehicle_count": random.randint(0, 200),
        "average_speed": round(random.uniform(10.0, 100.0), 2),
        "congestion_level": random.choice(CONGESTION_LEVELS),
        "timestamp": datetime.utcnow().isoformat()
    }

def get_current_count():
    try:
        response = requests.get(COUNT_URL)
        if response.status_code == 200:
            return response.json().get("count", 0)
    except Exception as e:
        print(f"[{datetime.now()}] Error checking count: {e}")
    return 0

def clean_data():
    """Calls the /clean API to truncate the dataset."""
    try:
        print(f"[{datetime.now()}] Data limit reached. Cleaning database...")
        response = requests.post(CLEAN_URL, json={"command": "sudo"})
        if response.status_code == 200:
            print(f"[{datetime.now()}] Database cleaned successfully.")
            return True
        else:
            print(f"[{datetime.now()}] Failed to clean database: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[{datetime.now()}] Error during cleaning: {e}")
    return False

def main():

    print(f"Starting capped traffic data ingestion (Limit: {MAX_DATA_POINTS})...")
    while True:
        try:
            current_count = get_current_count()
            
            if current_count >= MAX_DATA_POINTS:
                if clean_data():
                    # After cleaning, we continue immediately to ingest new data
                    current_count = 0 
                else:
                    print(f"[{datetime.now()}] Limit reached but cleaning failed ({current_count}/{MAX_DATA_POINTS}). Waiting...")
                    time.sleep(60)
                    continue

            data = generate_traffic_data()
            response = requests.post(TRAFFIC_URL, json=data)
            if response.status_code == 200:
                print(f"[{datetime.now()}] Ingested data ({current_count + 1}/{MAX_DATA_POINTS}) for {data['location_id']}")
            else:
                print(f"[{datetime.now()}] Failed to ingest data: {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now()}] Error: {e}")
        
        # Ingest every 1-5 seconds
        time.sleep(random.randint(1, 5))

if __name__ == "__main__":
    main()
