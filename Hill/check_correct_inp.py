import numpy as np


def gcd(n1, n2):
    """
    Calculate the greatest common divisor (GCD) of two numbers using Euclidean algorithm.

    Args:
        n1 (int): First number.
        n2 (int): Second number.

    Returns:
        int: GCD of n1 and n2.
    """
    return abs(n1) if n2 == 0 else gcd(n2, n1 % n2)


def check(matrix_key: np.array, block_size: int, open_txt: list) -> int:
    """
    Check the validity of the key matrix and input text for Hill cipher.

    Args:
        matrix_key (np.array): Key matrix.
        block_size (int): Block size.
        open_txt (list): List of numeric values representing the input text.

    Returns:
        int: 4 if all checks pass, otherwise raises ValueError with an error message.
    """
    determinant = round(np.linalg.det(matrix_key)) % 26

    match gcd(determinant, 26):
        case 0:
            raise ValueError("Error: Key determinant is 0")
        case n if (n != 1):
            raise ValueError("Error: GCD(determinant, 26) is not 1")

    for i in range(block_size):
        for j in range(block_size):
            matrix_key[i][j] %= 26

    for x in 'йцукенгшщзхъфывапролджэячсмитьбюё':
        if x in open_txt:
            raise ValueError("Error: Text contains non-English characters")

    return True
