def main():
    """
    Main function to perform text encryption and decryption.
    """

    # Prompt the user for input text in English.
    print("Enter text in English:")
    input_text = input().lower().replace(' ', '')
    input_text = delete_extra(input_text)

    while not eng_alp(input_text):
        # Inform the user about non-English text input.
        print("You entered non-English text. Enter text in English:")
        input_text = input().lower().replace(' ', '')
        input_text = delete_extra(input_text)

    # Prompt the user for the type of encryption.
    print("Choose the encryption type:\n 1 - classic;\n 2 - self-key;\n 3 - self-key by ciphertext.")
    encryption_type = int(input())

    # Prompt the user for the desired action, encryption (en) or decryption (de).
    print("Enter the desired action (en or de):")
    action = input().lower()

    match encryption_type:
        case 1:
            print("Enter the key:")
            key = input().lower()
            key = delete_extra(key)

            while not eng_alp(key):
                # Inform the user about non-English key input.
                print("You entered a non-English key. Enter a key in English:")
                key = input().lower()
                key = delete_extra(key)
        case 2 | 3:
            print("Enter the key:")
            key = input().lower()
            key = delete_extra(key)

            while len(key) != 1:
                # Inform the user about an incorrect key length.
                print("The key length should be equal to 1.")
                key = input().lower()

                while not eng_alp(key):
                    # Inform the user about non-English key input.
                    print("You entered a non-English key. Enter a key in English:")
                    key = input().lower()
                    key = delete_extra(key)

    while action != "en" and action != "de":
        # Inform the user about incorrect action input.
        print("Incorrect action, enter en or de:")
        action = input().lower()

    match action:
        case "en":
            print("Encrypted text:")
            print(encrypt(input_text, key, encryption_type))
        case "de":
            print("Decrypted text:")
            print(decrypt(input_text, key, encryption_type))


def eng_alp(text: str) -> bool:
    """
    Check if the input text consists of English alphabet characters.

    Args:
        text (str): The input text to be checked.

    Returns:
        bool: True if the text contains only English alphabet characters, False otherwise.
    """

    # Check if the input text consists of English alphabet characters.
    for symbol in text:
        if 97 > ord(symbol) or ord(symbol) > 122:
            return False
    return True


def delete_extra(open_text: str) -> str:
    """
    Remove specified non-alphabetic characters from the input text.

    Args:
        open_text (str): The input text from which non-alphabetic characters will be removed.

    Returns:
        str: The input text with non-alphabetic characters removed.
    """

    # Remove specified non-alphabetic characters from the input text.
    for x in "1234567890-=`<>,.":
        open_text = open_text.replace(x, '')
    return open_text


def gamma_forming_encrypt(open_text: str, key: str, encryption_type: int) -> str:
    """
    Generate a gamma string based on the encryption type.

    Args:
        open_text (str): The input text to be encrypted.
        key (str): The encryption key.
        encryption_type (int): The type of encryption to be applied.

    Returns:
        str: The generated gamma string.
    """
    match encryption_type:
        case 1:
            return key * (len(open_text) // len(key) + 1 * int(bool(len(open_text) % len(key))))
        case 2:
            return key + open_text[0: len(open_text) - 1]
        case 3:
            for i in range(len(open_text) - 1):
                key += chr((ord(key[i]) + ord(open_text[i]) - 97 * 2) % 26 + 97)
            return key


def encrypt(open_text: str, key: str, encryption_type: int) -> str:
    """
    Encrypt the input text using the generated gamma string.

    Args:
        open_text (str): The input text to be encrypted.
        key (str): The encryption key.
        encryption_type (int): The type of encryption to be applied.

    Returns:
        str: The encrypted text.
    """
    
    gamma = gamma_forming_encrypt(open_text, key, encryption_type)

    close_text = ''
    for i in range(len(open_text)):
        close_text += chr(97 + (ord(open_text[i]) - 97 + ord(gamma[i]) - 97) % 26)
    return close_text


def gamma_forming_decrypt(close_text: str, key: str, encryption_type: int) -> str:
    """
    Generate a gamma string for decryption based on the encryption type.

    Args:
        close_text (str): The input text to be decrypted.
        key (str): The decryption key.
        encryption_type (int): The type of encryption to be applied.

    Returns:
        str: The generated gamma string for decryption.
    """

    match encryption_type:
        case 1:
            return key * (len(close_text) // len(key) + 1 * int(bool(len(close_text) % len(key))))
        case 2:
            for i in range(len(close_text) - 1):
                key += chr(97 + (ord(close_text[i]) - ord(key[i])) % 26)
            return key
        case 3:
            for i in range(len(close_text) - 1):
                open_sym = chr(((ord(close_text[i]) - 97) - (ord(key[i]) - 97)) % 26 + 97)
                key += chr((ord(key[i]) - 97 + ord(open_sym) - 97) % 26 + 97)
            return key


def decrypt(close_text: str, key: str, encryption_type: int) -> str:
    """
    Decrypt the input text using the generated gamma string for decryption.

    Args:
        close_text (str): The input text to be decrypted.
        key (str): The decryption key.
        encryption_type (int): The type of encryption to be applied.

    Returns:
        str: The decrypted text.
    """

    # Decrypt the input text using the generated gamma string for decryption.
    open_text = ''
    gamma = gamma_forming_decrypt(close_text, key, encryption_type)
    for i in range(len(close_text)):
        open_text += chr(97 + (ord(close_text[i]) - ord(gamma[i]) % 26))
    return open_text


if __name__ == "__main__":
    main()
