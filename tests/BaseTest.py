import sys
from .TestResponse import TestResponse
from autograder.printing import StatusMessage

def _dummy_setup_cleanup():
    pass

class BaseTest:
    def __init__(self,
                 student_obj=None,
                 solution_obj=None,
                 start_msg=None,
                 setup_fn=_dummy_setup_cleanup,
                 cleanup_fn=_dummy_setup_cleanup):
        """
        Initializes the BaseTest object which compares the student object to
        the solution object.

        Arguments
        ---------
        start_msg (str or None) -- The message to print at the beginning of the 
            test.
        setup_fn (function () -> None) -- The function that will be run before
            the test executes.
        cleanup_fn (function () -> None) -- The function that will be run after
            the test executes.
        """
        self.student_obj = student_obj
        self.solution_obj = solution_obj

        self.start_msg = start_msg
        if not start_msg:
            student_obj_name = student_obj.__name__
            self.start_msg = f'Testing {student_obj_name}...'

        self.start_msg = "{:68}".format(self.start_msg)

        self._setup_fn = setup_fn
        self._cleanup_fn = cleanup_fn


    def _handle_pass(self):
        """
        Prints out that the test passed.
        """
        diff = self.solution_response.diff(self.student_response)
        if diff and self.student_response.warning:
            print(StatusMessage('Warning.....', 'warning'))
            print(diff)
        else:
            print(StatusMessage('Test passed!', 'success'))


    @staticmethod
    def __handle_progressive_diff(diff):
        # Do Michael's progressive printing thing
        # 1. Find the error
        diff_lines = diff.split('\n')
        errors = filter(
            lambda idx_line: idx_line[1][0] == '+' or idx_line[1][0] == '-',
            enumerate(diff_lines)
        ) # does the line start with a + or a -?

        # 2. Print the header lines and capture the first error.
        print(next(errors)[1])
        print(next(errors)[1])
        fe_idx, fe_content = next(errors)

        # 3. Print the first error.
        print(fe_content)

        # 4. Ask up, down, or both
        msg = ("Type PRIOR to show all prior output, SUBSEQ for subsequent" 
               " output, or BOTH for a\nfull diff: ")
        resp = input(msg).upper()

        if resp == 'PRIOR':
            return '\n'.join(diff_lines[:fe_idx+1])
        elif resp == 'SUBSEQ':
            return '\n'.join(diff_lines[fe_idx-1:])
        else:
            return diff


    def _handle_fail(self):
        print(StatusMessage('Test failed!', 'fail'))

        diff = self.solution_response.diff(self.student_response)

        # Check if the progressive flag is set.
        is_progressive = '-p' in sys.argv or '--progressive' in sys.argv
        has_output_diff = self.solution_response.has_output_diff

        if is_progressive and has_output_diff:
            to_print = self.__handle_progressive_diff(diff)
        else:
            to_print = diff
        
        print(to_print)


    def _process_responses(self):
        """
        Processes the two responses and returns whether the test passed or
        failed.
        """
        output = self.solution_response == self.student_response

        if output:
            self._handle_pass()
        else:
            self._handle_fail()

        self._cleanup_fn()
        return output


    def _setup(self):
        """
        Sets up the test by printing the test start message and setting up by
        calling the provided setup function.
        """
        self._setup_fn()
        print(self.start_msg, end='')


    def run(self):
        """
        Runs the base test (just compares the two objects).
        """
        self._setup()

        self.solution_response = TestResponse(
            self.solution_obj, None, None, False, 'solution'
        )

        self.student_response = TestResponse(
            self.student_obj, None, None, False, 'student'
        )

        return self._process_responses()
