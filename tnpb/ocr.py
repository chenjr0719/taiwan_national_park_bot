from io import BytesIO

import cv2
import numpy as np
import pytesseract
from PIL import Image


def get_verify_code(verify_image):
    """
    Use tesseract to get the verify code from image
    :param verify_image bytes: The verify image
    :return: The verify code
    :rtype: str
    """
    img = Image.open(BytesIO(verify_image))
    img = img.convert("RGB")
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 3)

    verify_code = pytesseract.image_to_string(img)
    return verify_code
