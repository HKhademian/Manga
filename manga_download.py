import requests
from bs4 import BeautifulSoup
import json
# from urllib.request import urlretrieve
import shutil
import re
import os.path
from pathlib import Path

TOONILY = ('toonily', 'https://toonily.com/webtoon/{0}/chapter-{1}/')
WEBTOON = ('webtoon', 'https://www.webtoon.xyz/read/{0}/chapter-{1}/')

TEMP_PAGES_HTML = './template/pages.html'
TEMP_PAGES_CSS = './template/pages.css'
TEMP_IMAGES_HTML = './template/images.html'

BASE_DIR_ADDRESS_FORMAT = './output/{0}/{1}'
CONTENT_DIR_ADDRESS_FORMAT = BASE_DIR_ADDRESS_FORMAT + '/content'
IMAGES_DIR_ADDRESS_FORMAT = CONTENT_DIR_ADDRESS_FORMAT + '/images'

INDEX_ADDRESS_FORMAT = CONTENT_DIR_ADDRESS_FORMAT + '/index.json'
CSS_ADDRESS_FORMAT = CONTENT_DIR_ADDRESS_FORMAT + '/pages.css'
HTML_ADDRESS_FORMAT = BASE_DIR_ADDRESS_FORMAT + '/page-{2}.html'
IMAGE_ADDRESS_FORMAT = IMAGES_DIR_ADDRESS_FORMAT+ '/page-{2}-image-{3}.jpg'

PAGE_HOME_ADDRESS_FORMAT = './index.html'
PAGE_HTML_ADDRESS_FORMAT = './page-{0}.html'
IMAGE_HTML_ADDRESS_FORMAT = './content/images/page-{2}-image-{3}.jpg'

def saveImage(url, dest, overrideImages = False):
	if(os.path.isfile(dest) and not overrideImages):
		return 0

	try:
		response = requests.get(url, stream=True)
		response.raise_for_status()
	except:
		return -1

	with open(dest, 'wb') as output:
		shutil.copyfileobj(response.raw, output)
	del response
	return 1


def createPage(src, title, pageRange, pageNumber, images):
	srcSite = src[0]
	fromPage = pageRange[0]
	toPage = pageRange[1]
	pageNum = str(pageNumber).zfill(3)
	pageFileAddress = HTML_ADDRESS_FORMAT.format(srcSite, title, pageNum)

	print('- Writing in file ...')

	with open(TEMP_PAGES_HTML, 'r') as pagesTempFile:
		pagesTemp = pagesTempFile.read()

	with open(TEMP_IMAGES_HTML, 'r') as imagesTempFile:
		imagesTemp = imagesTempFile.read()

	pageCount = toPage - fromPage + 1
	homePageLink = PAGE_HOME_ADDRESS_FORMAT
	firstPageLink = PAGE_HTML_ADDRESS_FORMAT.format(str(fromPage).zfill(3))
	lastPageLink = PAGE_HTML_ADDRESS_FORMAT.format(str(toPage).zfill(3))
	with open(pageFileAddress, 'w') as pageFile:
		contentStr = ''
		for (imageId, imageAddress) in images.items():
			localSrc = IMAGE_HTML_ADDRESS_FORMAT.format(srcSite, title, pageNum, imageId)
			contentStr += imagesTemp \
				.replace('{{id}}', imageId) \
				.replace('{{localSrc}}', localSrc) \
				.replace('{{externalSrc}}', imageAddress)

		backPageNumber = pageNumber-1 if pageNumber>fromPage else pageNumber
		nextPageNumber = pageNumber+1 if pageNumber<toPage else pageNumber
		backPageLink = PAGE_HTML_ADDRESS_FORMAT.format(str(backPageNumber).zfill(3))
		nextPageLink = PAGE_HTML_ADDRESS_FORMAT.format(str(nextPageNumber).zfill(3))

		pageStr = pagesTemp \
				.replace('{{title}}', title) \
				.replace('{{pageNumber}}', pageNum) \
				.replace('{{pageCount}}', pageCount) \
				.replace('{{fromPage}}', str(fromPage)) \
				.replace('{{toPage}}', str(toPage)) \
				.replace('{{stories}}', contentStr) \
				.replace('{{firstPageLink}}', firstPageLink) \
				.replace('{{backPageLink}}', backPageLink) \
				.replace('{{nextPageLink}}', nextPageLink) \
				.replace('{{lastPageLink}}', lastPageLink) \
				.replace('{{homePageLink}}', homePageLink)
		pageFile.write(pageStr)


def downloadPage(src, title, pageRange, pageNumber, overridePage = False, downloadImages = False, overrideImages = False):
	fromPage = pageRange[0]
	toPage = pageRange[1]
	pageNum = str(pageNumber).zfill(3)

	pageFileAddress = HTML_ADDRESS_FORMAT.format(src[0], title, pageNum)
	if(not overridePage and os.path.isfile(pageFileAddress)):
		return 0

	url = src[1].format(title, pageNumber)
	try:
		response = requests.get(url)
		response.raise_for_status()
	except:
		return -1
	print('- Get Page completed!')

	soup = BeautifulSoup(response.content, 'html.parser')	# resp.text
	print('- Page Loaded.')

	if src == TOONILY or src == WEBTOON:
		content = soup.find(class_='reading-content')
		for image in content.findAll('img'):
			imageId = img['id'].strip()
			imageSrc = img['data-src'].strip()
			imageId = re.search('image-(.*)', imageId, re.IGNORECASE).group(1).zfill(3)
			images[imageId] = imageSrc
	else:
		images = {}

	createPage(src, title, pageRange, pageNumber, images)
	return images


def download(src, title, pageRange, overridePages = False, downloadImages = False, overrideImages = False):
	srcSite = src[0]
	Path(IMAGES_DIR_ADDRESS_FORMAT.format(srcSite, title)).mkdir(parents=True, exist_ok=True)

	fromPage = pageRange[0]
	toPage = pageRange[1]
	index = {}

	indexFileAddress = INDEX_ADDRESS_FORMAT.format(srcSite, title)
	if(os.path.isfile(indexFileAddress)):
		try:
			with open(indexFileAddress) as json_file:
				index = json.load(json_file)
		except:
			index = {}

	for pageNumber in range(fromPage, toPage+1):
		pageNum = str(pageNumber).zfill(3)
		print('\nStart getting page #{0}/{1}'.format(pageNum, toPage))

		res = downloadPage(src, title, pageRange, pageNumber, overridePages, downloadImages, overrideImages)

		if(res == 0):
			print('- Page {0} is already exists'.format(pageNum))
		elif(res == -1):
			print('- Error in downloading page {0}'.format(pageNum))
		else:
			index[pageNum] = res
			print('- Page {0} Downloaded!'.format(pageNum))

	with open(indexFileAddress, 'w') as indexFile:
		json.dump(index, indexFile)

	cssFileAddress = CSS_ADDRESS_FORMAT.format(srcSite, title)
	if not os.path.isfile(cssFileAddress):
		try:
			with open(TEMP_PAGES_CSS, 'r') as cssTempFile:
				with open(cssFileAddress, 'w') as cssFile:
					cssFile.write(cssTempFile.read())
		except:
			print('- Cannot create style file.')

	if downloadImages:
		print('\nStart downloading images ...')
		for pageNumber in range(fromPage, toPage+1):
			pageNum = str(pageNumber).zfill(3)
			if not pageNum in index: continue
			images = index[pageNum]
			i = 0
			I = len(images)
			for imageId, imageAddress in images.items():
				i += 1
				imageFile = IMAGE_ADDRESS_FORMAT.format(srcSite, title, pageNum, imageId)
				# print('-\t Downloading {0} from {1} to {2}'.format(imageId, imageAddress, imageFile))
				res = saveImage(imageAddress, imageFile)
				iI = str(i).zfill(3)
				if res == 0:
					print('- Page #{0}/{1} - Image #{2}/{3} exists.'.format(pageNum, toPage, iI, I))
				elif res == 1:
					print('- Page #{0}/{1} - Image #{2}/{3} downloaded.'.format(pageNum, toPage, iI, I))
				else:
					print('- Page #{0}/{1} - Image #{2}/{3} error to download.'.format(pageNum, toPage, iI, I))

	print('\nAll pages Download completed!')

