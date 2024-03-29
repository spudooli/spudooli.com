#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


echo "Copying the app..."

cp /home/dave/Sites/spudooli.com/spudoolicom/*.py /var/www/spudooli/spudoolicom/


echo "Deploying the static assets..."

cp /home/dave/Sites/spudooli.com/spudoolicom/static/* /var/www/spudooli/spudoolicom/static/
cp /home/dave/Sites/spudooli.com/spudoolicom/static/fonts/* /var/www/spudooli/spudoolicom/static/fonts/
cp /home/dave/Sites/spudooli.com/spudoolicom/static/js/* /var/www/spudooli/spudoolicom/static/js/

echo "Deploying the templates..."
cp /home/dave/Sites/spudooli.com/spudoolicom/templates/* /var/www/spudooli/spudoolicom/templates/


echo "Clearing the cache..."
rm -rf /var/www/spudooli/spudoolicom/__pycache__

echo "Restarting Gunicorn..."
systemctl restart www.spudooli.com.service

echo "Done"
