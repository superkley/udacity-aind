from collections import Counter
import ngram_quiz_2.utils as utils


def sample_run():
    # sample usage by test code (this definition not actually run for the quiz)
    tokens, bigrams = utils.bigrams_from_transcript('transcripts.txt')
    bg_dict = bigram_mle(tokens, bigrams)
    print(bg_dict)


def bigram_mle(tokens, bigrams):
    """
    provide a dictionary of probabilities for all bigrams in a corpus of text
    the calculation is based on maximum likelihood estimation and does not include
    any smoothing.  A tag '<unk>' has been added for unknown probabilities.
    :param tokens: list
        tokens: list of all tokens in the corpus
    :param bigrams: list
        bigrams: list of all two word tuples in the corpus
    :return: dict
        bg_mle_dict: a dictionary of bigrams:
            key: tuple of two bigram words, in order OR <unk> key
            value: float probability

    """
    bg_mle_dict = {}
    bg_mle_dict['<unk>'] = 0.
    #TODO implement
    return bg_mle_dict


if __name__ == '__main__':
    sample_run()
