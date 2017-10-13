# if there is a link it behaves as before, but
# if there is no link tag in the input string,
# it returns None, 0.

# Note that None is not a string and so should
# not be enclosed in quotes.

# Also note that your answer will appear in
# parentheses if you print it.

def get_next_target(page):
    start_link = page.find('<a href=')

    # if the link tag sequence is not found, find returns a -1
    if start_link == -1:
        # return the error codes of None, 0 now and skip the rest!
        return None, 0

    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


if __name__ == '__main__':
    tests = [
        'Not "valid" at all!',
        'Here is a <a href="https://udacity.com">valid link</a>'
    ]

    for i, test in enumerate(tests):
        print("Test {}: {}".format(i, test))
        url, enpos = get_next_target(test)
        print('returned values were {}'.format((url, enpos)))

