import pandas as pd
import numpy as np

df = pd.read_csv('../input/thoughtWords.csv')

new_words = []
word_class = []

# generate permutations
for count in range(len(df['Word'])):
    word = df['Word'][count]
    permuted_word = word
    while len(permuted_word) < 30:
        permuted_word += ' '
    new_words.append(permuted_word)
    word_class.append(df['Class'][count])
    temp_word = ''
    for char in range(len(word)):
        temp_word += word[char]
        permuted_word = temp_word
        for i in range(1, 15):
            for k in range(1,i):
                permuted_word += word[char]
            for j in range(char, len(word)):
                permuted_word += word[j]
            while len(permuted_word) < 30:
                permuted_word += ' '
            new_words.append(permuted_word)
            word_class.append(df['Class'][count])
            permuted_word = temp_word

# Write to csv
output = pd.DataFrame(np.array([word_class, new_words]).T, columns={'Word', 'Class'})
output.to_csv('AllThoughtWords.csv')
