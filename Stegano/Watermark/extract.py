from PIL import Image
import numpy as np


def read_to_matrix(container: Image, h_image: int, w_image: int):
    """
    Read the image into a matrix.

    Args:
        container (Image): The image container.
        h_image (int): Height of the image.
        w_image (int): Width of the image.

    Returns:
        numpy.ndarray: The image matrix.
    """
    container_mx = []

    for row in range(h_image):
        b_row = []
        for col in range(w_image):
            pos = (col, row)
            r, g, b = container.getpixel(pos)
            b -= 128
            b_row.append(b)

        container_mx.append(b_row)
    container_mx = np.array(container_mx)
    return container_mx


def slicing(container):
    """
    Slice the image matrix into subarrays.

    Args:
        container (numpy.ndarray): The image matrix.

    Returns:
        numpy.ndarray: The sliced matrix.
    """
    subarrays = []
    h, w = container.shape
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            subarray = [row[j:j + 8] for row in container[i:i + 8]]
            subarrays.append(subarray)
    slice_array = np.array(subarrays)

    return slice_array


def dct_forming():
    """
    Form the Discrete Cosine Transform (DCT) matrix.

    Returns:
        numpy.ndarray: The DCT matrix.
    """
    f_r_item = 0.354  # For the first row
    first_row = []
    dct_matrix = []

    for i in range(8):
        first_row.append(f_r_item)
    dct_matrix.append(first_row)

    for i in range(1, 8):
        row = []
        for j in range(8):
            val = ((2 * j + 1) * i * np.pi) / 16
            item = 0.5 * np.cos(val)
            row.append(round(item, 3))
        dct_matrix.append(row)

    dct_matrix = np.array(dct_matrix)

    return dct_matrix


def dct(sector):
    """
    Apply the Discrete Cosine Transform (DCT) to a sector.

    Args:
        sector (numpy.ndarray): The image sector.

    Returns:
        numpy.ndarray: The transformed sector.
    """
    dct_mx = dct_forming()
    return np.matmul(np.matmul(dct_mx, sector), dct_mx.T)


def extraction(stego_cont: Image, t_inp):
    """
    Extract bits from a stego container image.

    Args:
        stego_cont (Image): The stego container image.
        t_inp (int): T value.

    Returns:
        list: The extracted bits.
    """
    np.set_printoptions(suppress=True)
    stego_cont = stego_cont.convert('RGB')
    w_image, h_image = stego_cont.size
    container_matrix = read_to_matrix(stego_cont, h_image, w_image)
    container_matrix = slicing(container_matrix)
    t = t_inp
    bits = []

    first_sector = container_matrix[0]
    first_sector_DCT = dct(first_sector)

    for i in range(len(container_matrix) - 1):
        sector_default = container_matrix[i]
        sector_DCT = dct(sector_default)
        next_sector_default = container_matrix[i + 1]
        next_sector_DCT = dct(next_sector_default)
        x_0 = 0
        y_0 = 4
        b1 = sector_DCT[y_0][x_0]
        b2 = next_sector_DCT[y_0][x_0]
        delta_LR = b1 - b2

        if (delta_LR < -t) or (0 < delta_LR < t):
            bits.append(1)
        else:
            bits.append(0)

        x_0 = 0
        y_0 = 5
        b1 = sector_DCT[y_0][x_0]
        b2 = next_sector_DCT[y_0][x_0]
        delta_LR = b1 - b2

        if (delta_LR < -t) or (0 < delta_LR < t):
            bits.append(1)
        else:
            bits.append(0)

    x_0 = 0
    y_0 = 6
    last = len(container_matrix) - 1
    sector_default = container_matrix[last]
    sector_DCT = dct(sector_default)
    next_sector_DCT = first_sector_DCT
    b1 = sector_DCT[y_0][x_0]
    b2 = next_sector_DCT[y_0][x_0]
    delta_LR = b1 - b2

    if (delta_LR < -t) or (0 < delta_LR < t):
        bits.append(1)
    else:
        bits.append(0)

    return bits
