#!/usr/bin/env python3
import random
import string
import sys

chars = [string.digits, string.ascii_uppercase, string.ascii_lowercase, string.punctuation]
exit_words = ["q", "quit", "exit", "-", ""]


def pass_gen(length: int) -> str:
    ps_is_correct = False

    while not ps_is_correct:

        used_types = [0, 0, 0, 0]

        pswd = ""

        for n in range(length):
            Type = random.randint(0, len(chars)-1)
            pswd += chars[Type][random.randint(0, len(chars[Type])-1)]
            used_types[Type] += 1
        if 0 not in used_types:
            ps_is_correct = True

    return pswd

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(pass_gen(int(sys.argv[1])))
    else:
        while True:
            try:
                length = (input("Введите длинну: "))

                if length in exit_words:
                    break

                length = int(length)

            except:
                print("Неправильный ввод!!!")
                continue
            
            print(pass_gen(length))
