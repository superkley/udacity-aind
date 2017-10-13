import numpy as np

def sinusoid(freq):
    """
    return a sinusoidal of random amplitude and phase for a given frequency
    :param freq: 
    :return: 
    """
    phase = np.random.random()
    amplitude = 2 * (np.random.random_integers(1, 10))
    return amplitude * np.cos(2 * np.pi * freq - phase)


def get_wave_timing(num_samples=500, range_of_time = 5.0):
    """
    provide an array of time values of size num_samples spread evenly over range_of_time
    :param num_samples: int 
    :param range_of_time: float
    :return: int, float, np.array
    """
    # sample spacing
    spacing = range_of_time / num_samples
    # array for time samples
    t = np.linspace(0.0, range_of_time, num_samples)
    return num_samples, spacing, t


def make_waves(t, freqs):
    """
    convert three frequencies into arrays of discrete values representing sinusoidal waves
    :param freqs: [float, float, float]
    :return: [np.array, np.array, np.array]
    """
    w0 = sinusoid(t * freqs[0])
    w1 = sinusoid(t * freqs[1])
    w2 = sinusoid(t * freqs[2])
    return w0, w1, w2

