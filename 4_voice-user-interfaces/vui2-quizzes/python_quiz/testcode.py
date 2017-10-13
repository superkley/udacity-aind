# start of this quiz code
import python_quiz.function as function

tests = [
    'Not "valid" at all!',
    'Here is a <a href="https://udacity.com">valid link</a>'
]

for i, test in enumerate(tests):
    print("Test {}: {}".format(i, test))
    url, enpos = function.get_next_target(test)
    print('returned values were {}'.format((url, enpos)))