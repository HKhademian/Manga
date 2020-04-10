from manga_download import *

src = input('Please enter src: (TOONILY/webtoon) ')
src = WEBTOON if(src == 'webtoon') else TOONILY

title = ''
while (len(title)<=0):
	title = input('Please enter title: ').strip()

startPage = int(input('Please enter start page number: '))
lastPage = startPage-1
while(lastPage<startPage):
	lastPage = int(input('Please enter last page number: '))

overridePages = True if('y' == input('Do you want to override existing pages: (y/N) ')) else False

downloadImages = False if('n' == input('Do you want to access image localy: (Y/n) ')) else True

overrideImages = False
if(downloadImages):
	overrideImages = True if('y' == input('Do you want to override extisting images: (y/N) ')) else False

download(src, title, (startPage, lastPage), overridePages, downloadImages, overrideImages)
print('Have fun ;)')
