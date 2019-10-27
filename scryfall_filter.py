import json
import sys

exluded_ids = open("exluded-ids.txt").read().splitlines()

cards = json.load(sys.stdin)
for card in cards:
	if card["full_art"]:
		continue
	if card["oversized"]:
		continue
	if card["promo"]:
		continue
	if card["layout"] == "split":
		continue
	if card["textless"]:
		continue
	if card["legalities"]["commander"] != "legal":
		continue
	if int(card["released_at"][:4]) < 2012:
		continue
	if not card["highres_image"]:
		continue
	if card["id"] in exluded_ids:
		continue
	if card.get("promo_types") is not None:
		if "datestamped" in card["promo_types"]:
			continue
	print(json.dumps(card))
