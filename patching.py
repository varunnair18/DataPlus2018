'''
patching.py

Script that splits all images from folder into patches of variable size
Also outputs csv with vectorized encoding of classes present in each patch as 'output.csv'
Example command: python patching.py test_image/ test_mask/ test_output/ 250

Author: Xiaolan You & Artem Streltsov
Group: Duke Data+ and Energy Initiative
Date: July 28, 2018
'''
import numpy as np 
import sys
import os
import pickle
import pandas as pd
from PIL import Image
from scipy.misc import imsave
from sklearn.preprocessing import MultiLabelBinarizer

labelencoder = {
    'DT':1,
    'DL':2,
    'TT':3,
    'TL':4,
    'OT':5,
    'OL':6,
    'SS':7
}

def iterateFiles(imagePath, maskPath, outputPath, patchSize):
    for f in [x for x in os.listdir(imagePath) if x.endswith('.tif')]:
        img = np.array(Image.open(imagePath+f)).astype(np.uint8)
        filename=f.split('.tif')[0]
        mask = np.array(Image.open(maskPath+filename+maskSuffix+'.tif')).astype(np.uint8)
        patchSize=int(patchSize)
        iteratePatch(img, mask, outputPath, patchSize, filename)
    return
        
def iteratePatch(image, mask, outputPath, patchSize, filename):
    xcoord=[x for x in range(image.shape[0]) if x%patchSize==0][:-1]
    ycoord=[y for y in range(image.shape[1]) if y%patchSize==0][:-1]
    count=0
    for x in xcoord:
        for y in ycoord:
            patch(image, mask, x, y, patchSize, filename, count)
            count+=1
    return

def patch(image, mask, x, y, patchSize, filename, count):
    patchImg=image[x:x+patchSize,y:y+patchSize,:image.shape[2]]
    patchMask=mask[x:x+patchSize,y:y+patchSize]
    unique=np.unique(patchMask)
    imageName=filename+'_'+str(count)+'_image.tif'
    fullName=outputPath+imageName
    maskName=outputPath+filename+'_'+str(count)+'_mask.tif'
    encoded_all, encoded_binary = encode(unique)
    data.append([imageName, encoded_all, encoded_binary])
    imsave(fullName, patchImg)
    imsave(maskName, patchMask)
    return
        
def encode(unique):
    unique=unique.reshape(len(unique), 1)
    mlb_encoder=MultiLabelBinarizer()
    classes=[0]
    classes=np.append(classes, np.array(list(labelencoder.values())))    
    classes=classes.reshape(1, len(classes))
    mlb_encoder.fit(classes)
    mlb_encoded=mlb_encoder.transform(unique)
    mlb_encoded=mlb_encoded.any(axis=0).astype(int)
    mlb_encoded_binary=mlb_encoded[1:].any().astype(int)

    return mlb_encoded[1:], mlb_encoded_binary

imagePath=sys.argv[1]
maskPath=sys.argv[2]
outputPath=sys.argv[3]
patchSize=sys.argv[4]
maskSuffix='_multiclass'

data=[]
iterateFiles(imagePath, maskPath, outputPath, patchSize)

columns=['imagename', 'label_all', 'label_binary']
df=pd.DataFrame(data, columns=columns)
df.to_csv(outputPath+'output.csv', index=False)


