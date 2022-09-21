ciph = input('Enter your encrypted message: ')


def decrypt(cipher):
    result = ""
    # Iterate through the cipher
    for _, char in enumerate(cipher):

        print(char)

        # Check if character is alphanumeric
        if char.isalpha():

            # Check char is either Z or z and append A, a respectively
            if char == "A":
                result += "Z"
            elif char == "a":
                result += "z"
            else:
                # Else shift letter one below
                result += chr(ord(char) - 1)
        else:
            result += char

    return result


print("Cipher was :", ciph)
print("Decrypted message is :", decrypt(ciph))
