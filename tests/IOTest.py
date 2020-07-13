from .ArgTest import ArgTest
from autograder.io_utils import RedirectStdin

class IOTest(ArgTest):
    def __init__(self,
                 student_obj=None,
                 solution_obj=None,
                 in_params=(),
                 *pos_args,
                 **key_args):
        # Initialize the ArgTest
        super().__init__(student_obj, solution_obj, 
                         *pos_args, **key_args)

        # Prepare the stdin buffer
        self.stdin_buffer = RedirectStdin(in_params)


    def run(self):
        """
        Runs the IO test (captures stdout, stderr, provides the given input
        to stdin, and runs both of the functions).
        """
        self._setup()

        # Run solution code and reset the buffer
        self.solution_response = self._captured_runner(
            self.solution_obj, self.args, self.kwargs, 'solution',
            f_stdin=self.stdin_buffer
        )
        self.stdin_buffer.reset_buffer()

        # Run student code and reset the buffer
        self.student_response = self._captured_runner(
            self.student_obj, self.args, self.kwargs, 'student',
            f_stdin=self.stdin_buffer
        )
        self.stdin_buffer.reset_buffer()

        return self._process_responses()