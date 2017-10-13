from python_speech_features import mfcc
import scipy.io.wavfile as wav


def wav_to_mfcc(wav_filename, num_cepstrum):
    """ extract MFCC features from a wav file

    :param wav_filename: filename with .wav format
    :param num_cepstrum: number of cepstrum to return
    :return: MFCC features for wav file
    """

    # TODO implement
    raise NotImplementedError


if __name__ == '__main__':
    import mfcc_quiz.dutils
    mfcc_sig = wav_to_mfcc('nd889_audio/sample02.wav', 13)
    (rate, raw_sig) = wav.read('nd889_audio/sample02.wav')
    mfcc_quiz.dutils.plot_raw_audio(raw_sig)
    mfcc_quiz.dutils.plot_mfcc_feature(mfcc_sig)


