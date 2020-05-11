#!/usr/bin/bash

mkdir tmp 2>/dev/null

curl -o "tmp/#1.json" 'https://api.scryfall.com/cards/search?q=type:planeswalker%20OR%20type:forest%20OR%20type:island%20OR%20type:mountain%20OR%20type:plains%20OR%20type:swamp%20OR%20is:masterpiece%20OR%20type:saga&page=[1-22]&unique=prints'
cat tmp/*.json | jq '.data[].id' | tr -d \" >| tmp/excluded_ids.txt

if [[ -z "$SCRYFALL_ARCHIVE" ]]; then
	echo 'SCRYFALL_ARCHIVE is not set'
	exit
fi

unzip -p "$SCRYFALL_ARCHIVE" | python3 scryfall_filter.py >| tmp/scryfall_stripped.txt
< tmp/scryfall_stripped.txt jq '.image_uris.art_crop' | grep -v null | cut -c 48-91 >| images.txt
rm -rf tmp