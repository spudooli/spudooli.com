#!/bin/bash

echo "Copying the app..."

cp /home/dave/Sites/spudooli.com/spudoolicom/*.py /var/www/spudooli/spudoolicom/


echo "Deploying the static assets..."

cp /home/dave/Sites/spudooli.com/spudoolicom/static/* /var/www/spudooli/spudoolicom/static/

echo "Deploying the templates..."
cp /home/dave/Sites/spudooli.com/spudoolicom/templates/* /var/www/spudooli/spudoolicom/templates/


echo "Clearing the cache..."
rm -rf /var/www/spudooli/spudoolicom/__pycache__

echo "Done"
