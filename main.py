#!./.venv/bin/python
import random
import string
import sys

import pyperclip
import click

chars = [string.digits, string.ascii_uppercase, string.ascii_lowercase, string.punctuation]
exception_words = ["--help", "-h"]


@click.command()
@click.option('-l', '--length', default=12, help="Length of generated password")
@click.option('-c', '--copy', is_flag=True, help="Copy generated password to clipboard")
@click.option('-h', '--hide', is_flag=True, help="Hide generated password")
def pass_gen(length: int, copy: bool, hide: bool):
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

    if hide:
        click.echo(f"pass-gen:{'*' * length}")
    else:
        click.echo(password)
    
    if copy:
        pyperclip.copy(password)

if __name__ == "__main__":
    pass_gen()