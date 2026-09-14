# Automated Media Server Stack

A complete, self-hosted media ecosystem powered by Docker Compose. Includes streaming services, automated media organizers, indexer aggregation, and download queue managers.

---

## Quick Setup Guide

### 1. Configure Environment
Copy the example environment file:
  cp .env.example .env

Open `.env` and configure:
* PUID / PGID: Set to your Linux user ID (run `id` in your shell).
* CONFIG_DIR: Absolute path on your SSD to store application configurations.
* MEDIA_DIR: Absolute mount path of your main media storage array.
* SERVER_IP / HOST_IP: Your server local LAN IP.

### 2. Prepare Storage Directories
Ensure the base directory skeleton exists on your storage drive:
  mkdir -p ${MEDIA_DIR}/downloads/{sonarr,radarr,lidarr}
  mkdir -p ${MEDIA_DIR}/{movies,tv-shows,anime,music}

### 3. Start Containers
  docker compose up -d

### 4. Post-Install API Keys
1. Open Sonarr (http://<SERVER_IP>:8989) -> Settings -> General -> Copy API Key.
2. Open Radarr (http://<SERVER_IP>:7878) -> Settings -> General -> Copy API Key.
3. Open Lidarr (http://<SERVER_IP>:8686) -> Settings -> General -> Copy API Key.
4. Paste the keys into `.env` and reload the cleaner daemon:
  docker compose restart queue-cleaner

---

## Service Port Reference

| Service | Port | Description |
| :--- | :--- | :--- |
| Homepage | 3000 | Central Dashboard |
| Jellyfin | 8096 | Streaming Server |
| Jellyseerr | 5055 | Media Requests |
| Sonarr | 8989 | TV & Anime Manager |
| Radarr | 7878 | Movie Manager |
| Lidarr | 8686 | Music Manager |
| Bazarr | 6767 | Subtitle Fetcher |
| Prowlarr | 9696 | Indexer Manager |
| Navidrome | 4533 | Music Streaming Server |
| rdtclient | 6500 | Real-Debrid / Downloader WebUI |

### 5. Configure Real-Debrid (rdt-client)
1. Obtain your API Token:
   https://real-debrid.com/apitoken
2. Open rdt-client WebUI:
   http://\<SERVER_IP\>:6500
3. Go to Settings -> Provider:
   - Select Provider: RealDebrid
   - Paste your API Token
4. Go to Settings -> Downloader:
   - Download Client: Internal Downloader
   - Save Path: /media/downloads
5. Save settings. rdt-client now handles cached torrents via Real-Debrid for Sonarr and Radarr.
