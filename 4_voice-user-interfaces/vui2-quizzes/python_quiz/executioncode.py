import json
import python_quiz.function as function


result = {'is_correct': False,
          'error': False,
          'values': [],
          'output': ''}

test_invalid_link = 'Not "valid" at all!'
test_valid_link = 'Here is a <a href="https://udacity.com">valid link</a>'
valid_url = "https://udacity.com"
valid_endpos = 38

try:
    # test get_next_target() correct
    url, enpos = function.get_next_target(test_valid_link)
    assert url == valid_url
    assert enpos == valid_endpos
    url, enpos = function.get_next_target(test_invalid_link)
    assert url is None
    assert enpos == 0
    result['is_correct'] = True

except Exception as err:
    result['feedback'] = 'Oops, looks like you got an error!'
    result['error'] = str(err)

print(json.dumps(result))