import os
import re

CDIR = os.path.dirname(os.path.realpath(__file__)) # os.path.abspath(__file__)

files = os.listdir(CDIR)
for file in files:
	res = re.search('page-(.*)-image-(.*).jpg', file, re.IGNORECASE)
	if not res: continue
	page = res.group(1).zfill(3)
	image = res.group(2).zfill(3)
	newName = 'page-{0}-image-{1}.jpg'.format(page, image)
	srcFile = os.path.join(CDIR, file)
	targetFile = os.path.join(CDIR, newName)

	os.rename(srcFile, targetFile)
	#shutil.move(srcFile, targetFile)
	#os.replace(srcFile, targetFile)
