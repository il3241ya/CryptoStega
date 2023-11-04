from PIL import Image


def check_size(size_of_img: tuple, input_message: str) -> bool:
    """
    Check if the image size can accommodate the given message.

    Args:
        size_of_img (tuple): A tuple representing the image size (width, height).
        input_message (str): The input message to be embedded in the image.

    Returns:
        bool: True if the message can fit in the image, False otherwise.
    """
    if size_of_img[0] * size_of_img[1] >= len(input_message) * 8:
        return True
    else:
        return False


def string_to_binary(input_message_str: str) -> list:
    """
    Convert a string message to a binary list.

    Args:
        input_message_str (str): The input message string.

    Returns:
        list: A list of binary values representing the input message.
    """
    input_message_bin = []
    for ch in input_message_str:
        input_message_bin.extend([int(bit) for bit in bin(ord(ch))[2:].zfill(8)])
    return input_message_bin


def save_img(image: Image, name: str):
    """
    Save the image to a file.

    Args:
        image (Image): The image to be saved.
        name (str): The name of the output image file.
    """
    image.save("out_img/" + name + ".PNG", "PNG")


def binary_to_string(input_message_bin: list) -> str:
    """
    Convert a binary list to a string message.

    Args:
        input_message_bin (list): A list of binary values representing the message.

    Returns:
        str: The decoded string message.
    """
    input_message_str = ""
    for i in range(0, len(input_message_bin), 8):
        ch = chr(int("".join(map(str, input_message_bin[i: i + 8])), 2))
        input_message_str += ch
    return input_message_str
