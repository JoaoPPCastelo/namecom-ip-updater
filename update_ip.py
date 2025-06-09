import os
import time
import requests
import re

# Configuration from environment
NAMECOM_USERNAME = os.getenv("NAMECOM_USERNAME")
NAMECOM_API_TOKEN = os.getenv("NAMECOM_API_TOKEN")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")
RECORD_ID = os.getenv("RECORD_ID")
DNS_HOST = os.getenv("DNS_HOST", "@")
INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))  # in seconds

# Validate environment
if not all([NAMECOM_USERNAME, NAMECOM_API_TOKEN, DOMAIN_NAME, RECORD_ID]):
    raise Exception("Missing required environment variables.")

IPV4_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        response.raise_for_status()
        ip = response.text.strip()
        if IPV4_PATTERN.match(ip):
            return ip
        else:
            print(f"[ERROR] Invalid IP format: {ip}")
    except Exception as e:
        print(f"[ERROR] Failed to get public IP: {e}")
    return None

def update_namecom_record(new_ip):
    url = f"https://api.name.com/v4/domains/{DOMAIN_NAME}/records/{RECORD_ID}"
    headers = {
        "Content-Type": "application/json",
    }
    auth = (NAMECOM_USERNAME, NAMECOM_API_TOKEN)
    data = {
        "host": DNS_HOST,
        "type": "A",
        "answer": new_ip,
        "ttl": 300
    }
    try:
        response = requests.put(url, json=data, auth=auth)
        response.raise_for_status()
        print(f"[INFO] Updated DNS record to {new_ip}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to update DNS record: {e}")

def main():
    last_ip = None
    while True:
        current_ip = get_public_ip()
        if current_ip and current_ip != last_ip:
            print(f"[INFO] IP change detected: {last_ip} -> {current_ip}")
            update_namecom_record(current_ip)
            last_ip = current_ip
        else:
            print(f"[INFO] IP unchanged or invalid: {current_ip}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
