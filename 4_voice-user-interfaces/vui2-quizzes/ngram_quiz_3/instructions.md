## Smoothing and logs

There are still a couple of problems to sort out before we use the bigram probability dictionary to calculate the probabilities of new sentences:

###### 1. Some possible combinations may not exist in our probability dictionary but are still possible.  We don't want to multiply in a probability of 0 just because our original corpus was deficient. This is solved through "smoothing".  There are a number of methods for this, but a simple one is the [Laplace smoothing](https://en.wikipedia.org/wiki/Additive_smoothing) with the "add-one" estimate where <span class="mathquill">V</span> is the size of the vocabulary for the corpus, i.e. the number of unique tokens:

`P_{add1}(w_i|w_{i-1})=\frac{c(w_{i-1},w_i)+1}{c(w_{i-1})+V}`

###### 2. Repeated multiplications of small probabilities can cause underflow problems in computers when the values become to small.  To solve this, we will calculate all probabilities in log space.  Multiplying probabilities in the log space has the added advantage that the logs can be added:

`<span class="mathquill">\qquad \qquad \qquad log(p_1\times p_2\times p_3\times p_4) = \log p_1 + \log p_2 + \log p_3 + \log p_4 </span>`

## Quiz 3 Instructions
In the following quiz, a utility named `utils.bigram_add1_logs` has been added for you with Laplace smoothing in the log space. Write a function that calculates the log probability for a given sentence, using this log probability dictionary.  If all goes well, you *should* observe that more likely sentences yield higher values for the log probabilities.
