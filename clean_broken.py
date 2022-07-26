# script to delete corrupt files in the dataset
import os
from PIL import Image

path = '/home/davisac1/marvel_ds'
cnt = 0
for classname in os.listdir(path):
    classpath = os.path.join(path,classname)
    for name in os.listdir(classpath):
        namepath = os.path.join(classpath,name)
        for file in os.listdir(namepath):
            try:
                img = Image.open(os.path.join(namepath,file))
                assert img.size == (1280,720) 
            except:
                os.remove(os.path.join(namepath,file))
                print(f'{os.path.join(namepath,file)} deleted')
            cnt += 1
            if cnt % 1000 == 0:
                print(f'{cnt} files checked')