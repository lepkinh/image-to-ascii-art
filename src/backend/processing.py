"""
The idea of this file is to contain the algorithm that processes images into ascii and returns to server.
Algorithm concept: image -> image data -> resize image -> grayscale -> map values to ascii -> return

Note: will have to make this file importable, perhaps create a class structure instead of this plan
NOTE: consider reording grayscale and resize, figure out what is the otpimal order for gen case
"""
import PIL.Image
import cv2
import numpy as np

# will need a function that accepts the image file in processing.py or server.py
# notes: should have max and min file sizes and error clauses

# resize an image array
def resize_img(img, new_width=100):
    height, width = img.shape
    # new height is calculated based on the ratio of the new width to the old width
    return cv2.resize(img, (new_width, int(new_width*height/width)))

# function: converts to numpy array, grayscales, resizes
# size 1 50px, size 2 100px, size 3 200px
def process_image(file, size=2):
    file = PIL.Image.open(file)
    data = np.array(file)

    # resize image to a width of 100px
    if size == 1:
        data = resize_img(data, 50)
    elif size == 2:
        data = resize_img(data)
    elif size == 3:
        data = resize_img(data, 200)
    else:
        # raise value error or return error data
        pass
    
    # convert to grayscale
    if len(data.shape) == 3:
        data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    
    return data


# function: maps pixel values to ascii
def ascii(data):
    ascii_chars = "@%#*+=-:. " # can change these to whatever really
    ascii_data = ""
    for row in data:
        for pixel in row:
            ascii_data += ascii_chars[pixel//32]
        ascii_data += "\n"
    return ascii_data

# function: format the ascii in json