#!/usr/bin/env python3
"""
PlexWatch - Automatic Plex Library Update Monitor
https://github.com/yourusername/plexwatch

A lightweight Python script that monitors your media directories and automatically 
triggers Plex library updates when changes are detected. Perfect for setups where 
Plex's built-in monitoring doesn't work properly (e.g., with NFS/SMB mounts).
"""

import os
import time
import json
import logging
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# ====================================================================================
# CONFIGURATION - EDIT THESE SETTINGS
# ====================================================================================

# Your Plex server URL (usually http://localhost:32400 if running on same machine)
PLEX_URL = "http://localhost:32400"

# Your Plex authentication token
# To find your token: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
PLEX_TOKEN = "YOUR_PLEX_TOKEN_HERE"

# How often to check for changes (in seconds)
# Default: 60 seconds (1 minute)
CHECK_INTERVAL = 60

# Directories to monitor and their Plex library names
# Format: "path/to/directory": "Library Name in Plex"
# Make sure these paths match EXACTLY what's configured in Plex
WATCH_PATHS = {
    "/path/to/movies": "Movies",
    "/path/to/tv": "TV Shows",
    "/path/to/music": "Music"
}

# ====================================================================================
# ADVANCED SETTINGS (usually don't need to change these)
# ====================================================================================

# File to store the state between runs
STATE_FILE = "/tmp/plexwatch_state.json"

# Log file location
LOG_FILE = "/var/log/plexwatch.log"

# File patterns to ignore (temporary files, etc.)
IGNORE_PATTERNS = ['.partial~', '.tmp', '.temp', '.downloading']

# ====================================================================================
# SCRIPT CODE - Don't modify below unless you know what you're doing
# ====================================================================================

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE)
    ]
)

def make_plex_request(endpoint):
    """Make a request to the Plex API"""
    url = f"{PLEX_URL}{endpoint}"
    req = urllib.request.Request(url)
    req.add_header('X-Plex-Token', PLEX_TOKEN)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        logging.error(f"Error making Plex request: {e}")
        return None

def get_library_sections():
    """Get library sections from Plex and match them with configured paths"""
    try:
        response = make_plex_request("/library/sections")
        if not response:
            return {}
        
        # Parse XML response
        root = ET.fromstring(response)
        library_map = {}
        
        # Find all library sections
        for directory in root.findall('.//Directory'):
            section_id = directory.get('key')
            section_title = directory.get('title')
            
            # Find locations for this section
            for location in directory.findall('.//Location'):
                path = location.get('path')
                
                if path in WATCH_PATHS:
                    library_map[path] = {
                        'id': section_id,
                        'name': section_title
                    }
                    logging.info(f"Found library '{section_title}' (ID: {section_id}) for path {path}")
        
        return library_map
        
    except Exception as e:
        logging.error(f"Error parsing XML: {e}")
        import traceback
        traceback.print_exc()
        return {}

def update_library(section_id, name):
    """Trigger a library update for a specific section"""
    response = make_plex_request(f"/library/sections/{section_id}/refresh")
    if response is not None:
        logging.info(f"Updated library '{name}' (ID: {section_id})")
        return True
    else:
        logging.error(f"Failed to update library '{name}'")
        return False

def should_ignore_file(filepath):
    """Check if a file should be ignored based on patterns"""
    filename = os.path.basename(filepath)
    return any(pattern in filename for pattern in IGNORE_PATTERNS)

def get_directory_mtime(path):
    """Get the most recent modification time in a directory tree"""
    if not os.path.exists(path):
        logging.warning(f"Path does not exist: {path}")
        return 0
    
    latest_mtime = 0
    
    try:
        for root, dirs, files in os.walk(path):
            # Check directory itself
            try:
                dir_mtime = os.path.getmtime(root)
                if dir_mtime > latest_mtime:
                    latest_mtime = dir_mtime
            except OSError:
                pass
            
            # Check all files
            for file in files:
                # Skip ignored files
                if should_ignore_file(file):
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    file_mtime = os.path.getmtime(file_path)
                    if file_mtime > latest_mtime:
                        latest_mtime = file_mtime
                except OSError:
                    pass
                    
    except OSError as e:
        logging.error(f"Error scanning {path}: {e}")
    
    return latest_mtime

def load_state():
    """Load previous state from file"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Could not load state file: {e}")
    return {}

def save_state(state):
    """Save current state to file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except Exception as e:
        logging.error(f"Error saving state: {e}")

def validate_configuration():
    """Validate that the configuration is properly set"""
    if PLEX_TOKEN == "YOUR_PLEX_TOKEN_HERE":
        logging.error("ERROR: You must configure PLEX_TOKEN in the script!")
        logging.error("See: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/")
        return False
    
    if not WATCH_PATHS:
        logging.error("ERROR: No watch paths configured!")
        return False
    
    # Check if paths exist
    missing_paths = []
    for path in WATCH_PATHS:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        logging.warning("Warning: Following paths do not exist:")
        for path in missing_paths:
            logging.warning(f"  - {path}")
    
    return True

def main():
    """Main function"""
    logging.info("PlexWatch started")
    
    # Validate configuration
    if not validate_configuration():
        return 1
    
    # Test connection to Plex
    response = make_plex_request("/")
    if not response:
        logging.error("Cannot connect to Plex server at " + PLEX_URL)
        logging.error("Check that Plex is running and the URL is correct")
        return 1
    
    # Get library mappings
    library_map = get_library_sections()
    
    if not library_map:
        logging.error("No matching libraries found.")
        logging.error("Configured paths:")
        for path, name in WATCH_PATHS.items():
            logging.error(f"  - {path} (expecting library: {name})")
        logging.error("\nMake sure these paths match exactly what's configured in Plex")
        return 1
    
    logging.info(f"Monitoring {len(library_map)} libraries")
    
    # Load previous state
    last_mtimes = load_state()
    
    # Main monitoring loop
    try:
        while True:
            current_mtimes = {}
            updates_needed = []
            
            # Check each monitored path
            for path, library_info in library_map.items():
                current_mtime = get_directory_mtime(path)
                current_mtimes[path] = current_mtime
                
                # Compare with last check
                last_mtime = last_mtimes.get(path, 0)
                
                if current_mtime > last_mtime:
                    logging.info(f"Changes detected in {path}")
                    updates_needed.append(library_info)
            
            # Update libraries that have changed
            if updates_needed:
                for library in updates_needed:
                    update_library(library['id'], library['name'])
            
            # Save current state
            save_state(current_mtimes)
            last_mtimes = current_mtimes
            
            # Wait for next check
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info("PlexWatch stopped by user")
        return 0
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())