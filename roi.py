
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--origine",help="image origine",required=True)
parser.add_argument("--new",help="new image",required=True)
parser.add_argument("--roi",help="x0,y0,x1,y1",required=True)
parser.add_argument("--excursion",help="amplitude de recherche",type=int,default=100)
args=parser.parse_args()

origine = args.origine
newimage = args.new
excursion = args.excursion
roi = args.roi
[x0,y0,x1,y1]= [int(f) for f in roi.split(",")]

print "origine   = " + origine
print "new image = " + newimage
print "excursion = " + str(excursion)
print "roi       = " + roi
print "x0        = " + str(x0)
print "y0        = " + str(y0)
print "x1        = " + str(x1)
print "y1        = " + str(y1)

I_origine=cv2.imread(origine,cv2.CV_LOAD_IMAGE_GRAYSCALE)
I_dest   =cv2.imread(newimage,cv2.CV_LOAD_IMAGE_GRAYSCALE)

excursion = 100
min_delta = 10000000
candidat = (0,0)
crop_ref = I_origine[y0:y1,x0:x1]

w,h = I_origine.shape[:2]
print w,h
w,h = I_dest.shape[:2]
print w,h

for i in range(-excursion,excursion):
	for j in range(-excursion,excursion):
		if (y0+i)<0 or (y1+i>w) or (x0+j)<0 or (x1+j)>h:
			continue
		crop_img=I_dest[(y0+i):(y1+i), (x0+j):(x1+j)]
		d = cv2.norm(crop_ref,crop_img,cv2.NORM_L1)
		if (d < min_delta):
			candidat=(i,j)
			min_delta=d
DY=candidat[0]
DX=candidat[1]

I_origine=cv2.cvtColor(I_origine,cv2.COLOR_GRAY2BGR)
cv2.rectangle(I_origine,(x0,y0),(x1,y1),(0,255,0),1)
cv2.imwrite("orig.bmp",I_origine)
I_show = cv2.cvtColor(I_dest,cv2.COLOR_GRAY2BGR)
cv2.rectangle(I_show,(x0+DX,y0+DY),(x1+DX,y1+DY),(0,0,255),1)
cv2.imwrite("show.bmp",I_show)
print candidat
print min_delta
