
import cv2
import numpy as np
import argparse
from os import listdir
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--glob",help="")
parser.add_argument("--best",help="amount of best images",type=int,default=100)
parser.add_argument("--ord",help="norm L1|L2",type=int,default=1)
group = parser.add_mutually_exclusive_group()
group.add_argument("--grid",help="size,step")
group.add_argument("--rois",nargs="+",help="(x0,y0,x1,y1)")

args = parser.parse_args()

files   = glob.glob(args.glob)
best    = args.best
rois    = args.rois
normord = args.ord

l_rois = [[int(ff) for ff in f.split(',')] for f in rois]

def Contrast(image):
	img = cv2.imread(image,cv2.CV_LOAD_IMAGE_GRAYSCALE)
	c = 0
	for r in l_rois:
		crop = img[r[1]:r[3], r[0]:r[2]]
		dst = cv2.Laplacian(crop,cv2.CV_64F)
		n = dst.reshape(dst.size)
		c = c + np.linalg.norm(n,ord=normord)
	return c

	

cont = [(Contrast(f),f) for f in files]
cont.sort(key=lambda t:-t[0])
for f in cont[0:best]:
	print f[1]


