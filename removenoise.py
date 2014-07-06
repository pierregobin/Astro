
import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--image",help="image with noise",required=True)
parser.add_argument("--black", help="black image",required=True)
parser.add_argument("--output",help="output",required=True)
args=parser.parse_args()

image=args.image
black=args.black
output=args.output

I = cv2.imread(image,cv2.CV_LOAD_IMAGE_GRAYSCALE)
N = cv2.imread(black,cv2.CV_LOAD_IMAGE_GRAYSCALE)
O = I-N
cv2.imwrite(output,O)
