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
    # get the sentence bigrams
    s_tokens, s_bigrams = utils.sentence_to_bigrams(sentence)

    # add the log probabilites of the bigrams in the sentence
    total_log_prob = 0.
    for bg in s_bigrams:
        if bg in bigram_log_dict:
            total_log_prob = total_log_prob + bigram_log_dict[bg]
        else:
            total_log_prob = total_log_prob + bigram_log_dict['<unk>']
    return total_log_prob


if __name__ == '__main__':
    sample_run()
