import matplotlib.pyplot as plt
import numpy as np
import fft_quiz.utils as utils
import scipy.fftpack

import fft_quiz.dutils as utils


def choose_frequencies():
    """
    # provide three frequencies in a range between 1 and 50    
    :return: [int, int, int]
    """
    freq1 = 1
    # freq1 = None #test
    freq2 = 3
    freq3 = 9
    return [freq1, freq2, freq3]


def qchoose_frequencies():
    """
    # provide three frequencies in a range between 1 and 50    
    :return: [int, int, int]
    """
    # *** TODO provide three frequencies between 1 and 50
    freq1 = None
    freq2 = None
    freq3 = None
    # end TODO

    return [freq1, freq2, freq3]


def add_the_waves(freqs):
    _, _, t = utils.get_wave_timing()
    w1, w2, w3 = utils.make_waves(t, freqs)
    sum_waves = w1 + w2 + w3
    # sum_waves = None #test
    return [w1, w2, w3, sum_waves]

def qadd_the_waves(freqs):
    """
    create three sinusoidal waves and one wave that is the sum of the three
    :param freqs: [int, int, int]
    :return: [np.array, np.array, np.array, np.array]
        representing wave1, wave2, wave3, sum of waves
        each array contains 500(by default) discrete values for plotting a sinusoidal
    """
    _, _, t = utils.get_wave_timing()
    w1, w2, w3 = utils.make_waves(t, freqs)

    # TODO sum the waves together to form sum_waves
    sum_waves = None
    # end TODO

    return [w1, w2, w3, sum_waves]


def qdemo_fft(sum_waves):
    num_samples, spacing, _ = utils.get_wave_timing()

    # TODO create a Fast Fourier Transform of the waveform using scipy.fftpack.fft
    # named 'y_fft'
    y_fft = None
    # end TODO

    x_fft = np.linspace(0.0, 1.0/spacing, num_samples)
    return x_fft, y_fft


def demo_fft(sum_waves):
    num_samples, spacing, t = utils.get_wave_timing()

    y_fft = scipy.fftpack.fft(sum_waves)
    # y_fft = None  # test
    x_fft = np.linspace(0.0, 1.0/spacing, num_samples)
    return x_fft, y_fft


if __name__ == '__main__':
    num_samples, spacing, t = utils.get_wave_timing()
    waves = add_the_waves(choose_frequencies())
    plt.Figure = dutils.display_sinusoids(t, *waves)
    plt.show()
    xf, yf = demo_fft(waves[-1])
    plt.Figure = dutils.display_fft(xf, yf)
    plt.show()
