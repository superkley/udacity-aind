def bigrams_from_transcript(filename):
    """
    read a file of sentences, adding start '<s>' and stop '</s>' tags; Tokenize it into a list of lower case words
    and bigrams
    :param filename: string 
        filename: path to a text file consisting of lines of non-puncuated text; assume one sentence per line
    :return: list, list
        tokens: ordered list of words found in the file
        bigrams: a list of ordered two-word tuples found in the file
    """
    tokens = []
    bigrams = []
    with open(filename, 'r') as f:
        for line in f:
            line_tokens, line_bigrams = sentence_to_bigrams(line)
            tokens = tokens + line_tokens
            bigrams = bigrams + line_bigrams
    return tokens, bigrams


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