#!/bin/sh
cd /home/marcel/instagram-graph-api-dsbr/src
./main.py ifes.csv
./main.py abepro.csv
cd ..
#cp -f usuarios.csv pub
cp -f src/ifes.csv pub/usuarios.csv
cp -f pub/ifes_media_data.csv pub/instagram_media_data.csv
cp -f pub/ifes_user_data.csv pub/instagram_user_data.csv
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

