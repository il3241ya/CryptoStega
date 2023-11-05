from vigener import decrypt


def brutforcer():
	print("Введите закрытый текст:")
	text = input()

	print("Введите тип шифра:\n 1 - самоключ;\n 2 - самоключ по шифротексту.")
	type = int(input())

	while type != 1 or type != 2:
		print("Введите тип шифра:\n 1 - самоключ;\n 2 - самоключ по шифротексту.")
		type = int(input())

	for key in "qwertyuiopasdfghjklzxcvbnm":
		open_text = decrypt(text, key, type+1)
		print(key,'-',open_text[:40])


if __name__ == "__main__": 
	brutforcer()