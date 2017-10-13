import json
import numpy as np
import ngram_quiz_2.function as function
import ngram_quiz_2.utils as utils
from collections import Counter


result = {'is_correct': False,
          'error': False,
          'values': [],
          'output': ''}

test_transcript = 'sam i am i am sam'
try:
    # test function.bigram_mle() function
    tokens, bigrams = utils.sentence_to_bigrams(test_transcript)
    result_dict = function.bigram_mle(tokens, bigrams)
    # correct result
    bg_mle_dict = {}
    bg_mle_dict['<unk>'] = 0.
    token_raw_counts = Counter(tokens)
    bigram_raw_counts = Counter(bigrams)
    for bg in bigram_raw_counts:
        bg_mle_dict[bg] = bigram_raw_counts[bg] / token_raw_counts[bg[0]]

    for b in bg_mle_dict:
        assert np.allclose(bg_mle_dict[b], result_dict[b])
    result['is_correct'] = True

except Exception as err:
    result['feedback'] = 'Oops, looks like you got an error!'
    result['error'] = str(err)

print(json.dumps(result))