import pandas as pd

word_bank = pd.read_csv('../input/AllThoughtWords.csv')
max_length = 0
for word in word_bank['Word']:
    if len(word) > max_length:
        max_length = len(word)


df = pd.read_csv('../input/AllThoughtWords.csv')

asciis = []

for i in range(len(df['Word'])):
    word = df['Word'][i]
    length = len(word)
    word_ascii = [ord(char) for char in word]
    for i in range(length, max_length):
        word_ascii.append(32)
    asciis.append(word_ascii)
output = pd.DataFrame(asciis)
output = pd.concat((output, df['Class']), axis=1)
output.to_csv('asciiThought.csv')
