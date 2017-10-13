from python_speech_features import mfcc
import scipy.io.wavfile as wav


def wav_to_mfcc(wav_filename, num_cepstrum):
    """ extract MFCC features from a wav file
    
    :param wav_filename: filename with .wav format
    :param num_cepstrum: number of cepstrum to return
    :return: MFCC features for wav file
    """
    (rate, sig) = wav.read(wav_filename)
    mfcc_features = mfcc(sig, rate, numcep=num_cepstrum)
    return mfcc_features


if __name__ == '__main__':
    import mfcc_quiz.dutils
    (rate, raw_sig) = wav.read('sample02.wav')
    mfcc_quiz.dutils.plot_raw_audio(raw_sig)
    mfcc_sig = wav_to_mfcc('sample02.wav', 13)
    mfcc_quiz.dutils.plot_mfcc_feature(mfcc_sig)


