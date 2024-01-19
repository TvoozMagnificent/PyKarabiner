
file = "/Users/luchang/Desktop/pythonprojects/PyKarabiner/PyKarabiner/words.txt"

def abbreviate(string):
    vowels = 'aeiou'
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    string = string.lower()
    string = string[0] + "".join([i for i in string[1:] if i not in vowels])
    for _ in alphabet:
        if _*2 in string: string = string.replace(_*2, _)
    return string

abbreviations = {}

for word in open(file).readlines():
    word = word.strip()
    _ = abbreviate(word)
    if _ not in abbreviations: abbreviations[_] = []
    abbreviations[_].append(word)

while True:
    _ = input('>>> ').strip()
    if _ in abbreviations: print(', '.join(abbreviations[_]))
    else: print('Not Found')
