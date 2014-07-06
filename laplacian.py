import cv2
import numpy as np
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--glob",help="glob file")
args = parser.parse_args()

files = glob.glob(args.glob)

def Laplace(image):
	img = cv2.imread(image,cv2.CV_LOAD_IMAGE_GRAYSCALE)
	l = np.abs(cv2.Laplacian(img, cv2.CV_64F))
	return l.max()

L = [(Laplace(f),f) for f in files]
L.sort(key=lambda t:-t[0])
for f in L:
	print f[1] + " " + str(f[0])

