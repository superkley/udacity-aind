import json
import numpy as np
import ngram_quiz_3.function as function
import ngram_quiz_3.utils as utils
from collections import Counter


result = {'is_correct': False,
          'error': False,
          'values': [],
          'output': ''}

test_sentence = 'the old man spoke to me'
try:
    bigram_log_dict = utils.bigram_add1_logs('transcripts.txt')
    # test function.log_prob_of_sentence()
    test_result = function.log_prob_of_sentence(test_sentence, bigram_log_dict)
    # correct result
    s_tokens, s_bigrams = utils.sentence_to_bigrams(test_sentence)
    total_log_prob = 0.
    for bg in s_bigrams:
        if bg in bigram_log_dict:
            total_log_prob = total_log_prob + bigram_log_dict[bg]
        else:
            total_log_prob = total_log_prob + bigram_log_dict['<unk>']

    assert np.allclose(test_result, total_log_prob)
    result['is_correct'] = True

except Exception as err:
    result['feedback'] = 'Oops, looks like you got an error!'
    result['error'] = str(err)

print(json.dumps(result))