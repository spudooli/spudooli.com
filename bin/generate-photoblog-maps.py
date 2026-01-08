#!/usr/bin/env python3
import sys
import os
import requests
import time

# Ensure we can import the spudoolicom application
# Assuming this script is located in /bin/ relative to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Hack: Mock RotatingFileHandler to avoid PermissionError on /tmp/spud.log
# This usually happens if the log file is owned by another user (e.g. root/www-data)
import logging
import logging.handlers
if not os.access('/tmp/spud.log', os.W_OK) and os.path.exists('/tmp/spud.log'):
    print("Warning: /tmp/spud.log is not writable. Disabling file logging.")
    original_handler = logging.handlers.RotatingFileHandler
    def mock_handler(*args, **kwargs):
        return logging.NullHandler()
    logging.handlers.RotatingFileHandler = mock_handler

from spudoolicom import app, db

def generate_maps():
    """
    Connects to the database, pulls all pixelpost records where googlemap is not null,
    generates a static map image for each post using a local tile server,
    and stores the image in the static/images/photoblogmaps directory.
    """
    print("Starting map generation...")
    
    # Use app context to access the database
    with app.app_context():
        # Define the output directory
        # The user requested: /var/www/spudooli/spudoolicom/static/images/photoblogmaps/
        output_dir = '/var/www/spudooli/spudoolicom/static/images/photoblogmaps/'
        
        # Ensure the directory exists
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"Created directory: {output_dir}")
            except OSError as e:
                print(f"Error creating directory {output_dir}: {e}")
                return

        # Query posts from pixelpost where googlemap is present
        try:
            cursor = db.mysql.connection.cursor()
            # Select id and googlemap string. 
            # We filter for non-null and non-empty googlemap fields.
            query = "SELECT id, googlemap FROM pixelpost_pixelpost WHERE googlemap IS NOT NULL AND googlemap != ''"
            cursor.execute(query)
            posts = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"Database error: {e}")
            return

        print(f"Found {len(posts)} posts to process.")

        for post in posts:
            post_id = post[0]
            googlemap_str = post[1]
            
            # Parse lat/lon from the string
            # format example: "(lat, lon)" 
            try:
                # Clean up format "(lat, lon)" -> "lat, lon"
                latlon = googlemap_str.replace('(', '').replace(')', '')
                parts = latlon.split(',')
                
                if len(parts) >= 2:
                    lat = parts[0].strip()
                    lon = parts[1].strip()
                else:
                    # Skip if format is unexpected
                    # print(f"Skipping post {post_id}: Invalid location format '{googlemap_str}'")
                    continue
            except Exception as e:
                print(f"Error parsing location for post {post_id}: {e}")
                continue

            # Construct the tile server URL
            # Requested URL: http://localhost:8080/styles/OSM%20OpenMapTiles/static/{lon},{lat},16/350x300.png?marker={lon},{lat}|marker-icon.png|scale:0.75
            map_url = f"http://localhost:8080/styles/OSM%20OpenMapTiles/static/{lon},{lat},16/350x300.png?marker={lon},{lat}|marker-icon.png|scale:0.75"
            
            # Define output filename
            filename = f"{post_id}.png"
            filepath = os.path.join(output_dir, filename)
            
            # Download and save the image
            try:
                # print(f"Downloading map for post {post_id} at {lat}, {lon}...")
                response = requests.get(map_url, timeout=10)
                
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved map for post {post_id} to {filepath}")
                else:
                    print(f"Failed to download map for post {post_id}: HTTP {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Network error downloading map for post {post_id}: {e}")
            except IOError as e:
                print(f"File I/O error saving map for post {post_id}: {e}")
            
    print("Map generation complete.")

if __name__ == "__main__":
    generate_maps()
