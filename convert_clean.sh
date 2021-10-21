#!/bin/bash

cat pub/*media_data.csv | sed '/;[0-9]\+$/!d' | sed 's/.\+;\([0-9]\+\)$/\1/' > ids.csv
cat pub/*_user_data.csv | awk -F ";" '{print $5}' | sed '/^[[:space:]]*$/d' | sed '/^id$/d' >> ids.csv

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

