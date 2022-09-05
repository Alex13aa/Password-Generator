import sys
import os
from random import random
from platform import system as sys_plat
import pickle


class Error(Exception):
    def __init__(self, text='Unknown Exception', description=''):
        self.text = text
        if not description:
            self.description = 'Programmer don\'t predict this exception.'
        else:
            self.description = description

    def __str__(self):
        if sys_plat() == 'Linux':
            return '\n\033[41m{}:\033[0;31m\ndetails:\n{}\033[0m'.format(self.text, self.description)
        else:
            return '\n{}:\ndetails:\n{}'.format(self.text, self.description)


class LengthError(Error):
    def __init__(self, text='Bad length value!'):
        Error.__init__(self, text, 'Length should be int and greater than 0.')


class EmptyDictionaryError(Error):

    def __init__(self, text='Dictionary is empty'):
        Error.__init__(self, text, 'In dictionary.dict should be not commented out dictionary of chars for password')


def no_duplicates(main_string, add_string):
    for char in add_string:
        if char not in main_string:
            main_string += char
    return main_string


alphabet = ''
length = 20


def load_dictionary():
    global alphabet
    try:
        with open('dictionary.dict') as dictionary:
            for line in dictionary:
                if line.startswith('#'):
                    continue
                else:
                    alphabet = no_duplicates(alphabet, line.replace('\n', ''))
        if not alphabet:
            raise EmptyDictionaryError
    except (EmptyDictionaryError, FileNotFoundError):
        return 2
    else:
        return 0


def give_options(option_list: list):
    global alphabet
    global length
    if '--help' in option_list:
        i_help(option_list[0])
        return 0
    elif '--auto' in option_list:
        alphabet = no_duplicates(alphabet, alphabet.upper())
        alphabet = no_duplicates(alphabet, alphabet.lower())
        option_list.remove('--auto')

    if '-l' in option_list or '--length' in option_list:
        try:
            length = int(option_list[option_list.index('-l' if '-l' in option_list else '--length') + 1])
            if length <= 0:
                raise LengthError()
            option_list.remove(option_list[option_list.index('-l' if '-l' in option_list else '--length') + 1])
            option_list.remove('-l' if '-l' in option_list else '--length')
        except (LengthError, ValueError, IndexError):
            return 1

    for i in option_list:
        if i.startswith('-'):
            option_list.remove(i)
    if len(option_list) > 1:
        operation_on_file(option_list)
    else:
        save_file()


def open_file(file):
    with open(file, 'rb') as f:
        x = pickle.load(f)
    string = ''
    for char in x[x[0][0]]:
        if str(char).isdigit():
            string += str(char)
        else:
            string += char

    print('file name:', file)
    print('password:', ''.join(string))


def operation_on_file(*files):
    f = list(*files)[1:]
    for file in f:
        try:
            if os.path.isfile(file):
                open_file(file)
            else:
                save_file(file)
        except Exception:
            pass


def save_file(file=str(int(random() * 1_000_000)) + '.bin'):
    while os.path.isfile(file):
        file = str(int(random() * 1_000_000)) + '.bin'

    passwd = [alphabet[int(random() * len(alphabet))] for i in range(length)]
    s_pass = passwd.copy()
    passwd = list(map(lambda x: int(x) if x.isdigit() else x, passwd))
    line = int(random() * 200)
    lorem = [[alphabet[int(random() * len(alphabet))] for i in range(length)] for j in range(198)]
    lorem = list(map(lambda i: list(map(lambda x: int(x) if x.isdigit() else x, i)), lorem))
    text = [[line]] + lorem
    # print(line)
    t = text[line]
    text[line] = passwd
    text.append(t)

    with open(file, 'wb') as f:

        pickle.dump(text, f)
    print('file name:', file)
    print('password:', ''.join(s_pass))


def i_help(name='pass generator'):
    print('Hi, in help for pass_generator', '', '{} [OPTIONS] [FILE]'.format(name),
          'OPTIONS', '\t-l [VALUE]\tSet length for your password, (longer version is --length [VALUE])',
          '\t--auto\t\tYour password will have lower and upper char',
          'FILE\tGive localisation for save or load generated password in binary code',
          '\tif file don\'t life save else load from file and print on display', sep='\n')


def main():
    if sys_plat() == 'Linux':
        print('\033[36mMade by Alex13aa\033[0m')
    else:
        print('Made by Alex13aa')
    err = load_dictionary()
    if not err:
        err = give_options(sys.argv)
    if err:
        if err == 1:
            print(LengthError('Bad length value'))
        elif err == 2:
            print(EmptyDictionaryError())
        i_help(sys.argv[0])


if __name__ == '__main__':
    main()
