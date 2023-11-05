from PIL import Image, ImageFilter
from functions import save_img


def extraction_filtered(q: int, stego_filtred_img: Image) -> list:
    """
    Extract a binary message from a filtered stego image.

    Args:
        q (int): The quantization step used for embedding.
        stego_filtred_img (Image): The filtered stego image.

    Returns:
        list: A list of extracted binary values.
    """
    stego_filtred_img = stego_filtred_img.convert('RGB')
    size_of_input_img = stego_filtred_img.size

    ext_message_binary = []

    for y in range(size_of_input_img[1]):
        for x in range(size_of_input_img[0]):
            pos = (x, y)
            r_modified, g, b = stego_filtred_img.getpixel(pos)

            P_0 = q * (r_modified // q)
            P_1 = q * (r_modified // q) + (q // 2)

            m_i = min(abs(r_modified - P_0), abs(r_modified - P_1))
            if abs(r_modified - P_0) < abs(r_modified - P_1):
                ext_message_binary.append(0)
            else:
                ext_message_binary.append(1)
    return ext_message_binary


def check(inp_mes: list, ext_mes: list) -> float:
    """
    Calculate the Bit Error Rate (BER) between two binary messages.

    Args:
        inp_mes (list): The input binary message.
        ext_mes (list): The extracted binary message.

    Returns:
        float: The BER (Bit Error Rate) between the two messages.
    """
    B_e = 0
    for i in range(len(inp_mes)):
        if inp_mes[i] != ext_mes[i]:
            B_e += 1
    BER = B_e / len(inp_mes)
    return BER


def blur_and_check(q: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply a blur filter to a stego image and calculate the BER.

    Args:
        q (int): The quantization step used for embedding.
        input_bin (list): The input binary message.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate (BER) after applying the blur filter.
    """
    stego_filtred_img = stego_img.filter(ImageFilter.BLUR)
    ext_mes_bin = extraction_filtered(q, stego_filtred_img)
    BER = check(input_bin, ext_mes_bin)
    
    save_img(stego_filtred_img, "blur")
    return BER


def sharpen_and_check(q: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply a sharpen filter to a stego image and calculate the BER.

    Args:
        q (int): The quantization step used for embedding.
        input_bin (list): The input binary message.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate (BER) after applying the sharpen filter.
    """
    stego_filtred_img = stego_img.filter(ImageFilter.SHARPEN)
    ext_mes_bin = extraction_filtered(q, stego_filtred_img)
    BER = check(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, "sharpen")
    return BER


def smooth_and_check(q: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply a smooth filter to a stego image and calculate the BER.

    Args:
        q (int): The quantization step used for embedding.
        input_bin (list): The input binary message.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate (BER) after applying the smooth filter.
    """
    stego_filtred_img = stego_img.filter(ImageFilter.SMOOTH)
    ext_mes_bin = extraction_filtered(q, stego_filtred_img)
    BER = check(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, "smooth")
    return BER


def contour_and_check(q: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply a contour filter to a stego image and calculate the BER.

    Args:
        q (int): The quantization step used for embedding.
        input_bin (list): The input binary message.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate (BER) after applying the contour filter.
    """
    stego_filtred_img = stego_img.filter(ImageFilter.CONTOUR)
    ext_mes_bin = extraction_filtered(q, stego_filtred_img)
    BER = check(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, 'contour')
    return BER


def detail_and_check(q: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply a detail filter to a stego image and calculate the BER.

    Args:
        q (int): The quantization step used for embedding.
        input_bin (list): The input binary message.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate (BER) after applying the detail filter.
    """
    stego_filtred_img = stego_img.filter(ImageFilter.DETAIL)
    ext_mes_bin = extraction_filtered(q, stego_filtred_img)
    BER = check(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, 'detail')
    return BER


def emboss_and_check(q: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply an emboss filter to a stego image and calculate the BER.

    Args:
        q (int): The quantization step used for embedding.
        input_bin (list): The input binary message.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate (BER) after applying the emboss filter.
    """
    stego_filtred_img = stego_img.filter(ImageFilter.EMBOSS)
    ext_mes_bin = extraction_filtered(q, stego_filtred_img)
    BER = check(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, 'emboss')
    return BER


def grayscale_and_check(q: int, input_bin: list, stego_img: Image) -> float:
    """
    Apply a grayscale filter to a stego image and calculate the BER.

    Args:
        q (int): The quantization step used for embedding.
        input_bin (list): The input binary message.
        stego_img (Image): The stego image.

    Returns:
        float: The Bit Error Rate (BER) after applying the grayscale filter.
    """
    stego_filtred_img = stego_img.convert('L')
    ext_mes_bin = extraction_filtered(q, stego_filtred_img)
    BER = check(input_bin, ext_mes_bin)
    save_img(stego_filtred_img)
