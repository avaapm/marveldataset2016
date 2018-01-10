 Author: Erhan Gundogdu
 Last Update: 09/28/2016

 CITATION:
 If you use MARVEL in your research, please cite:
	@PROCEEDINGS {MARVEL,
    author       = "Gundogdu E., Solmaz B, Yucesoy V., Koc A.",
    title        = "Marvel: A Large-Scale Image Dataset for Maritime Vessels",
    year         = "2016",
    organization = "Asian Conference on Computer Vision (ACCV)"
	}
 
 This document is to explain the use of MARVEL and its metadata and to download it from the web.
 
 (0) Downloading MARVEL dataset:
	In order to download the MARVEL dataset, 'MARVEL_Download.py' Python script must be run with the appropriate
	.dat file, i.e. Uncomment the related dat file: 'VesselClassificationUpdated.dat' for Vessel Classification,
	'IMOTrainAndTest.dat' for Vessel Verification/Retrieval/Recognition tasks.	
	Default values and explanation of the download parameters inside MARVEL_Download.py are:
		NUMBER_OF_WORKERS = 10 ## Number of threads that will be working in parallel
		MAX_NUM_OF_FILES_IN_FOLDER = 5000 ## Maximum number of files in a folder
		IMAGE_HEIGHT = 256 ## image height unless ORIGINAL_SIZE = 1
		IMAGE_WIDTH = 256 ## image width unless ORIGINAL_SIZE = 1
		ORIGINAL_SIZE = 0 # 1 for yes, 0 for no
		JUST_IMAGE = 1 # 1 for yes, 0 for no
	
	The images are downloaded to the location of MARVEL_Download.py with a meta folder structure.
	Once the download is finished, the vessel images are distributed in a meta folder structure.
	The output filename is FINAL.dat, which has the same structure as the input XXX.dat file except for appended path names
	as the last column of each line.
	
	e.g. one line from input IMOTrainAndTest.dat file: '993293,1,1,Container Ship'
	and one line from output FINAL.dat file: '993293,1,1,Container Ship,path\to\your\folder\W1_1\993293.jpg'
	
	
 (1) Vessel Classification:
	VesselClassificationUpdated.dat is the corresponding file for vessel classification.
	
	Each line carries the information related to the training and the test images in the following structure:
		vessel ID, set index, class label, class label name
	vessel ID: is the ID consistent with the url name in the corresponding website and helps us to download the image.
	set index: 1 or 2 (1 for training and 2 for test)
	class label: vessel type label enumeration (from 1 to 26)
	class label name: the name of the class label given in our paper
	
	
 (2) IMO Training and Test Sets:
	IMOTrainAndTest.dat is the corresponding file containing information of IMO train and test sets defined in the paper.
	
	Each line carries the information related to the IMO train and the test images in the following structure:
			vessel ID, set index, class label, class label name, IMO Number
		vessel ID: is the ID consistent with the url name in the corresponding website and helps us to download the image.
		set index: 1 or 2 (1 for training and 2 for test)
		class label: vessel type label enumeration (from 1 to 26)
		class label name: the name of the class label given in our paper
		IMO number: is International Maritime Organization number of the corresponding vessel taken from the website
	Note: The IMO Train and test sets contain 400K images in total and Vessel Verification/Retrieval/Recognition set indices
	are based on the ordering of these 400K image list.
		
 (3) Vessel Verification:
	VesselVerificationTest.dat and VesselVerificationTrain.dat are the vessel verification task related .dat files.
	In each file, every line corresponds to the indices of the pairs of images for positive and negative examples.
	As stated in the paper, a positive example is a pair of images belonging to the same vessel
	and a negative example is a pair of images belonging to different vessels. These pairs are randomly sampled from
	the IMO train and test sets.
	
	Each line has the following structure:
			vessel index 1, vessel index 2, set index
		vessel index 1/2: the index of the vessels within a pos/neg example with respect to the IMO train/test set.
		set index: 0 or 1 (0 for negative examples, 1 for positive examples)
	
	Note: In order to use the VesselVerificationTest.dat and VesselVerificationTrain.dat files, IMOTrainAndTest.dat 
	is required, since the indices of this task are given with respect to the 400K IMO training and test sets.
 (4) Vessel Retrieval
	ChiTest.dat, ChiTrain.dat, EucTest.dat, EucTrain.dat are the corresponding meta files for vessel retrieval tasks for
	the chi square and euclidean distances.
	In each file, every line corresponds to training and test examples.
	
	Each line has the following structure:
			vessel index, class label, class name
		vessel index: the index of the corresponding example with respect to the IMO train/test set.
		class label: class label of the example out of 109 different vessels (as stated in the paper.)
		class name: name of the vessel type (as stated in the paper)
	Note: In order to use the VesselVerificationTest.dat and VesselVerificationTrain.dat files, IMOTrainAndTest.dat 
	is required, since the indices of this task are given with respect to the 400K IMO training and test sets.

 (5) Vessel Recognition
	The folder with the name Recognition (please first extract Recognition.zip) contains 29 classes for the purpose of recognizing individual vessel within their
	corresponding vessel types. This folder contains seperate foldera for different 29 vessel types.
	Each vessel type folder, e.g. Bulk Carrier, contain five different folds for training and testing. Each .dat file, i.e.
	trainSplit_X, has the following structure:
			vesselindex, IMO number
		vessel index: the index of the corresponding example with respect to the IMO train/test set.
		IMO number: IMO number for the example vessel image (This label is required for training a classifier and can also 
		be obtained from the first column of IMOTrainAndTest.dat file with the help of the vessel index.)
	Note: In order to use the VesselVerificationTest.dat and VesselVerificationTrain.dat files, IMOTrainAndTest.dat 
	is required, since the indices of this task are given with respect to the 400K IMO training and test sets.
