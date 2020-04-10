import os
import re
from manga_download import *

src = TOONILY
title = 'perfect-roommates'
pageRange = (0,17)

CDIR = os.path.dirname(os.path.realpath(__file__)) # os.path.abspath(__file__)
indexPath = INDEX_ADDRESS_FORMAT.format(src[0], title)

with open(indexPath, 'r') as indexFile:
	index = json.load(indexFile)

for pageNum in index:
	pageNumber = int(pageNum)
	images = index[pageNum]
	createPage(src, title, pageRange, pageNumber, images)
