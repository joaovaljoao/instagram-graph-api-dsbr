#!/bin/bash

sed '/;[0-9]\+$/!d' pub/instagram_media_data.csv | sed 's/.\+;\([0-9]\+\)$/\1/' > ids.csv
awk -F ";" '{print $5}' pub/instagram_user_data.csv | sed '/^[[:space:]]*$/d' | tail -n +2 >> ids.csv

for i in images/*.jpg
do
	FILE=${i#images/}
	ID=${FILE%.jpg}
	EXIST=`cat ids.csv | sed "/^$ID/!d"`
	if [ -z "$EXIST" ]
	then
		echo "Removendo arquivo $i"
		rm -f "$i"
		rm -rf "pub/images/$i"
	else
		if [ ! -f "pub/images/$FILE" ]
		then
			echo "Convertendo arquivo de id: $ID"
			convert "$i" -resize "30%" "pub/images/$FILE"
		fi
	fi
done

