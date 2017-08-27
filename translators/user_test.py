from sklearn.externals import joblib
import pandas as pd
import numpy as np

word_bank = pd.read_csv('../input/allActuallyWords.csv')
max_length = 0
for word in word_bank['Word']:
    if len(word) > max_length:
        max_length = len(word)


file_name = '../pretrained models/dont.pkl'

model = joblib.load(filename=file_name)

print('Enter words (e for exit):')
user_test = input()
while not user_test == 'e':
    ascii_input = [ord(x) for x in user_test]
    while len(ascii_input) < max_length:
        ascii_input.append(32)

    prediction = model.predict(np.array(ascii_input).T.reshape(1, -1))
    # if prediction == 0:
    #     print('you')
    # elif prediction == 1:
    #     print('your')
    # else:
    #     print('not you or your')
    # if prediction == 0:
    #     print('actually')
    # else:
    #     print('not actually')
    if prediction == 0:
        print('don\'t')
    else:
        print('not don\'t')
    user_test = input()
