"""
The idea of this file is to contain the algorithm that processes images into ascii and returns to server.
Algorithm idea: image -> image data -> resize image -> grayscale -> map values to ascii -> return
"""
import PIL.Image
import cv2
import numpy as np


def resize_img(img, new_width=100):
    """
    Resizes img data in an array without adjusting aspect ratio.

    Parameters:
    img: numpy array, the image data
    new_width: int, the new width of the image, default is 100 (size 2/medium)

    Returns:
    numpy array, the resized image data
    """
    height, width = img.shape

    # new height is calculated based on the ratio of the new width to the old width
    return cv2.resize(img, (new_width, int(new_width*height/width)))


def process_image(file, size=2):
    """ 
    Processess img file into a resized, grayscaled numpy array.

    Parameters:
    file: file, the image file
    size: int, the size of the ascii image, default is 2 (medium)

    Returns:
    numpy array, the processed image data
    """
    try:
        # img isconverted grayscaled when loaded, this prevents having to deal with weird img types
        img = PIL.Image.open(file).convert("L")
        data = np.array(img)

        # resizing the image data to appropriate width
        size_map = {1: 50, 2: 100, 3: 200}

        try:
            new_width = size_map.get(size, 100)
            data = resize_img(data, new_width)
        except Exception as e:
            print(f"Failure in resize_img(): {e}")
            return None

        return data
    # exception invalid file
    except Exception as e:
        print(f"Failure in process_image(): {e}")
        return None


# function: convert pixel values to ascii (API route)
def ascii(data):
    """ 
    Converts img data (numpy array) into ascii art.

    Parameters:
    data: numpy array, the image data

    Returns:
    str, the ascii art representation of the image
    """
    # can change these characters to anything NOTE: play around with these
    ascii_chars = "@%#*+=-:. " 
    ascii_data = []
    for row in data:
        ascii_row = "".join(ascii_chars[pixel // 32] for pixel in row)
        ascii_data.append(ascii_row)
    return "\n".join(ascii_data)

