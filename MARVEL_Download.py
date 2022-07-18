from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, build_opener, install_opener
from PIL import Image
import traceback
import threading
# import datetime
# import logging
import codecs
import math
import os
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
# import requests
import time
from tqdm import tqdm

##Uncomment the related dat file ('VesselClassification.dat' for Vessel Classification, 'IMOTrainAndTest.dat' for Vessel Verification/Retrieval/Recognition tasks.)
# FILE_TO_DOWNLOAD_FROM = "VesselClassification.dat"
# FILE_TO_DOWNLOAD_FROM = "accom_test2.csv"
##FILE_TO_DOWNLOAD_FROM = "IMOTrainAndTest.dat" 
crop = 20
NUMBER_OF_WORKERS = 10
# MAX_NUM_OF_FILES_IN_FOLDER = 5000
IMAGE_HEIGHT = 720
IMAGE_WIDTH = 1280
ORIGINAL_SIZE = 0 # 1 for yes, 0 for no
JUST_IMAGE = 1 # 1 for yes, 0 for no

# savedir = '/data1/marvel_ds'
savedir = '/home/davisac1/marvel_ds'
datadir = '/home/davisac1/marveldataset2016/category_data'
cats = [os.path.splitext(x)[0] for x in os.listdir(datadir)]

# sourceLink = "http://www.shipspotting.com/gallery/photo.php?lid="
sourceLink = "http://www.shipspotting.com/photos/"

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )
# logging.debug("Process started at " + str(datetime.datetime.now()))

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0",
# }

def save_image(ID,justImage,outFolder):
    url = sourceLink + ID
    opener = build_opener()
    # opener.addheaders = [('User-Agent', 'MyApp/1.0')]
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0')]
    install_opener(opener)
    req = Request(url)
    # html = requests.get(url, headers=headers).text
    works = False
    while not works:
        wait = 1
        try:
            html = urlopen(req, timeout=300).read()
            works = True
        except:
            traceback.print_exc()
            print(f'Trying again after {wait} seconds')
            time.sleep(wait)
            wait = wait + 1
    soup = BeautifulSoup(html,"lxml")
    # soup = BeautifulSoup(html,"html.parser")


    images = [img for img in soup.find_all('img')]
    image_links = [each.get('src') for each in images]

    label = {}

    filename = " "
    for each in image_links:
        if "http" in each and "jpg" in each and "photos/big" in each:
            filename=each.split('/')[-1]
            works = False
            wait = 1
            while not works:
                try:
                    f = urlopen(each)
                    works = True
                except:
                    wait = wait + 1
                    traceback.print_exc()
                    print(f'Trying again after {wait} seconds')
                    time.sleep(1)
            with open(os.path.join(outFolder,filename), "wb") as local_file:
                local_file.write(f.read())
            if ORIGINAL_SIZE == 0:
                img = Image.open(os.path.join(outFolder,filename)).resize((IMAGE_WIDTH,IMAGE_HEIGHT), Image.ANTIALIAS)
                os.remove(os.path.join(outFolder,filename))
                img = img.crop((0,0,IMAGE_WIDTH,IMAGE_HEIGHT-crop))
                img.save(os.path.join(outFolder,filename))
            break

    label['filename'] = filename
    if not justImage:
        photo_label = [ele.text for ele in soup.find_all('div', {'class': 'summary-photo__card-general__label'})]     
        for pt in photo_label:
            key, value = pt.split(': ')
            label[key] = value
  
    if filename != " " and not justImage:
        with open(os.path.join(outFolder,filename)+'.txt','w') as tFile:   
            for k,v in label.items():
                tFile.write(k+':'+v+'\n')

    if filename == " ":
        return 0
    else:
        return 1


def worker(content,cat):
    workerIndex = 0
    folderIndex = 0
    # folderNo = 1

    # currFolder = os.path.join(os.getcwd(),'W'+str(workerNo)+'_'+str(folderNo))
    saveFolder = os.path.join(savedir, cat)
    if not os.path.exists(saveFolder):
        os.mkdir(saveFolder)
    for boat in content:
        title = boat[1]
        ID = boat[0]
        boatFolder = os.path.join(saveFolder, title)
        if not os.path.exists(boatFolder):
            os.mkdir(boatFolder)
        # if folderIndex == MAX_NUM_OF_FILES_IN_FOLDER:
        #     folderIndex = 0
        #     folderNo = folderNo + 1
        #     # currFolder = os.path.join(os.getcwd(),'W'+str(workerNo)+'_'+str(folderNo))
        #     saveFolder = os.path.join(savedir, cat)
        #     if not os.path.exists(saveFolder):
        #         os.mkdir(saveFolder)
        try:

            status = save_image(ID,JUST_IMAGE,boatFolder)
            workerIndex = workerIndex + 1
            if status == 1:
                folderIndex = folderIndex + 1
                # logging.debug(str(ID) + "\t - Downloaded... - " + str(workerIndex) + "\t/" + str(len(content)))
            # else:
                # logging.debug(str(ID) + "\t - NO SUCH FILE  - " + str(workerIndex) + "\t/" + str(len(content)))
        except:
            traceback.print_exc()
    # logging.debug(str(datetime.datetime.now()) + "-------------- DONE ")
    return

def main(cat):
    
    priorFiles = []
    dirs = os.listdir(os.getcwd())
    for eachDir in dirs:
        if 'W' in eachDir:
            oldFiles = os.listdir(os.path.join(os.getcwd(),eachDir))
            for eachFile in oldFiles:
                if ".jpg" in eachFile:
                    oldID = eachFile.split(".")[0]
                    priorFiles.append(oldID)

    downloadsource = os.path.join(datadir,cat) + '.csv'
    downloadFile = codecs.open(downloadsource,"r","utf-8")
    downloadContent = downloadFile.readlines()
    downloadFile.close()
    finalContent = []
    for eachLine in downloadContent:
        temp = (eachLine.split(',')[0],eachLine.split(',')[2])
        if temp not in priorFiles:
            finalContent.append(temp)

    numOfFiles = len(finalContent) 

    numOfFilesPerEachWorker = [int(math.floor(float(numOfFiles)/NUMBER_OF_WORKERS)) for x in range(0,NUMBER_OF_WORKERS-1)]
    numOfFilesPerEachWorker.append(numOfFiles - (NUMBER_OF_WORKERS-1)*int(round(numOfFiles/NUMBER_OF_WORKERS,0)))

    # logging.debug("There will be %s workers in this download process" % NUMBER_OF_WORKERS)
    print(f'There will be {NUMBER_OF_WORKERS} workers in this download process')
    # logging.debug("%s files will be downloaded" % numOfFiles)
    print(f'{numOfFiles} files will be downloaded')

    threads = []
    imageCount = 0
    for i in range(0,NUMBER_OF_WORKERS):
        t = threading.Thread(name='Worker'+str(i), target=worker, args=(finalContent[imageCount:imageCount + numOfFilesPerEachWorker[i]],cat))
        imageCount = imageCount + numOfFilesPerEachWorker[i]
        threads.append(t)
        t.start()

    # flag = True
    # while flag:
    #     counter = 0
    #     for eachT in threads:
    #         if eachT.is_alive() == False:
    #             counter = counter + 1
    #     if counter == NUMBER_OF_WORKERS:
    #         flag = False

    # logging.debug(str(datetime.datetime.now()) + " - list all files startes ")

    # allPaths = []
    # allIDs = []
    # dirs = os.listdir(os.getcwd())
    # for eachDir in dirs:
    #     if 'W' in eachDir:
    #         FinalList = os.listdir(os.path.join(os.getcwd(),eachDir))
    #         for eachFile in FinalList:
    #             if ".jpg" in eachFile:
    #                 fPath = os.path.join(os.getcwd(),eachDir,eachFile)
    #                 fID = eachFile.split(".")[0]
    #                 allPaths.append(fPath)
    #                 allIDs.append(fID)
    # logging.debug(str(datetime.datetime.now()) + " - write to disc ")

    # FINAL = codecs.open("FINAL.dat","w","utf-8")
    # for eachLine in downloadContent:
    #     tempID = eachLine.split(",")[0]
    #     try:
    #         tempIndex = allIDs.index(tempID)
    #         FINAL.write(eachLine[:-1]+","+str(allPaths[tempIndex])+"\n")
    #     except:
    #         FINAL.write(eachLine[:-1]+","+"-\n")
    # FINAL.close()

if __name__ == '__main__':
    for cat in tqdm(cats):
        if cat in os.listdir(savedir):
            print(f'{cat} already downloaded')
            continue
        print('Begin downloading ' + cat)
        main(cat)













                                                                  





