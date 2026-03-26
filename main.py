import random
import string

chars = [string.digits, string.ascii_uppercase, string.ascii_lowercase, string.punctuation]


exit_words = ["q", "quit", "exit", "-", ""]

while True:
    try:
        lenght = (input("Введите длинну: "))

        if lenght in exit_words:
            break

        lenght = int(lenght)

    except:
        print("Неправильный ввод!!!")
        continue

    ps_is_correct = False

    while not ps_is_correct:

        used_types = [0, 0, 0, 0]

        pswd = ""

        for n in range(lenght):
            Type = random.randint(0, len(chars)-1)
            pswd += chars[Type][random.randint(0, len(chars[Type])-1)]
            used_types[Type] += 1
        if 0 not in used_types:
            ps_is_correct = True

    print(pswd)