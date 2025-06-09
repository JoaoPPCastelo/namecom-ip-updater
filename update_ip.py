import os
import time
import requests
import re
import logging
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)

# Configuration from environment
NAMECOM_USERNAME = os.getenv("NAMECOM_USERNAME")
NAMECOM_API_TOKEN = os.getenv("NAMECOM_API_TOKEN")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")
RECORD_ID = os.getenv("RECORD_ID")
DNS_HOST = os.getenv("DNS_HOST", "@")
INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))  # in seconds

# Validate environment
missing = []
if not NAMECOM_USERNAME:
    missing.append("NAMECOM_USERNAME")
if not NAMECOM_API_TOKEN:
    missing.append("NAMECOM_API_TOKEN")
if not DOMAIN_NAME:
    missing.append("DOMAIN_NAME")
if not RECORD_ID:
    missing.append("RECORD_ID")

if missing:
    logging.error(f"Missing required environment variables: {', '.join(missing)}")
    exit(1)

IPV4_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        response.raise_for_status()
        ip = response.text.strip()
        if IPV4_PATTERN.match(ip):
            return ip
        logging.warning(f"Invalid IP format received: {ip}")
    except RequestException as e:
        logging.warning(f"Could not fetch public IP: {e}")
    return None

def update_namecom_record(new_ip):
    url = f"https://api.name.com/v4/domains/{DOMAIN_NAME}/records/{RECORD_ID}"
    auth = (NAMECOM_USERNAME, NAMECOM_API_TOKEN)
    data = {
        "host": DNS_HOST,
        "type": "A",
        "answer": new_ip,
        "ttl": 300
    }
    try:
        response = requests.put(url, json=data, auth=auth, timeout=10)
        response.raise_for_status()
        logging.info(f"DNS record updated to {new_ip}")
    except RequestException as e:
        logging.error(f"Failed to update DNS record: {e}")

def main():
    logging.info(f"Starting namecom-ip-updater for domain {DOMAIN_NAME} with host {DNS_HOST}")
    last_ip = None
    while True:
        current_ip = get_public_ip()
        if current_ip and current_ip != last_ip:
            logging.info(f"IP change detected: {last_ip} → {current_ip}")
            update_namecom_record(current_ip)
            last_ip = current_ip
        elif current_ip:
            logging.info(f"IP unchanged: {current_ip}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
