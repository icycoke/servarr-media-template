import os
import time
import requests

SONARR_URL = os.getenv("SONARR_URL", "http://sonarr:8989")
RADARR_URL = os.getenv("RADARR_URL", "http://radarr:7878")
LIDARR_URL = os.getenv("LIDARR_URL", "http://lidarr:8686")

SONARR_KEY = os.getenv("SONARR_API_KEY")
RADARR_KEY = os.getenv("RADARR_API_KEY")
LIDARR_KEY = os.getenv("LIDARR_API_KEY")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))

def clean_queue(service_name, base_url, api_key):
    if not api_key or api_key.startswith("your_"):
        return
    headers = {"X-Api-Key": api_key}
    try:
        res = requests.get(f"{base_url}/api/v3/queue", headers=headers, timeout=10)
        if res.status_code != 200:
            return
        items = res.json().get("records", [])
        for item in items:
            status = item.get("status", "").lower()
            tracked_status = item.get("trackedDownloadStatus", "").lower()
            if status == "warning" or tracked_status == "warning":
                item_id = item.get("id")
                requests.delete(
                    f"{base_url}/api/v3/queue/{item_id}",
                    headers=headers,
                    params={"removeFromClient": "true", "blocklist": "true"},
                    timeout=10
                )
                print(f"[{service_name}] Evicted stalled download item: {item_id}")
    except Exception as e:
        print(f"[{service_name}] Queue cleaner error: {e}")

if __name__ == "__main__":
    print("Queue Cleaner daemon running...")
    while True:
        clean_queue("Sonarr", SONARR_URL, SONARR_KEY)
        clean_queue("Radarr", RADARR_URL, RADARR_KEY)
        clean_queue("Lidarr", LIDARR_URL, LIDARR_KEY)
        time.sleep(CHECK_INTERVAL)
