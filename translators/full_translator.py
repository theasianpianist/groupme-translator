from sklearn.externals import joblib
import pandas as pd
import numpy as np

word_bank = pd.read_csv('../input/AllWords.csv')
max_length = 0
for word in word_bank['Word']:
    if len(word) > max_length:
        max_length = len(word)

replace_words = [['you', 'your', 'no replace'], ['actually', 'no replace'], ['don\'t', 'no replace'], ['thought', 'no replace']]

file_names = ['../pretrained models/you.pkl', '../pretrained models/actually.pkl', '../pretrained models/dont.pkl', '../pretrained models/thought.pkl']
models = []
for file in file_names:
    models.append(joblib.load(filename=file))

print('Enter sentence (e for exit):')
user_test = input()
while not user_test == 'e':
    words = user_test.lower().split(' ')
    changed = False
    for i in range(len(words)):
        word = words[i]
        ascii_input = [ord(x) for x in word]
        while len(ascii_input) < max_length:
            ascii_input.append(32)

        for j in range(len(models)):
            model = models[j]
            prediction = model.predict(np.array(ascii_input).T.reshape(1, -1))
            if not replace_words[j][prediction[0]] == 'no replace':
                words[i] = replace_words[j][prediction[0]]
                changed = True
    if changed:
        new_message = ''
        for word in words:
            new_message += word + ' '
    else:
        new_message = user_test
    print(new_message)
    user_test = input()
