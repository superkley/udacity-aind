import ngram_quiz_3.utils as utils

test_sentences = [
    'the old man spoke to me',
    'me to spoke man old the',
    'old man me old man me',
]

def sample_run():
    # sample usage by test code (this definition not actually run for the quiz)
    bigram_log_dict = utils.bigram_add1_logs('transcripts.txt')
    for sentence in test_sentences:
        print('*** "{}"'.format(sentence))
        print(log_prob_of_sentence(sentence, bigram_log_dict))

def log_prob_of_sentence(sentence, bigram_log_dict):
    total_log_prob = 0.

    # TODO implement
    # get the sentence bigrams with utils.sentence_to_bigrams
    # look up the bigrams from the sentence in the bigram_log_dict
    # add all the the log probabilities together
    # if a word doesn't exist, be sure to use the value of the '<unk>' lookup instead

    return total_log_prob


if __name__ == '__main__':
    sample_run()
