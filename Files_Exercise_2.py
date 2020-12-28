import argparse
parser = argparse.ArgumentParser()
parser.add_argument('word', type=str, help='zadej slovo')

args = parser.parse_args()

print(args)

def count_letters(word):
    v=0
    c=0
    for letter in word:
        if letter in 'aeiou':
            v += 1
        else:
            c += 1
    return v, c

print('Počet samohlásek, souhlásek', count_letters(args.word))