import json
import ngram_quiz_1.function as function


result = {'is_correct': False,
          'error': False,
          'values': [],
          'output': ''}

try:
    # test sentence_to_bigrams() function
    sentence = 'the old man spoke to me'
    t, b = function.sentence_to_bigrams(sentence)
    sentence_tokens = ['<s>'] + sentence.lower().split() + ['</s>']
    sentence_bigrams = []
    for i in range(len(sentence_tokens) - 1):
        sentence_bigrams.append((sentence_tokens[i], sentence_tokens[i + 1]))
    assert t == sentence_tokens
    assert b == sentence_bigrams
    result['is_correct'] = True

except Exception as err:
    result['feedback'] = 'Oops, looks like you got an error!'
    result['error'] = str(err)

print(json.dumps(result))