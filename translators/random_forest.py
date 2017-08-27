print('importing libraries')

import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier

WORD = 'thought.pkl'

print('Reading input')
X = pd.read_csv('../input/asciiThought.csv')
X.sample(frac=1)
y = X.pop('Class')

word_bank = pd.read_csv('../input/AllThoughtWords.csv')
max_length = 0
for word in word_bank['Word']:
    if len(word) > max_length:
        max_length = len(word)

print('fitting model')
model = RandomForestClassifier(n_estimators=20, verbose=0)
model.fit(X, y)

print('Model accuracy:', model.score(X, y))

print('Saving model state')
joblib.dump(model, WORD)

