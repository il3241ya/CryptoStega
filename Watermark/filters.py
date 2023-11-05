from PIL import Image, ImageFilter
import extract

def save_img(image: Image, name: str):
    """
    Save an image with a given name.

    Args:
        image (Image): The image to save.
        name (str): The name for the saved image.
    """
    image.save("out_img/" + name + ".PNG", "PNG")


def to_list(matrix):
    """
    Convert a matrix to a binary list.

    Args:
        matrix (list): The input matrix.

    Returns:
        list: The binary list.
    """
    row = []
    for j in range(len(matrix)):
        for i in range(len(matrix[0])):
            if matrix[j][i] == 0.0 or matrix[j][i] == 0:
                row.append(0)
            else:
                row.append(1)
    return row


def CHECK(inp_mes: list, ext_mes: list) -> float:
    """
    Check for Bit Error Rate (BER) between two message lists.

    Args:
        inp_mes (list): The input message list.
        ext_mes (list): The extracted message list.

    Returns:
        float: The Bit Error Rate.
    """
    B_e = 0

    for i in range(len(inp_mes)):
        if inp_mes[i] != ext_mes[i]:
            B_e += 1
    BER = B_e / len(inp_mes)

    return BER


def blur_and_check(t_inp: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply blur filter to an image and check for BER.

    Args:
        t_inp (int): T value.
        input_bin (list): Input binary data.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate.
    """
    stego_filtered_img = stego_img.filter(ImageFilter.BLUR)
    ext_mes_bin = extract.extraction(stego_filtered_img, t_inp)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtered_img, "1")
    
    return BER


def sharpen_and_check(t_inp: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply sharpen filter to an image and check for BER.

    Args:
        t_inp (int): T value.
        input_bin (list): Input binary data.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate.
    """
    stego_filtered_img = stego_img.filter(ImageFilter.SHARPEN)
    ext_mes_bin = extract.extraction(stego_filtered_img, t_inp)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtered_img, "2")
    
    return BER


def smooth_and_check(t_inp: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply smooth filter to an image and check for BER.

    Args:
        t_inp (int): T value.
        input_bin (list): Input binary data.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate.
    """
    stego_filtered_img = stego_img.filter(ImageFilter.SMOOTH)
    ext_mes_bin = extract.extraction(stego_filtered_img, t_inp)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtered_img, "4")
    
    return BER


def contour_and_check(t_inp: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply contour filter to an image and check for BER.

    Args:
        t_inp (int): T value.
        input_bin (list): Input binary data.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate.
    """
    stego_filtered_img = stego_img.filter(ImageFilter.CONTOUR)
    ext_mes_bin = extract.extraction(stego_filtered_img, t_inp)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtered_img, '3')
    
    return BER


def jpg_scale_90(t_inp: int, input_bin: list, stego_img: Image) -> float:
    """
    Compress an image at 90% quality and check for BER.

    Args:
        t_inp (int): T value.
        input_bin (list): Input binary data.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate.
    """
    stego_img.save("out_img/compressed_image_90.jpg", format="JPEG", quality=90)
    stego_filtered_img = Image.open("out_img/compressed_image_90.jpg")
    ext_mes_bin = extract.extraction(stego_filtered_img, t_inp)
    BER = CHECK(input_bin, ext_mes_bin)
    
    return BER


def jpg_scale_60(t_inp: int, input_bin: list, stego_img: Image) -> float:
    """
    Compress an image at 60% quality and check for BER.

    Args:
        t_inp (int): T value.
        input_bin (list): Input binary data.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate.
    """
    stego_img.save("out_img/compressed_image_60.jpg", format="JPEG", quality=60)
    stego_filtered_img = Image.open("out_img/compressed_image_60.jpg")
    ext_mes_bin = extract.extraction(stego_filtered_img, t_inp)
    BER = CHECK(input_bin, ext_mes_bin)
    
    return BER


def jpg_scale_20(t_inp: int, input_bin: list, stego_img: Image) -> float:
    """
    Compress an image at 20% quality and check for BER.

    Args:
        t_inp (int): T value.
        input_bin (list): Input binary data.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate.
    """
    stego_img.save("out_img/compressed_image_20.jpg", format="JPEG", quality=20)
    stego_filtered_img = Image.open("out_img/compressed_image_20.jpg")
    ext_mes_bin = extract.extraction(stego_filtered_img, t_inp)
    BER = CHECK(input_bin, ext_mes_bin)
    
    return BER
