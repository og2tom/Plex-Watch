# PlexWatch

A lightweight Python script that monitors your media directories and automatically triggers Plex library updates when changes are detected.

## Why PlexWatch?

Plex's built-in library monitoring can be unreliable, especially with network-mounted storage (NFS, SMB, etc.). PlexWatch solves this by providing a simple, reliable alternative that works with any storage type.

## Features

- 🔍 Monitors multiple directories for changes
- 🔄 Automatically triggers Plex library updates
- 🪶 Lightweight - uses only Python standard library
- 📝 Detailed logging
- ⚡ Configurable check intervals
- 🚫 Ignores temporary files
- 🔧 Easy to set up and configure

## Requirements

- Python 3.x
- Access to Plex Media Server
- Plex authentication token

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/plexwatch.git
cd plexwatch
```

2. Copy the script to your preferred location:
```bash
sudo mkdir -p /opt/plexwatch
sudo cp plexwatch.py /opt/plexwatch/
sudo chmod +x /opt/plexwatch/plexwatch.py
```

3. Edit the configuration section in `plexwatch.py`:
```python
# Your Plex server URL
PLEX_URL = "http://localhost:32400"

# Your Plex token (see instructions below)
PLEX_TOKEN = "YOUR_PLEX_TOKEN_HERE"

# Directories to monitor
WATCH_PATHS = {
    "/path/to/movies": "Movies",
    "/path/to/tv": "TV Shows",
    "/path/to/music": "Music"
}
```

4. Test the script:
```bash
python3 /opt/plexwatch/plexwatch.py
```

## Finding Your Plex Token

1. Sign into your Plex account in Plex Web App
2. Browse to a library item and click the three dots → "Get Info"
3. Click "View XML" at the bottom of the dialog
4. Check the URL for `X-Plex-Token=`

Or follow the official guide: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

## Running as a Service

### Using systemd (Recommended)

1. Create the service file:
```bash
sudo nano /etc/systemd/system/plexwatch.service
```

2. Add the following content:
```ini
[Unit]
Description=PlexWatch - Plex Library Monitor
After=network.target plex.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/plexwatch/plexwatch.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable plexwatch
sudo systemctl start plexwatch
```

4. Check the status:
```bash
sudo systemctl status plexwatch
sudo journalctl -u plexwatch -f
```

## Troubleshooting

### Script exits immediately
- Check that your Plex token is correctly configured
- Verify Plex is running and accessible
- Check the logs for error messages

### Libraries not found
- Ensure the paths in `WATCH_PATHS` match exactly what's configured in Plex
- Check for case sensitivity
- Verify the directories exist and are accessible

### Changes not detected
- Ensure the script has read permissions for monitored directories
- Check the logs to see if the script is running
- Try reducing `CHECK_INTERVAL` for faster detection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for reliable Plex library monitoring
- Thanks to the Plex community for API documentation
