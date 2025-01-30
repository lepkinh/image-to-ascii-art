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
    try:
        # img isconverted grayscaled when loaded, this prevents having to deal with weird img types
        img = PIL.Image.open(file).convert("L")
        data = np.array(img)

        # resizing the image data to appropriate width
        size_map = {1: 50, 2: 100, 3: 200}
        new_width = size_map.get(size, 100)
        data = resize_img(data, new_width)

        return data
    # exception invalid file
    except Exception as e:
        print(f"Failure in process_image(): {e}")
        return None


# function: convert pixel values to ascii (API route)
def ascii(data):
    # can change these characters to anything NOTE: play around with these
    ascii_chars = "@%#*+=-:. " 
    ascii_data = []
    for row in data:
        ascii_row = "".join(ascii_chars[pixel // 32] for pixel in row)
        ascii_data.append(ascii_row)
    return "\n".join(ascii_data)

