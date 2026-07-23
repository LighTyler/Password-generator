#! /home/ilya/Projects/Password-generator/.venv/bin/python3
import random
import string
import sys

import pyperclip
import click


@click.command()
@click.option('-l', '--length', default=12, help="Length of generated password")
@click.option('-c', '--copy', is_flag=True, help="Copy generated password to clipboard")
@click.option('-h', '--hide', is_flag=True, help="Hide generated password")
@click.option('-d', '--digits', is_flag=True, help="Digits only")
@click.option('--lowercase', is_flag=True, help="Lowercase letters only")
@click.option('-U', '--uppercase', is_flag=True, help="Uppercase letters only")
@click.option('-s', '--special', is_flag=True, help="Special characters only")
@click.option('-L', '--letters', is_flag=True, help="Letters only")
def pass_gen(length: int, copy: bool, hide: bool, digits: bool, lowercase: bool, uppercase: bool, special: bool, letters: bool):
    ps_is_correct = False
    
    types = {
        string.ascii_lowercase: lowercase,
        string.ascii_uppercase: uppercase,
        string.digits: digits,
        string.punctuation: special,
        string.ascii_letters: letters
    }

    if any(types.values()):
        chars = []
        for key in types:
            if types[key]:
                chars.append(key)
    else:
        chars = [string.digits, string.ascii_uppercase, string.ascii_lowercase, string.punctuation]


    while not ps_is_correct:

        used_types = [0] * len(chars)

        password = ""

        for _ in range(length):
            type_ = random.randint(0, len(chars)-1)
            password += chars[type_][random.randint(0, len(chars[type_])-1)]
            used_types[type_] += 1
        if 0 not in used_types:
            ps_is_correct = True

    if hide:
        click.echo(f"pass-gen:{'*' * length}")
    else:
        click.echo(password)
    
    if copy:
        pyperclip.copy(password)

if __name__ == "__main__":
    pass_gen()
