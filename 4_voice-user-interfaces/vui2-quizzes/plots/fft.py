import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack

def example():
    # https: // stackoverflow.com / questions / 25735153 / plotting - a - fast - fourier - transform - in -python
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.fftpack

    # Number of samplepoints
    N = 600
    # sample spacing
    T = 1.0 / 800.0
    x = np.linspace(0.0, N * T, N)
    y = np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x)
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)

    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.show()


def show_three_sinusoids(freq1, freq2, freq3):

    # function to create sinusoid with random phase at given frequenc
    def sinusoid(freq):
        phase = np.random.random()
        amplitude = 2*(np.random.random_integers(1,10))
        return amplitude*np.cos(2*np.pi * freq - phase)


    # Number of sample points
    N = 500
    # sample period
    T = 0.01
    # range max to display
    R = 5.0

    # time plotted on X axis
    t = np.linspace(0.0, R, N)

    # plot three frequencies with random phase shifts on y axis
    plt.figure(1)
    f1 = sinusoid(t*freq1)
    f2 = sinusoid(t*freq2)
    f3 = sinusoid(t*freq3)
    f4 = f1+f2+f3

    plt.subplot(411) #3 rows, 1 column, fignum 1
    plt.plot(t, f1)
    plt.title('1st frequency component')

    plt.subplot(412) #3 rows, 1 column, fignum 2
    plt.plot(t, f2)
    plt.title('2nd frequency component')


    plt.subplot(413) #3 rows, 1 column, fignum 3
    plt.plot(t, f3)
    plt.title('3rd frequency component')


    # sum
    plt.subplot(414) #3 rows, 1 column, fignum 4
    plt.plot(t, f4, 'r')
    plt.title('Sum of components')

    # adjust format of display to make room for titles
    plt.subplots_adjust(
        top=0.94,
        bottom=0.06,
        left=0.09,
        right=0.97,
        hspace=0.65,
        wspace=0.2
        )
    plt.ylabel('amplitude')
    plt.show()
    return f4, T

def splitem(signal, spacing):

    # Number of sample points
    N = np.shape(signal)[0]

    # sample spacing
    T = spacing


    yf = scipy.fftpack.fft(signal)
    # start, stop, number of samples
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)

    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.title('Fast Fourier Transform')
    plt.xlabel('frequency')
    plt.ylabel('amplitude')
    plt.show()


if __name__ == '__main__':


    # pick three frequencies in a range between 0 and 50
    # they will be given random amplitudes and phases
    f1 = 3
    f2 = 8
    f3 = 1

    # add them and display
    frequencies_summed, spacing = show_three_sinusoids(f1, f2, f3)

    # now decompose with FFT
    splitem(frequencies_summed, spacing)