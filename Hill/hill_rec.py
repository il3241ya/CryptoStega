import numpy as np
import random
import check_correct_inp


def main():
    """
    Main function to interact with the user and perform Hill Cipher encryption/decryption.
    """
    try:
        open_text = input("Enter the text: ")
        block_size = int(input("Enter the block size: "))
        
        matrix_key_1 = get_matrix_key(block_size, f"Enter a rows of the first key matrix ({block_size}x{block_size}):")
        matrix_key_2 = get_matrix_key(block_size, f"Enter a rows of the second key matrix ({block_size}x{block_size}):")

        open_text = from_text_to_num(open_text)
        en_de = input("Enter 'en' for encryption or 'de' for decryption: ")

        if check_matrix_keys(matrix_key_1, matrix_key_2, block_size, open_text):
            if en_de == 'en':
                encrypt(open_text, block_size, matrix_key_1, matrix_key_2)
            elif en_de == 'de':
                decrypt(open_text, block_size, matrix_key_1, matrix_key_2)
    except ValueError as e:
        print(str(e))
        main()


def get_matrix_key(block_size: int, prompt: str) -> np.array:
    """
    Get the matrix key from the user.

    Args:
        block_size (int): Block size.
        prompt (str): A prompt to ask the user for the matrix key.

    Returns:
        np.array: The matrix key as a NumPy array.
    """
    matrix_key = []
    print(prompt)
    for _ in range(block_size):
        row = list(map(int, input().split()))
        matrix_key.append(row)
    return np.array(matrix_key)


def check_matrix_keys(matrix_key_1: np.array, matrix_key_2: np.array, block_size: int, open_text: list) -> bool:
    """
    Check the validity of the matrix keys for Hill cipher.

    Args:
        matrix_key_1 (np.array): First matrix key.
        matrix_key_2 (np.array): Second matrix key.
        block_size (int): Block size.
        open_text (list): List of numeric values representing the input text.

    Returns:
        bool: True if the matrix keys are valid, False otherwise.
    """
    try:
        check_correct_inp.check(matrix_key_1, block_size, open_text)
        check_correct_inp.check(matrix_key_2, block_size, open_text)
    except ValueError as e:
        print(e)
        return False
    return True


def from_text_to_num(open_text: str) -> list:
    """
    Convert the input text to a list of numeric values.

    Args:
        open_text (str): The input text.

    Returns:
        list: A list of numeric values.
    """
    open_text_num = []

    for i in open_text:
        open_text_num.append(ord(i)-97)

    return open_text_num


def add_rand(open_text: list, block_size: int) -> list:
    """
    Add random values to the input text to ensure it's a multiple of the block size.

    Args:
        open_text (list): List of numeric values.
        block_size (int): Block size.

    Returns:
        list: The input text with random padding.
    """
    dop = block_size - len(open_text) % block_size

    for i in range(dop):
        random_addition = random.randint(0, 26)
        #print(random_addition)
        open_text.append(random_addition)

    return open_text


def create_matrix_key(matrix_key_1: np.array, matrix_key_2: np.array, block_size: int) -> np.array:
    """
    Create a matrix key by multiplying two matrix keys.

    Args:
        matrix_key_1 (np.array): First matrix key.
        matrix_key_2 (np.array): Second matrix key.
        block_size (int): Block size.

    Returns:
        np.array: The resulting matrix key.
    """
    matrix_key = np.dot(matrix_key_1, matrix_key_2)
    for i in range(block_size):
        for j in range(block_size):
            matrix_key[i][j] %= 26
    return matrix_key


def encrypt(open_text: list, block_size: int, matrix_key_1: np.array, matrix_key_2: np.array) -> str:
    """
    Encrypt the input text using the Hill Cipher.

    Args:
        open_text (list): List of numeric values.
        block_size (int): Block size.
        matrix_key_1 (np.array): First matrix key.
        matrix_key_2 (np.array): Second matrix key.

    Returns:
        str: The encrypted text.
    """
    close_text = ''
    if len(open_text) % block_size != 0:
        open_text = add_rand(open_text, block_size)

    row_open_text = np.array(open_text[0: block_size])
    for k in range(block_size):
        row_key = np.array(matrix_key_1[k, :])
        close_text += chr(97 + round((row_key.dot(row_open_text))) % 26)

    row_open_text = np.array(open_text[block_size: 2*block_size])
    for k in range(block_size):
        row_key = np.array(matrix_key_2[k, :])
        close_text += chr(97 + round((row_key.dot(row_open_text))) % 26)

    matrix_key_i = create_matrix_key(matrix_key_2, matrix_key_1, block_size)

    for i in range(2*block_size, len(open_text)-block_size+1, block_size):

        row_open_text = np.array(open_text[i: i + block_size])
        for k in range(block_size):
            row_key = np.array(matrix_key_i[k, :])
            close_text += chr(97 +round((row_key.dot(row_open_text))) % 26)


        matrix_key_1 = matrix_key_2
        matrix_key_2 = matrix_key_i

        matrix_key_i = create_matrix_key(matrix_key_2, matrix_key_i, block_size)

    print("close text:\n",close_text)


def decrypt(close_text: list, block_size: int, matrix_key_1: np.array, matrix_key_2: np.array) -> str:
    """
    Decrypt the input text using the Hill Cipher.

    Args:
        close_text (list): List of numeric values representing the encrypted text.
        block_size (int): Block size.
        matrix_key_1 (np.array): First matrix key.
        matrix_key_2 (np.array): Second matrix key.

    Returns:
        str: The decrypted text.
    """
    open_text = ''

    matrix_key_1 = find_rev(matrix_key_1, block_size)
    matrix_key_2 = find_rev(matrix_key_2, block_size)

    row_close_text = np.array(close_text[0: block_size])
    for k in range(block_size):
        row_key = np.array(matrix_key_1[k, :])
        open_text += chr(97 + round((row_key.dot(row_close_text))) % 26)

    row_close_text = np.array(close_text[block_size: 2 * block_size])
    for k in range(block_size):
        row_key = np.array(matrix_key_2[k, :])
        open_text += chr(97 + round((row_key.dot(row_close_text))) % 26)


    matrix_key_i = create_matrix_key(matrix_key_1, matrix_key_2, block_size)

    for i in range(2 * block_size, len(close_text) - block_size + 1, block_size):

        row_close_text = np.array(close_text[i: i + block_size])
        for k in range(block_size):
            row_key = np.array(matrix_key_i[k, :])
            open_text += chr(97 + round((row_key.dot(row_close_text))) % 26)

        matrix_key_1 = matrix_key_2
        matrix_key_2 = matrix_key_i

        matrix_key_i = create_matrix_key(matrix_key_1, matrix_key_2, block_size)

    print("open text:\n",open_text)


def find_rev_det(det: int) -> int:
    """
    Find the modular multiplicative inverse of the determinant.

    Args:
        det (int): The determinant value.

    Returns:
        int: The modular multiplicative inverse.
    """
    for x in range(1, 26):
        if (det * x) % 26 == 1:
            rev_det = x
    return rev_det


def find_rev(matrix_key: np.array, block_size: int) -> np.array:
    """
    Find the inverse of a matrix key.

    Args:
        matrix_key (np.array): The matrix key to find the inverse for.
        block_size (int): Block size.

    Returns:
        np.array: The inverse of the matrix key.
    """
    inv = np.linalg.inv(matrix_key)
    det = np.linalg.det(matrix_key)%26
    rev_det = find_rev_det(int(det))

    for i in range(block_size):
        for j in range(block_size):
            inv[i][j] = round(((inv[i][j] * (np.linalg.det(matrix_key))) * rev_det) % 26)
    
    return inv

if __name__ == "__main__":
    main()