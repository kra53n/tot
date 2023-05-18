import io

import numpy as np
from PIL import Image, ImageFilter


def process_img(img_bytes: io.BytesIO) -> io.BytesIO:
    img = Image.open(io.BytesIO(img_bytes))

    kernel = ImageFilter.Kernel(size=(3, 3), kernel=[
        -1, -1, -1,
        -1,  9, -1,
        -1, -1, -1,
    ])
    filtered_img = img.filter(kernel)

    filename = 'last_filtered_img.jpg'
    filtered_img.save(filename)
    with open(filename, 'rb') as f:
        file = f.read()
    return file
