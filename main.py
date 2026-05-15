#!/home/ilya/projects/Password-generator/.venv/bin/python
import random
import string
import sys

import pyperclip

chars = [string.digits, string.ascii_uppercase, string.ascii_lowercase, string.punctuation]
exception_words = ["--help", "-h"]

def pass_gen(length: int) -> str:
    ps_is_correct = False

    while not ps_is_correct:

        used_types = [0, 0, 0, 0]

        password = ""

        for _ in range(length):
            type_ = random.randint(0, len(chars)-1)
            password += chars[type_][random.randint(0, len(chars[type_])-1)]
            used_types[type_] += 1
        if 0 not in used_types:
            ps_is_correct = True

    return password

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            length = int(sys.argv[1])
        except:
            if sys.argv[1] not in exception_words:
                print(f"pass-gen: {sys.argv[1]} is not a pass-gen command. Check «pass-gen --help».")
                sys.exit()
            else:
                print("pass-gen: Choose the length of the password.")
                sys.exit()
        password = pass_gen(int(sys.argv[1]))
        pyperclip.copy(password)
        print(password)
    else:
        print("pass-gen: Choose the length of the password.")