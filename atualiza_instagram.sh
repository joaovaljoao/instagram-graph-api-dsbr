#!/bin/sh
cd /home/marcel/instagram-graph-api-dsbr/src
./main.py ifes.csv
#cp -f usuarios.csv pub
#./convert_clean.sh
#AWS configuration
#rclone sync --checksum pub 360:instagram-360
#for i in pub/*.csv
#do
#	rclone copy --checksum "$i" 360:datascibr-360/360
#done

#Google Cloud Configuration
#rclone sync pub instagram:power-bi-static-assets-mec-dsbr/instagram

