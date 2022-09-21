msg = input("Enter your message to encrypt: ")


def encrypt(message):
    result = ""

    # iterate through the input msg
    for _, char in enumerate(message):

        # Check if character is alphanumeric
        if char.isalpha():

            # Check char is either Z or z and append A, a respectively
            if char == "Z":
                result += "A"
            elif char == "z":
                result += "a"
            else:
                # Add 1 to ascii value of char
                result += chr(ord(char) + 1)

        # Check if character is numeric
        elif char.isnumeric():
            # Add 1 to ascii value of char
            result += chr(ord(char) + 1)
        else:
            # Add char to result
            result += char

    return result


print("Message to encrypt : ", msg)
print("Cipher: ", encrypt(msg))
