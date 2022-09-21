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
                # Else shift to the next letter
            else:
                char = chr(ord(char) + 1)

        # If char not alphanumeric just continue

        return result


print("Message to encrypt : ", msg)
print("Cipher: ", encrypt(msg))
