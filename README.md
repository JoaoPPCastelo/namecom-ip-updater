# namecom-ip-updater
Image to check for the host's public IP and update a DNS record on name.com

## How to use
```bash
docker run -d \
  -e NAMECOM_USERNAME="your_namecom_username" \
  -e NAMECOM_API_TOKEN="your_api_token" \
  -e DOMAIN_NAME="example.com" \
  -e RECORD_ID="12345678" \
  -e DNS_HOST="@" \
  -e CHECK_INTERVAL="300" \
  joaoppcastelo/namecom-ip-updater:<tag>
```
