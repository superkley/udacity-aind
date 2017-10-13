test_sentences = [
    'the old man spoke to me',
    'me to spoke man old the',
    'old man me old man me',
]

def sentence_to_bigrams(sentence):
    """
    Add start '<s>' and stop '</s>' tags to the sentence and tokenize it into a list
    of lower-case words (sentence_tokens) and bigrams (sentence_bigrams)
    :param sentence: string
    :return: list, list
        sentence_tokens: ordered list of words found in the sentence
        sentence_bigrams: a list of ordered two-word tuples found in the sentence
    """
    sentence_tokens = ['<s>'] + sentence.lower().split() + ['</s>']
    sentence_bigrams = []
    for i in range(len(sentence_tokens)-1):
        sentence_bigrams.append((sentence_tokens[i], sentence_tokens[i+1]))
    return sentence_tokens, sentence_bigrams


if __name__ == '__main__':
    for sentence in test_sentences:
        print('\n*** Sentence: "{}"'.format(sentence))
        t, b = sentence_to_bigrams(sentence)
        print('tokens = {}'.format(t))
        print('bigrams = {}'.format(b))
