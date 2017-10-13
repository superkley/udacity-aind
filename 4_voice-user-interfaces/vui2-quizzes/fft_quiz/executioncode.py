import json

import numpy as np
import fft_quiz.function as function
import scipy.fftpack

import fft_quiz.utils as utils

result = {'is_correct': False,
          'error': False,
          'values': [],
          'output': ''}

try:
    # test choose_frequencies()
    num_samples, spacing, t = utils.get_wave_timing()
    freqs = function.choose_frequencies()
    assert None not in freqs, 'choose_frequencies ERROR: Please replace the "None" values with values from 1 to 50.'
    assert len(freqs) == 3 and max(freqs) <= 50 and min(
        freqs) >= 1

    # test add_the_waves
    waves = function.add_the_waves(freqs)
    assert waves[3] is not None
    testsum = waves[0] + waves[1] + waves[2]
    assert len(waves) == 4 and len(waves[3]) == num_samples and np.allclose(waves[3], testsum)

    # test demo_fft
    xf, yf = function.demo_fft(waves[-1])
    assert yf is not None
    testyf = scipy.fftpack.fft(waves[-1])
    assert np.allclose(yf, testyf)
    result['is_correct'] = True

except Exception as err:
    result['feedback'] = 'Oops, looks like you got an error!'
    result['error'] = str(err)

print(json.dumps(result))