import os
import re
import json

CDIR = os.path.dirname(os.path.realpath(__file__)) # os.path.abspath(__file__)
indexPath = os.path.join(CDIR, './output/toonily/perfect-roommates/content/index.json')

with open(indexPath, 'r') as indexFile:
	index = json.load(indexFile)

newIndex = {}
for key in index:
	page = index[key]
	newPage = {}
	for img in page:
		image = re.search('image-(.*)', img, re.IGNORECASE).group(1).zfill(3)
		newPage[image] = page[img]
	newIndex[key.zfill(3)] = newPage

with open(indexPath, 'w') as indexFile:
	json.dump(newIndex, indexFile)

