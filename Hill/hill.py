import numpy as np
import random
import check_correct_inp


def inp():
    open_text = input()
    block_size = int(input())
    matrix_key = []
    for i in range(block_size):
        tp = list(map(int, input().split()))
        matrix_key.append(tp)
    matrix_key = np.array(matrix_key)
    open_text = from_text_to_num(open_text)
    en_de = input()

    if check_correct_inp.check(matrix_key, block_size, open_text) == 4:
        if en_de == 'en':
            encrypt(open_text, block_size, matrix_key)
        if en_de == 'de':
            decrypt(open_text, block_size, matrix_key)
    if check_correct_inp.check(matrix_key, block_size, open_text) == 1:
        print("error key, determinant = 0")
        inp()
    if check_correct_inp.check(matrix_key, block_size, open_text) == 2:
        print("error key, NOD(determinant, 26) != 1")
        inp()
    if check_correct_inp.check(matrix_key, block_size, open_text) == 3:
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


def encrypt(open_text: list, block_size: int, matrix_key: np.array) -> str:
    close_text = ''
    if len(open_text) % block_size != 0:
        open_text = add_rand(open_text, block_size)


    for i in range(0, len(open_text)-block_size+1, block_size):

        row_open_text = np.array(open_text[i: i + block_size])
        for k in range(block_size):
            row_key = np.array(matrix_key[k, :])
            close_text += chr(97 +int((row_key.dot(row_open_text))) % 26)

    print("close text:\n", close_text)

    return close_text

def find_rev_det(det: int) -> int:
    for x in range(1, 26):
        if (det * x) % 26 == 1:
            rev_det = x
    return rev_det

def find_rev(matrix_key: np.array, block_size: int) -> np.array:
    inv = np.linalg.inv(matrix_key)
    det = np.linalg.det(matrix_key)%26
    rev_det = find_rev_det(round(det))

    for i in range(block_size):
        for j in range(block_size):
            inv[i][j] = (((inv[i][j] * (np.linalg.det(matrix_key))) * rev_det) % 26)
            #print(np.linalg.det(matrix_key))
            #print(rev_det)

    return inv

def decrypt(close_text: list, block_size: int, matrix_key: np.array) -> str:
    open_text = ''

    decrypt_key = find_rev(matrix_key, block_size)
    #print("\ndecrypt key:\n", decrypt_key, '\n')
    for i in range(0, len(close_text) - block_size + 1, block_size):

        row_close_text = np.array(close_text[i: i + block_size])
        for k in range(block_size):
            row_key = np.array(decrypt_key[k, :])
            open_text += chr(97 + round((row_key.dot(row_close_text))) % 26)

    print("open text:\n",open_text)

    return open_text

if __name__ == "__main__":
    inp()

