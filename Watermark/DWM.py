import numpy as np
from PIL import Image


def get_watermark(type_w: str) -> np.ndarray:
    """
    Get the watermark image based on the specified type.

    Args:
        type_w (str): The type of watermark to retrieve.

    Returns:
        np.ndarray: The watermark image as a two-dimensional array.
    """
    match type_w:
        case '1':
            watermark_3 = Image.open('in_watermark/32.png').convert('L')
            array3 = np.array(watermark_3)
            return array3
        case '2':
            watermark2 = Image.open('in_watermark/16x16.PNG').convert('L')
            array2 = np.array(watermark2)
            return array2
        case '3':
            watermark1 = Image.open('in_watermark/watermark2.PNG').convert('L')
            array1 = np.array(watermark1)
            return array1
        case _:
            try:
                watermark_custom = Image.open(f'in_watermark/{type_w}').convert('L')
                arrayc = np.array(watermark_custom)
                return arrayc
            except:
                return 0
