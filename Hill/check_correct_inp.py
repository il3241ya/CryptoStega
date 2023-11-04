import numpy as np

def nod(n1, n2):
    if n1 == 0:
        return n2
    return nod(n2 % n1, n1)

def check(matrix_key: np.array, block_size: int, open_txt: list) -> int:

    determinant = round(np.linalg.det(matrix_key))%26

    if determinant == 0:
        return 1
    n = nod(determinant, 26)
    if n != 1:
        print(determinant, 1)
        return 2

    for i in range(block_size):
        for j in range(block_size):
            if matrix_key[i][j] >= 26:
                matrix_key[i][j] %= 26

    for x in 'йцукенгшщзхъфывапролджэячсмитьбюё':
        if x in open_txt:
             return 3


    return 4


