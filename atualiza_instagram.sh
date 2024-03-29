#!/bin/bash
cd /home/marcel/instagram-graph-api-dsbr
source venv/bin/activate
python3 src/main.py -f ifes.csv
#./main.py abepro.csv
#cp -f usuarios.csv pub
cp -f usernames/ifes.csv pub/usuarios.csv
cp -f pub/ifes_media_data.csv pub/instagram_media_data.csv
cp -f pub/ifes_user_data.csv pub/instagram_user_data.csv
rm -rf pub/videos/*
./convert_clean.sh
rm -f ids.csv
#AWS configuration
#rclone sync --checksum pub 360:instagram-360
#for i in pub/*.csv
#do
#	rclone copy --checksum "$i" 360:datascibr-360/360
#done

#Google Cloud Configuration
rclone sync pub instagram:power-bi-static-assets-mec-dsbr/instagram

