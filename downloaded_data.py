import os

# returns the number of images in each classname folder

data_path = '/home/davisac1/marvel_ds'

for classname in os.listdir(data_path):
    class_path = os.path.join(data_path, classname)
    count = 0
    for name in os.listdir(class_path):
        name_path = os.path.join(class_path, name)
        for path in os.scandir(name_path):
            if path.is_file():
                count += 1
    print(f'{classname}: {count}')
        
