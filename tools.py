import os
import shutil
from natsort import natsorted
import glob

def destroyFiles(path):
	path_to_dir  = path  # path to directory you wish to remove
	files_in_dir = os.listdir(path_to_dir) 
	for file in files_in_dir:
		os.remove(f'{path_to_dir}/{file}')

def copyToOriginal(fromdir , todir):
	src = fromdir
	trg = todir
	files=os.listdir(src)
	for fname in files:
		shutil.copy2(os.path.join(src,fname), trg)

def remover(path):
	if os.path.isfile(path) or os.path.islink(path):
		os.remove(path)
	elif os.path.isdir(path):
		shutil.rmtree(path)
	else:
		pass

def resetNames(directoryNames,ty):
	y = 1000000000
	for filename in natsorted(glob.glob("./upload/"+directoryNames+"/"+ty+"/*.png")):
		x = os.path.join("./upload/"+directoryNames+"/"+ty+"/",filename[39:len(filename):1])
		os.rename(x,"./upload/"+directoryNames+"/"+ty+"/"+f"{y}.png")
		y += 1
	p = 1
	for filename in natsorted(glob.glob("./upload/"+directoryNames+"/original/*.png")):
		z = os.path.join("./upload/"+directoryNames+"/"+ty+"/",filename[39:len(filename):1])
		os.rename(z,"./upload/"+directoryNames+"/"+ty+"/"+f"{p}.png")
		p += 1