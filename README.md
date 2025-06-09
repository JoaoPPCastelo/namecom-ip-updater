# namecom-ip-updater
Image to check for the host's public IP and update a DNS record on name.com

<br>

## How to use

```bash
docker run -d \
  -e NAMECOM_USERNAME="your_namecom_username" \
  -e NAMECOM_API_TOKEN="your_api_token" \
  -e DOMAIN_NAME="example.com" \
  -e RECORD_ID="12345678" \
  -e DNS_HOST="@" \
  -e CHECK_INTERVAL="300" \
  ip-updater
```

or with compose
```yaml
version: "3.9"

services:
  ip-updater:
    image: joaoppcastelo/namecom-ip-updater:<tag>
    container_name: ip-updater
    restart: unless-stopped
    environment:
      NAMECOM_USERNAME: your_namecom_username
      NAMECOM_API_TOKEN: your_api_token
      DOMAIN_NAME: example.com
      RECORD_ID: "12345678"
      DNS_HOST: "@"
      CHECK_INTERVAL: "300"

```

## Reference
- [Name.com API Reference](https://www.name.com/api-docs/)
- [GitHub repo](https://github.com/JoaoPPCastelo/namecom-ip-updater)
- [Docker repo](https://hub.docker.com/r/joaoppcastelo/namecom-ip-updater)