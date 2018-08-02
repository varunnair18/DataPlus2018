'''
cutTiff.py

Cuts input tif into specified patches of specific size using gdal_translate. 
Different from numpy approach in patching.py because this does not loop through values within the tif file. 
Example terminal command: python cutTiff.py Brazil_Rio_1.tif 5000
Adapted from: https://gis.stackexchange.com/questions/14712/splitting-raster-into-smaller-chunks-using-gdal

Author: Xiaolan You
Group: Duke Data+ and Energy Initiative
Date: June 20, 2018

'''

import os, sys
from osgeo import gdal

dset = gdal.Open(sys.argv[1])
width = dset.RasterXSize
height = dset.RasterYSize

print(width, 'x', height)

filename = sys.argv[1].split('.tif')[0]
tilesize = int(sys.argv[2])

for i in range(0, width, tilesize):
    for j in range(0, height, tilesize):
        w = min(i+tilesize, width) - i
        h = min(j+tilesize, height) - j
        gdaltranString = "gdal_translate -of GTIFF -srcwin "+str(i)+", "+str(j)+", "+str(w)+", " \
            +str(h)+" " + sys.argv[1] + " " + filename + "_"+str(i)+"_"+str(j)+".tif"
        os.system(gdaltranString)