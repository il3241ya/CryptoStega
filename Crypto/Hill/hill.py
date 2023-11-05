import numpy as np
import random
import check_correct_inp


def main():
    """
    Main function for Hill cipher encryption and decryption.
    """
    try:
        open_text = input("Enter the text: ")
        block_size = int(input("Enter the block size: "))
        matrix_key = []
        print(f"Enter a rows of the key matrix ({block_size}x{block_size}):")
        for i in range(block_size):
            tp = list(map(int, input().split()))
            matrix_key.append(tp)
        matrix_key = np.array(matrix_key)
        open_text = from_text_to_num(open_text)
        en_de = input("Enter 'en' for encryption or 'de' for decryption: ")

        result = check_correct_inp.check(matrix_key, block_size, open_text)

        if result:
            if en_de == 'en':
                encrypt(open_text, block_size, matrix_key)
            if en_de == 'de':
                decrypt(open_text, block_size, matrix_key)

    except ValueError as e:
        print(str(e))
        main()


def from_text_to_num(open_text: str) -> list:
    """
    Convert a string of characters to a list of numeric values.

    Args:
        open_text (str): Input text.

    Returns:
        list: List of numeric values representing the input text.
    """
    open_text_num = []
    for i in open_text:
        open_text_num.append(ord(i) - 97)
    return open_text_num


def add_rand(open_text: list, block_size: int) -> list:
    """
    Add random values to the open_text list to make its length a multiple of block_size.

    Args:
        open_text (list): List of numeric values.
        block_size (int): Block size.

    Returns:
        list: Extended list with random values.
    """
    dop = block_size - len(open_text) % block_size
    for i in range(dop):
        random_addition = random.randint(0, 26)
        open_text.append(random_addition)
    return open_text


def encrypt(open_text: list, block_size: int, matrix_key: np.array) -> str:
    """
    Encrypt the open_text using the Hill cipher.

    Args:
        open_text (list): List of numeric values.
        block_size (int): Block size.
        matrix_key (np.array): Key matrix.

    Returns:
        str: Encrypted text.
    """
    close_text = ''
    if len(open_text) % block_size != 0:
        open_text = add_rand(open_text, block_size)

    for i in range(0, len(open_text) - block_size + 1, block_size):
        row_open_text = np.array(open_text[i: i + block_size])
        for k in range(block_size):
            row_key = np.array(matrix_key[k, :])
            close_text += chr(97 + int((row_key.dot(row_open_text))) % 26)

    print("Encrypted text:\n", close_text)
    return close_text


def find_rev_det(det: int) -> int:
    """
    Find the multiplicative inverse of a determinant modulo 26.

    Args:
        det (int): Determinant.

    Returns:
        int: Multiplicative inverse of the determinant modulo 26.
    """
    for x in range(1, 26):
        if (det * x) % 26 == 1:
            rev_det = x
    return rev_det


def find_rev(matrix_key: np.array, block_size: int) -> np.array:
    """
    Find the inverse of a matrix modulo 26.

    Args:
        matrix_key (np.array): Key matrix.
        block_size (int): Block size.

    Returns:
        np.array: Inverse of the matrix modulo 26.
    """
    inv = np.linalg.inv(matrix_key)
    det = np.linalg.det(matrix_key) % 26
    rev_det = find_rev_det(round(det))
    for i in range(block_size):
        for j in range(block_size):
            inv[i][j] = (((inv[i][j] * (np.linalg.det(matrix_key))) * rev_det) % 26)
    return inv


def decrypt(close_text: list, block_size: int, matrix_key: np.array) -> str:
    """
    Decrypt the close_text using the Hill cipher.

    Args:
        close_text (list): List of numeric values.
        block_size (int): Block size.
        matrix_key (np.array): Key matrix.

    Returns:
        str: Decrypted text.
    """
    open_text = ''
    decrypt_key = find_rev(matrix_key, block_size)
    for i in range(0, len(close_text) - block_size + 1, block_size):
        row_close_text = np.array(close_text[i: i + block_size])
        for k in range(block_size):
            row_key = np.array(decrypt_key[k, :])
            open_text += chr(97 + round((row_key.dot(row_close_text))) % 26)

    print("Decrypted text:\n", open_text)
    return open_text


if __name__ == "__main__":
    main()
