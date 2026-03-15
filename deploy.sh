#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


echo "Running tests..."
cd /home/dave/Sites/spudooli.com
sudo -u dave python3 -m pytest || { echo "Tests failed, aborting deploy"; exit 1; }

echo "Copying the app..."

cp /home/dave/Sites/spudooli.com/spudoolicom/*.py /var/www/spudooli/spudoolicom/


echo "Deploying the static assets..."

cp -r /home/dave/Sites/spudooli.com/spudoolicom/static/* /var/www/spudooli/spudoolicom/static/

echo "Deploying the templates..."
cp -r /home/dave/Sites/spudooli.com/spudoolicom/templates/* /var/www/spudooli/spudoolicom/templates/

echo "Minify the CSS and Javascript..."
python3 -m rcssmin < /home/dave/Sites/spudooli.com/spudoolicom/static/style.css > /var/www/spudooli/spudoolicom/static/style.css
python3 -m rcssmin < /home/dave/Sites/spudooli.com/spudoolicom/static/leaflet.css > /var/www/spudooli/spudoolicom/static/leaflet.css
python3 -m rjsmin < /home/dave/Sites/spudooli.com/spudoolicom/static/js/superfish.js > /var/www/spudooli/spudoolicom/static/js/superfish.js

echo "Clearing the cache..."
rm -rf /var/www/spudooli/spudoolicom/__pycache__

echo "Restarting Gunicorn..."
systemctl restart www.spudooli.com.service

sleep 2 && systemctl is-active www.spudooli.com.service || echo "WARNING: service may not be running"

echo "Done"
