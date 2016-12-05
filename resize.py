import os
from PIL import Image
def reSize():
	path = "./thumb"
	filelist = os.listdir(path)
	for files in filelist:
		filedir = os.path.join(path,files)
		if os.path.isdir(filedir):
			childlist = os.listdir(filedir)
			for image in childlist:
				imagedir = os.path.join(filedir,image)
				filetype = os.path.splitext(image)[1]
				if(filetype == '.png'):
					print imagedir
					filein = Image.open(imagedir)
					fileout = filein.resize((60,60),Image.ANTIALIAS)
					fileout.save(imagedir)
	
if (__name__ == '__main__'):
	reSize()
