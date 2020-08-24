import io
import sys
import traceback

from .BaseTest import BaseTest
from .TestResponse import TestResponse
from autograder.printing import StatusMessage
from autograder.io_utils import RedirectStdin

class ArgTest(BaseTest):
    def __init__(self,
                 student_obj=None,
                 solution_obj=None,
                 args=(),
                 kwargs={},
                 start_msg=None,
                 *pos_args,
                 **key_args):
        """
        Initializes the BaseTest object which compares the student object to
        the solution object.

        Arguments
        ---------
        args (tuple) -- The positional arguments to supply to the function when 
            tested.
        kwargs (dict) -- The keyword arguments to supply to the function when
            tested.
        start_msg (str or None) -- The message to print at the beginning of the 
            test.
        """
        super().__init__(student_obj, solution_obj, start_msg,
                         *pos_args, **key_args)

        self.args = args
        self.kwargs = kwargs

        # Optionally overwrite the start message with the filled out arguments
        if start_msg is None:
            self.start_msg = f"Testing {self._serialize_args()}..."
            self.start_msg = "{:68}".format(self.start_msg)


    def _serialize_args(self):
        """
        Builds a string representing the function call.
        """
        student_obj_name = self.student_obj.__name__
        
        args_lst = [repr(arg) for arg in self.args]
        kwargs_lst = [f'{k}={repr(v)}' for k, v in self.kwargs.items()]
        all_args = args_lst + kwargs_lst

        output = f"{student_obj_name}({', '.join(all_args)})"

        if len(output) > 57:
            output = f"{student_obj_name}(...several arguments...)"

        return output


    @staticmethod
    def _captured_runner(fn, args, kwargs, name,
                         f_stdout=None, f_stderr=None, f_stdin=None):
        """
        Runs fn with args, kwargs and loads responses into a TestResponse object
        with name.

        Keyword Arguments
        -----------------
        f_stdout, f_stderr, f_stdin (buffer or None) -- The buffer to read/write
            the captured data from/to.
        """
        # Store old buffers
        __old_stdout = sys.stdout
        __old_stderr = sys.stderr
        __old_stdin = sys.stdin

        # Create new buffers
        f_stdout = f_stdout or io.StringIO()
        f_stderr = f_stderr or io.StringIO()
        f_stdin = f_stdin or RedirectStdin()

        # Replace buffers
        sys.stdout = f_stdout
        sys.stderr = f_stderr
        sys.stdin = f_stdin

        # Build TestRunner arguments
        output = None
        error = None
        warning = None

        # Test the function
        try:
            output = fn(*args, **kwargs)

        except Exception as e:
            # Function raised an exception
            error = f"Threw {e}.\n{traceback.format_exc()}"

        except SystemExit:
            # Function called exit() or quit()
            warning = 'The code tried to exit the Python process.'

        finally:
            # Restore the old buffers
            sys.stdout = __old_stdout
            sys.stderr = __old_stderr
            sys.stdin = __old_stdin

        # If there was an uncaught exception above, the below code will not run
        stdout = f_stdout.getvalue()
        stderr = f_stderr.getvalue()

        return TestResponse(output, stdout, stderr, name, error, warning)


    def run(self):
        """
        Runs the argument test (captures stdout and stderr and runs both of the
        functions).
        """
        self._setup()

        self.solution_response = self._captured_runner(
            self.solution_obj, self.args, self.kwargs, 'solution'
        )

        self.student_response = self._captured_runner(
            self.student_obj, self.args, self.kwargs, 'student'
        )

        return self._process_responses()