import numpy as np
import random
import check_correct_inp


def inp():
    open_text = input()
    block_size = int(input())
    matrix_key_1 = []

    for i in range(block_size):
        tp = list(map(int, input().split()))
        matrix_key_1.append(tp)

    matrix_key_1 = np.array(matrix_key_1)

    matrix_key_2 = []

    for i in range(block_size):
        tp = list(map(int, input().split()))
        matrix_key_2.append(tp)

    matrix_key_2 = np.array(matrix_key_2)

    open_text = from_text_to_num(open_text)
    en_de = input()


    if check_correct_inp.check(matrix_key_1, block_size, open_text) == 4 \
            and check_correct_inp.check(matrix_key_2, block_size, open_text) == 4:
        if en_de == 'en':
            encrypt(open_text, block_size, matrix_key_1, matrix_key_2)
        if en_de == 'de':
            decrypt(open_text, block_size, matrix_key_1, matrix_key_2)
    if check_correct_inp.check(matrix_key_1, block_size, open_text) == 1 \
            and check_correct_inp.check(matrix_key_2, block_size, open_text) == 1:
        print("error key, determinant = 0")
        inp()
    if check_correct_inp.check(matrix_key_1, block_size, open_text) == 2 \
            and check_correct_inp.check(matrix_key_2, block_size, open_text) == 2:
        print("error key, NOD(determinant, 26) != 1")
        inp()
    if check_correct_inp.check(matrix_key_1, block_size, open_text) == 3\
            and check_correct_inp.check(matrix_key_2, block_size, open_text) == 3:
        print("error text")
        inp()

def from_text_to_num(open_text: str) -> list:
    open_text_num = []

    for i in open_text:
        open_text_num.append(ord(i)-97)

    return open_text_num

def add_rand(open_text: list, block_size: int) -> list:
    dop = block_size - len(open_text) % block_size

    for i in range(dop):
        random_addition = random.randint(0, 26)
        #print(random_addition)
        open_text.append(random_addition)

    return open_text

def create_matrix_key(matrix_key_1: np.array, matrix_key_2: np.array, block_size: int) -> np.array:
    matrix_key = np.dot(matrix_key_1, matrix_key_2)
    #print(matrix_key, "do")
    for i in range(block_size):
        for j in range(block_size):
            matrix_key[i][j] %= 26
    #print(matrix_key, "posle")
    return matrix_key

def encrypt(open_text: list, block_size: int, matrix_key_1: np.array, matrix_key_2: np.array) -> str:
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
    return close_text

def decrypt(close_text: list, block_size: int, matrix_key_1: np.array, matrix_key_2: np.array) -> str:
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
    return open_text


def find_rev_det(det: int) -> int:

    for x in range(1, 26):
        if (det * x) % 26 == 1:
            rev_det = x
    return rev_det
def find_rev(matrix_key: np.array, block_size: int) -> np.array:
    inv = np.linalg.inv(matrix_key)
    det = np.linalg.det(matrix_key)%26
    rev_det = find_rev_det(int(det))

    for i in range(block_size):
        for j in range(block_size):
            inv[i][j] = round(((inv[i][j] * (np.linalg.det(matrix_key))) * rev_det) % 26)
    #print(inv)
    return inv

if __name__ == "__main__":
    inp()
