def index_func(text: str, n: int) -> float:
    dict = {}
    l=0
    for i in range(0, len(text), n):
        key = text[i]
        if key not in dict:
            dict[key] = 0
        else:
            dict[key] += 1
        l += 1

    index = 0

    for key in "qwertyuiopasdfghjklzxcvbnm":
        if key in dict:
            f = dict[key]
        else:
            f = 0
        index += f * (f - 1)

    return index / (l * (l - 1))


if __name__ == "__main__":
    print("Введите зашифрованный текст:")
    text = input()
    block_size = int(input())
    for n in range(2, block_size):
        print("Длина блока - ", n, "Индекс совпадения - ", index_func(text, n))




