# Automated Media Server Stack

A complete, self-hosted media ecosystem powered by Docker Compose. Includes streaming services, automated media organizers, indexer aggregation, Real-Debrid ingestion, and download queue managers.

---

## Directory Structure

```text
.
|-- config/
|   |-- homepage/
|   |   |-- services.yaml
|   |   `-- widgets.yaml
|   `-- prowlarr-limiter/
|       `-- default.conf
|-- docker-compose.yml
|-- .env.example
|-- .gitignore
|-- README.md
`-- scripts/
    `-- queue_cleaner.py
```

---

## Quick Setup Guide

### 1. Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```

Open `.env` and configure:
* `PUID` / `PGID`: Set to your Linux user ID (run `id` in your shell to check).
* `CONFIG_DIR`: Absolute path on your SSD to store application configurations.
* `MEDIA_DIR`: Absolute mount path of your main media storage array.
* `SERVER_IP` / `HOST_IP`: Your server local LAN IP.

### 2. Prepare Storage Directories
Ensure the base download and media directory skeleton exists on your storage drive:
```bash
mkdir -p ${MEDIA_DIR}/downloads/{sonarr,radarr,lidarr}
mkdir -p ${MEDIA_DIR}/{movies,tv-shows,anime,music}
```

### 3. Initialize Homepage Config
Ensure the pre-configured Homepage templates are copied to your persistent config directory before starting:
```bash
mkdir -p ${CONFIG_DIR}/homepage
cp -r config/homepage/* ${CONFIG_DIR}/homepage/
```

### 4. Start Containers
```bash
docker compose up -d
```

### 5. Post-Install API Keys
1. Open **Sonarr** (`http://<SERVER_IP>:8989`) -> `Settings` -> `General` -> Copy `API Key`.
2. Open **Radarr** (`http://<SERVER_IP>:7878`) -> `Settings` -> `General` -> Copy `API Key`.
3. Open **Lidarr** (`http://<SERVER_IP>:8686`) -> `Settings` -> `General` -> Copy `API Key`.
4. Paste the keys into `.env` and restart the queue-cleaner daemon:
```bash
docker compose restart queue-cleaner
```

### 6. Configure Real-Debrid (rdt-client)
1. Obtain your API Token from Real-Debrid:
   [https://real-debrid.com/apitoken](https://real-debrid.com/apitoken)
2. Open rdt-client WebUI:
   `http://<SERVER_IP>:6500`
3. Navigate to **Settings -> Provider**:
   * Select Provider: `RealDebrid`
   * Paste your API Token
4. Navigate to **Settings -> Downloader**:
   * Download Client: `Internal Downloader`
   * Save Path: `/media/downloads`
5. Save settings. rdt-client now handles cached torrents via Real-Debrid for Sonarr and Radarr.

---

## Service Port Reference

| Service | Port | Description |
| :--- | :--- | :--- |
| **Homepage** | `3000` | Central Dashboard |
| **Jellyfin** | `8096` | Media Streaming Server |
| **Jellyseerr** | `5055` | Media Requests |
| **Sonarr** | `8989` | TV & Anime Manager |
| **Radarr** | `7878` | Movie Manager |
| **Lidarr** | `8686` | Music Manager |
| **Bazarr** | `6767` | Subtitle Fetcher |
| **Prowlarr** | `9696` | Indexer Manager |
| **Navidrome** | `4533` | Music Streaming Server |
| **rdtclient** | `6500` | Real-Debrid / Downloader WebUI |
| **FlareSolverr** | `8191` | Cloudflare Bypass Proxy |
