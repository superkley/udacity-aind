import json

import mfcc_quiz.function as function

import numpy as np
from python_speech_features import mfcc
import scipy.io.wavfile as wav

result = {'is_correct': False,
          'error': False,
          'values': [],
          'output': ''}

try:
    # test wav_to_mfcc()
    mfcc_features = function.wav_to_mfcc('sample02.wav', 13)
    assert mfcc_features is not None, 'mfcc_features ERROR: returned None'
    (rate, sig) = wav.read('sample02.wav')
    correct_mf = mfcc(sig, rate, numcep=13)
    assert np.allclose(mfcc_features, correct_mf), 'unexpected values for mfcc features'
    result['is_correct'] = True

except Exception as err:
    result['feedback'] = 'Oops, looks like you got an error!'
    result['error'] = str(err)

print(json.dumps(result))