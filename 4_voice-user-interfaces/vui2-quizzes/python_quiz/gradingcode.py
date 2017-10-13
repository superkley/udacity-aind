"""
Grading Code - The Python code responsible for marking submission correct/incorrect 
    and to provide feedback when a student clicks ‘Submit’. 
    To do this, you need to use the dictionary called 
            executor_result 
    which contains the output of the Execution Code. The executor_result dictionary contains:
            executor_result ['stderr'] - All of the errors messages from trying to run your 
                code/the student's code. This can be kind of confusing to just show the 
                students since it contains what is produced when the VM running the code 
                tries to run your code as well as the student's code.
            executor_result ['stdout'] - The result of any print calls.

    To actually set what the student sees, you need to set the following values in the dictionary grade_result:
            grade_result['correct'] - You can set this to True, False or None. 
                True and False map to the question considered being passed or failed. 
                Setting it to None is good if you have an open ended quiz and don't 
                want to style the feedback as explicitly telling the student they did something right or wrong.
            grade_result['comment'] - This is the comment the student sees. You can use markdown in it. 
                Pretty nifty.
"""
# included in the quiz backend - do not add when pasting to quiz
grade_result = None
executor_result = None
#####
# start of paste to quiz
import json

# This is the stdout from Submit Code.
result = json.loads(executor_result['stdout'])
comment = ""

if result['is_correct']:
    grade_result["correct"] = True
    grade_result["comment"] = 'Nice work!'
elif not result['is_correct']:
    grade_result["correct"] = False
    grade_result["comment"] = "Looks like something is missing in your code. Try again!"
else:
    comment = "Something went wrong with your submission:"
    #grade_result['comment'] = result['error']