## Generating N-Grams

An N-Gram is an ordered sequence of words. For example:
![ngram example](../images/ngrams_numbers.png)
In the following series of quizes, you will work with 2-grams, or [bigrams](https://en.wikipedia.org/wiki/Bigram), as they are more commonly called.
The objective is to create a function that calculates the probability that a particular sentence
could occur in a corpus of text, based on the probabilities of its component bigrams.  We'll do this in stages though:
* Quiz 1 - Extract tokens and bigrams from a sentence
* Quiz 2 - Calculate probabilities and log likelihoods for bigrams
* Quiz 3 - Calculate the log likelihood of a given sentence based on a corpus of text using bigrams

#### Assumptions and terminology
We will assume that text data is in the form of sentences with no punctuation.  If a sentence is in a single line, we will add add a token for
start of sentence: `<s>` and end of sentence: `</s>`.  For example, if the sentence is "I love language models." it will appear in code as:

```
'I love language models'
```

The **tokens** for this sentence are represented as an ordered list of the lower case words plus the start and end sentence tags:

```
tokens = ['<s>', 'i', 'love', 'language', 'models', '</s>']
```

The **bigrams** for this sentence are represented as a list of lower case ordered pairs of tokens:

```
bigrams = [('<s>', 'i'), ('i', 'love'), ('love', 'language'), ('language', 'models'), ('models', '</s>')]
```

## Quiz 1 Instructions

In the quiz below, write a function that returns a list of tokens and a list of bigrams for a given sentence.  You will need to first break a sentence into words in a list, then add a `<s>` and `<s/>` token to the
start and end of the list to represent the start and end of the sentence.

Your final lists should be in the format shown above and called out in the function docstring.