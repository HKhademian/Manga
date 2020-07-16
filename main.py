#!/usr/bin/python
import sys
from manga_download import *

src, title, startPage, lastPage, overridePages, downloadImages, overrideImages = '', '', 0, 0, False, True, False

args = sys.argv[1:]
if len(args):
	src = args.pop(0).strip()
	title = args.pop(0).strip()
	startPage = int(args.pop(0))
	lastPage = int(args.pop(0))
	overridePages = 'overridePages' in args
	overrideImages = 'overrideImages' in args
	downloadImages = overrideImages or 'downloadImages' in args
else:
	src = input('Please enter src: (TOONILY/webtoon) ').strip()

	while not len(title):
		title = input('Please enter title: ').strip()

	startPage = int(input('Please enter start page number: '))
	lastPage = startPage-1
	while lastPage<startPage:
		lastPage = int(input('Please enter last page number: '))

	overridePages = True if('y' == input('Do you want to override existing pages: (y/N) ')) else False

	downloadImages = False if('n' == input('Do you want to access image localy: (Y/n) ')) else True

	overrideImages = False
	if downloadImages:
		overrideImages = True if('y' == input('Do you want to override extisting images: (y/N) ')) else False

src = WEBTOON if src == 'webtoon' else TOONILY

# print ((src, title, startPage, lastPage, overridePages, downloadImages, overrideImages))
# exit()

download(src, title, (startPage, lastPage), overridePages, downloadImages, overrideImages)
print('Have fun ;)')
