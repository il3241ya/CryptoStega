def text_block():
    print("Введите текст:")
    text = input()
    print("Введите размер ключа:")
    block_size = int(input())

    text_list = []
    for n in range(block_size):
        tp_text = ''

        for i in range(n, len(text), block_size):
            tp_text += text[i]

        text_list.append(tp_text)

    for i in range(block_size):
        print(text_list[i])


if __name__ == "__main__":
    text_block()