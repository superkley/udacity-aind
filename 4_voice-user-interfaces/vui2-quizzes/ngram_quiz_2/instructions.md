## Probabilities and Likelihoods with Bigrams

Recall from a previous video that the probability of a series of words
can be calculated from the chained probabilities of its history:

`<span class="mathquill">P(w_1w_2...w_n)=\prod_i P(w_i|w_1w_2...w_{i-1})</span>`

The probabilities of sequence occurrences in a large textual corpus can be calculated this
way and used as a language model to add grammar and contectual knowledge to a speech
recognition system.  However, there is a prohibitively large number of calculations for all the 
possible sequences of varying length in a large textual corpus. 

To address this problem, we use the [Markov Assumption](https://en.wikipedia.org/wiki/Markov_property) to approximate
a sequence probability with a shorter sequence:

`P(w_1w_2...w_n)\approx \prod_i P(w_i|w_{i-k}...w_{i-1})`

We can calculate the probabilities by using **counts** of the bigrams and individual tokens:

`P(w_i|w_{i-1})=\frac{c(w_{i-1},w_i)}{c(w_{i-1})}`

In Python, the  [Counter](https://docs.python.org/3.6/library/collections.html#collections.Counter) method is useful for this task

``` python
from collections import Counter
# Sentence: "I am as I am"
tokens = ['<s>', 'i', 'am', 'as', 'i', 'am', '</s>']
token_counts = Counter(tokens)
print(token_counts)
# output:
# Counter({'</s>': 1, '<s>': 1, 'am': 2, 'as': 1, 'i': 2})
```


## Quiz 2 Instructions

In the quiz below, write a function that returns a probability dictionary when given a lists of tokens and bigrams.
