## Generating N-Grams

An N-Gram is an ordered sequence of words. For example:
![ngram example](../images/ngrams_numbers.png)
In this quiz, you will work with the 2-grams, or [bigrams](https://en.wikipedia.org/wiki/Bigram) as they are more commonly called.
The objective of the quiz is to create a function that calculates the probability that a particular sentence
could occur in a corpus of text, based on the probabilities of its component bigrams.  For this exercise, we will al so add a token for
start of sentence: `<s>` and end of sentence: `</s>`.

A text corpus with calculated counts has been provided for you.  Your tasks are to:
