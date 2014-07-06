
import argparse
import glob
import cv2
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("--family",help="family image", required=True)
parser.add_argument("--output",help="output", required=True)

args=parser.parse_args()

family=args.family
output=args.output

print "family = "+family
files =  glob.glob(family+"_*.bmp")
I = np.zeros((480,640))
for f in files:
	img = cv2.imread(f, cv2.CV_LOAD_IMAGE_GRAYSCALE).astype(float)
	I = I + img

I = I / len(files)

cv2.imwrite(output,I)
