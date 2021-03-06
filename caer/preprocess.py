# Author: Jason Dsouza
# Github: http://www.github.com/jasmcaus

# Importing the necessary packages
import sys
sys.path.append('..')

import os
import time
import numpy as np
from .utils import readImg
from .utils import saveNumpy
from .utils import get_classes_from_dir
from .preprocessing import MeanProcess

def preprocess_from_dir(DIR, 
                        classes=None, 
                        channels=1, 
                        IMG_SIZE=224, 
                        train_size=None, 
                        normalize_train=False, 
                        mean_subtraction=None, 
                        isShuffle=True, 
                        save_train=False, 
                        destination_filename=None, 
                        display_count=True):
    """
    Reads Images in base directory DIR using 'classes' (computed from sub directories )
    :param DIR: Directory 
    :param classes: A list of folder names within 'DIR'
    :param channels: Number of channels each image will be processed to (default: 1)
    :param train_size: Size of the training set
    :param normalize_train: Whether to normalize each image to between [0,1]
    :param mean_subtraction: Whether mean subtraction should be applied (Tuple)
    :param isShuffle: Shuffle the training set
    :param save_train: If True, saves the training set as a .npy or .npz file based on destination_filename
    :param destination_filename: if save_train is True, the train set will be saved as the filename specified
    :param display_count: Displays the progress as preprocessing continues
    
    :return train: Image Pixel Values with corresponding labels (float32)
    Saves the above variables as .npy files if save_train = True
    """

    train = [] 
    if save_train:
        if destination_filename is None:
            raise TypeError('[ERROR] Specify a destination file name')

        elif not ('.npy' in destination_filename or '.npz' in destination_filename):
            raise ValueError('[ERROR] Specify the correct numpy destination file extension (.npy or .npz)', destination_filename)
    
        elif destination_filename is not None:
            destination_filename = None
    
    elif classes is not None:
        if type(classes) is not list:
            raise ValueError('[ERROR] "classes" must be a list')

    elif not os.path.exists(DIR):
        raise ValueError('[ERROR] The specified directory does not exist', DIR)

    elif IMG_SIZE is None:
        raise ValueError('[ERROR] IMG_SIZE must be specified')

    elif type(IMG_SIZE) is not int:
        raise ValueError('[ERROR] IMG_SIZE must be an integer')

    # Loading from Numpy Files
    elif destination_filename is not None and os.path.exists(destination_filename):
        since = time.time()
        print('[INFO] Loading from Numpy Files')
        train = np.load(destination_filename, allow_pickle=True)
        end = time.time()
        print('----------------------------------------------')
        print('[INFO] Loaded in {:.0f}s from Numpy Files'.format(end-since))

        return train

    # Extracting image data
    else:
        since_preprocess = time.time()
        if destination_filename is not None:
            print(f'[INFO] Could not find {destination_filename}. Generating the Image Files')
        else:
            print('[INFO] Could not find a file to load from. Generating Image Files')
        print('----------------------------------------------')

        if classes is None:
            classes = get_classes_from_dir(DIR)

        if train_size is None:
            train_size = len(os.listdir(os.path.join(DIR, classes[0])))

        # Checking if 'mean_subtraction' values are valid. Returns boolean value
        subtract_mean = check_mean_subtraction(mean_subtraction, channels)

        for item in classes:
            class_path = os.path.join(DIR, item)
            class_label = classes.index(item)
            count = 0 
            for image in os.listdir(class_path):
                if count != train_size:
                    image_path = os.path.join(class_path, image)

                    # Returns image RESIZED and img
                    img = readImg(image_path, resized_img_size=IMG_SIZE, channels=channels)
                    if img is None:
                        continue
                    # Normalizing
                    if normalize_train:
                        img = normalize(img)
                    
                    # Subtracting Mean
                    # Mean must be calculated ONLY on the training set
                    if subtract_mean:
                        mean_subtract = MeanProcess(mean_subtraction, channels)
                        img = mean_subtract.mean_preprocess(img, channels)
                        
                    # Appending to train set
                    train.append([img, class_label])
                    count +=1 

                    if display_count is True:
                        _printTotal(count, item)
                else:
                    break

        # Shuffling the Training Set
        if isShuffle is True:
            train = shuffle(train)

        # Converting to Numpy
        train = np.array(train)

        # Saves the Train set as a .npy file
        if save_train is True:
            #Converts to Numpy and saves
            if destination_filename.endswith('.npy'):
                print('[INFO] Saving as .npy file')
            elif destination_filename.endswith('.npz'):
                print('[INFO] Saving as .npz file')
            
            since = time.time()
            # Saving
            saveNumpy(destination_filename, train)
            end = time.time()
            
            time_elapsed = end-since

            print('[INFO] {} saved! Took {:.0f}m {:.0f}s'.format(destination_filename, time_elapsed // 60, time_elapsed % 60))

        #Returns Training Set
        end_preprocess = time.time()
        time_elapsed_preprocess = end_preprocess-since_preprocess
        print('----------------------------------------------')
        print('[INFO] Preprocessing complete! Took {:.0f}m {:.0f}s'.format(time_elapsed_preprocess // 60, time_elapsed_preprocess % 60))

        return train, classes

def _printTotal(count, category):
    print(f'{count} - {category}')

def check_mean_subtraction(value, channels):
    """
        Checks if mean subtraction values are valid based on the number of channels
        Must be a tuple of dimensions = number of channels
    Returns boolean value
        True -> Expression is valid
        False -> Expression is invalid
    """
    if value is None:
        return False
    elif type(value) is tuple and len(value) == channels:
        return True
    else:
        raise ValueError(f'[ERROR] Expected a tuple of dimension {channels}', value) 

def shuffle(train):
    """
    Shuffles the Array
    """
    import random
    random.shuffle(train)
    return train

def sep_train(train, IMG_SIZE=None, channels=1):
    # x = []
    # y = []
    # for feature, label in train:
    #     x.append(feature)
    #     y.append(label)
    
    if IMG_SIZE is None:
        raise ValueError('[ERROR] IMG_SIZE not defined')
    else:
        x = [i[0] for i in train]
        y = [i[1] for i in train]

        # Without reshaping, X.shape --> (no. of images, IMG_SIZE, IMG_SIZE)
        # On reshaping, X.shape --> (no. of images, IMG_SIZE, IMG_SIZE,channels)

        # Converting to Numpy + Reshaping X
        x = reshape(x, IMG_SIZE, channels)
        y = np.array(y)

        return x, y

def reshape(x, IMG_SIZE, channels):
    return np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE, channels)

def normalize(x, dtype='float32'):
    """
    Normalizes the data to mean 0 and standard deviation 1
    """
    # x/=255.0 raises a TypeError
    # x = x/255.0
    
    # Converting to float32 and normalizing (float32 saves memory)
    x = x.astype(dtype) / 255
    return x