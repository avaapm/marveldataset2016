import os
import random

# returns the number of images in each classname folder and deletes any above the maximum
delete_over_max=False
max_per_class = 12000

data_path = '/home/davisac1/marvel_ds'

for classname in os.listdir(data_path):
    class_path = os.path.join(data_path, classname)
    count = 0
    for name in os.listdir(class_path):
        name_path = os.path.join(class_path, name)
        for path in os.scandir(name_path):
            if path.is_file():
                count += 1
    if delete_over_max==True and count>max_per_class: # in case you downloaded too much data for a class
        # remove random names until count < 12000
        namelist = os.listdir(class_path)
        random.shuffle(namelist)
        for name in namelist:
            name_path = os.path.join(class_path, name)
            for path in os.scandir(name_path):
                if path.is_file():
                    os.remove(path.path)
                    count -= 1
                    if count < 12000:
                        break
            # if name_path is empty, delete the folder
            if len(os.listdir(name_path)) == 0:
                os.rmdir(name_path)
                print(f'{name_path} deleted')
            if count < 12000:
                break

    print(f'{classname}: {count}')
        
