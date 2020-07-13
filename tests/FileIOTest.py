from .IOTest import IOTest
from autograder.io_utils import RedirectStdin

class FileIOTest(IOTest):
    def __init__(self,
                 filename,
                 student_obj=None,
                 solution_obj=None,
                 args=(),
                 kwargs={},
                 start_msg=None,
                 *pos_args,
                 **key_args):
        """
        Reads the lines from a file for the IOTest.
        """
        self.filename = filename
        
        with open(filename) as f:
            in_params = f.readlines()

        # Replace blank lines with \n
        in_params = [p if p else '\n' for p in in_params]

        # Initialize the IOTest
        super().__init__(student_obj, solution_obj, in_params, args, kwargs, 
                         start_msg, *pos_args, **key_args)


    def _serialize_args(self):
        """
        Builds a string representing the function call.
        """
        student_obj_name = self.student_obj.__name__
        
        args_lst = [repr(arg) for arg in self.args]
        kwargs_lst = [f'{k}={repr(v)}' for k, v in self.kwargs.items()]
        all_args = args_lst + kwargs_lst

        # Arguments and filename
        output = (f"{student_obj_name}({', '.join(all_args)}) "
                  f"(input from {self.filename})")

        # Try suppressing arguments
        if len(output) > 57:
            output = (f"{student_obj_name}(...several arguments...) "
                      f"(input from {self.filename})")

        # Otherwise suppress arguments message
        if len(output) > 57:
            output = f"{student_obj_name}(...) (input from {self.filename})"

        # Finally suppress filename
        if len(output) > 57:
            output = f"{student_obj_name}(...several arguments...)"


        return output