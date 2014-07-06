
import cv2
import numpy as np
import argparse
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--origine",help="image origine",required=True)
parser.add_argument("--only",help="only a few image",type=int,default=0)
group_files=parser.add_mutually_exclusive_group()
group_files.add_argument("--glob",help="regexp for file")
group_files.add_argument("--filelist",help="file contains the name of all files to be processed")

group = parser.add_mutually_exclusive_group()
group.add_argument("--grid",help="size,step")
group.add_argument("--rois",nargs="+",help="(x0,y0,x1,y1)")
parser.add_argument("--dirdest",help="directory des roi",required=True)
parser.add_argument("--excursion",help="amplitude de recherche",type=int,default=100)
parser.add_argument("--annote",help="annotation",choices=['rectangle','vector'],default='vector')
parser.add_argument("--zoom", help="zoom",type=int,default=1)
parser.add_argument("--threshold", help="threshold",type=int,default=100)
parser.add_argument("--output", help="output file")
args=parser.parse_args()

origine   = args.origine
excursion = args.excursion
rois       = args.rois
dirdest   = args.dirdest
annote    = args.annote
zoom      = args.zoom
threshold = args.threshold
glob_file = args.glob
filelist  = args.filelist
onlyfiles = args.only
outputfile = args.output
I_origine=cv2.imread(origine,cv2.CV_LOAD_IMAGE_GRAYSCALE)
I_improveImage = I_origine.astype(float)
Height,Width = I_origine.shape[:2]
I_norm = np.ones((Height,Width))

print Width,Height
try:
	l_rois= [[int(ff) for ff in f.split(',')] for f in rois]
	print l_rois
except :
	grid = args.grid
	roisize = int(grid.split(":")[0])
	step = int(grid.split(":")[1])
	print roisize,step
	l_rois = [(x,y,x+roisize,y+roisize) for x in xrange(roisize/2,Width-roisize,step) 
                   for y in xrange(roisize/2,Height-roisize,step)]
	print l_rois

try:
	print "Glob = " + glob_file
	files = glob.glob(glob_file)
	print files
except:
	try:
		f = open(filelist)
		files =[i.rstrip() for i in f.readlines()]
		f.close()
	except:
		print "Error : missing input files"
		exit(1)

print "origine   = " + origine
print "dir dest  = " + dirdest
print "excursion = " + str(excursion)
print "annote    = " + annote



def FindRoi(I_ImageRef,(xx0,yy0,xx1,yy1),excursion,I_ImageDest):
	min_delta = 10000000
	candidat=(0,0)
	crop_ref = I_ImageRef[yy0:yy1, xx0:xx1]
	global Height,Width
	for i in range(-excursion,excursion):
		for j in range(-excursion,excursion):
			if (yy0+i)<0 or (yy1+i>Height) or (xx0+j)<0 or (xx1+j)>Width:
				continue
			crop_img=I_ImageDest[(yy0+i):(yy1+i), (xx0+j):(xx1+j)]
			d = cv2.norm(crop_ref,crop_img,cv2.NORM_L1)
			if (d < min_delta):
				candidat=(i,j)
				min_delta=d
	return candidat,min_delta

def Annote(I_image,(x0,y0,x1,y1),(dx,dy),TypeAnnote):
	if TypeAnnote=="rectangle":
		cv2.rectangle(I_image,(x0+dx,y0+dy),(x1+dx,y1+dy),(0,0,255),1)
	elif TypeAnnote=="vector":
		X = (x0+x1)/2
		Y = (y0+y1)/2
		cv2.line(I_image,(X,Y), (X+dx*zoom,Y+dy*zoom),(0,0,255),1)
		cv2.circle(I_image,(X,Y),2,(0,255,0))


def Grillage(I_origine,I_dest,rois):
	l = []
	w,h=I_origine.shape[:2]
	for r in rois:
		(DY,DX),distance = FindRoi(I_origine,
                               (r[0],r[1],r[2],r[3]),excursion,I_dest)
		l.append((r[0],r[1],r[2],r[3],DX,DY,distance))
	return l

#I_origine=cv2.cvtColor(I_origine,cv2.COLOR_GRAY2BGR)
#cv2.rectangle(I_origine,(x0,y0),(x1,y1),(0,255,0),1)
#cv2.imwrite("orig.bmp",I_origine)

def AnalyzeImage(f_image):
	I_dest=cv2.imread(f_image,cv2.CV_LOAD_IMAGE_GRAYSCALE)
	I_show = cv2.cvtColor(I_dest,cv2.COLOR_GRAY2BGR)
	for (x0,y0,x1,y1,DX,DY,d) in Grillage(I_origine,I_dest,l_rois):
		if d<threshold :
			Annote(I_show,(x0,y0,x1,y1),(DX,DY),annote)
			I_improveImage[y0:y1, x0:x1] = I_improveImage[y0:y1, x0:x1] + I_dest[y0+DY:y1+DY, x0+DX:x1+DX]
			I_norm[y0:y1, x0:x1] = I_norm[y0:y1, x0:x1] + np.ones((y1-y0,x1-x0))
	cv2.imwrite(dirdest+"/"+os.path.splitext(os.path.basename(f_image))[0]+".jpg",I_show)




if onlyfiles == 0:
	maxcount=len(files)
else:
	maxcount=onlyfiles

for f in files:
	print f
	AnalyzeImage(f)
	maxcount = maxcount-1
	if maxcount==0:
		break
		

I_improveImage = I_improveImage / I_norm
cv2.imwrite(outputfile,I_improveImage)
