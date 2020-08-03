import collections
from difflib import unified_diff

from autograder.printing import StatusMessage

BaseTestResponse = collections.namedtuple(
    'TestResponse',
    ('output', 'stdout', 'stderr', 'name', 'error', 'warning'),
    defaults=(None, None)
)

class TestResponse(BaseTestResponse):
    def __init__(self, *args, **kwargs):
        if self.stderr and not self.warning:
            self.warning = self.stderr

        self.has_output_diff = False


    def __eq__(self, other):
        """
        Compares two TestResponse objects. Checks that the return value was the 
        same, the printed output was the same, and there was no difference in
        error throwing.
        """
        if self.error and other.error:
            # Don't care about anything else
            return True

        return (self.output == other.output \
                and self.stdout == other.stdout \
                and bool(self.error) == bool(other.error))


    def diff(self, other, self_name=None, other_name=None):
        """
        Returns a diff between self and another test response object. This is
        intended for comparing the student output to the solution output.

        Arguments
        ---------
        other (TestResponse) -- The test response object to compare to.
        self_name (str or None) -- The title of the current test response 
            object.
        other_name (str or None) -- The title of the other test response object.

        Returns
        -------
        str -- The diff between self and other.
        """
        self_name = self_name or self.name
        other_name = other_name or other.name

        # Case 1: An error occurred during the execution of the code.
        error_occurred = self.error or other.error

        if error_occurred:
            both_errored = self.error and other.error
            if not both_errored:
                # Problem: one raised an error and the other didn't.
                if self.error:
                    header = f"{self_name.title()} threw an unexpected error:"
                    error_line = f"\n{self.error}"
                else:
                    header = f"{other_name.title()} threw an unexpected error:"
                    error_line = f"\n{other.error}"

                return (
                    f"{StatusMessage(header, 'info')}"
                    f"{error_line}"
                )

            return

        # Case 2: Difference in what was printed.
        printing_error = self.stdout != other.stdout

        if printing_error:
            self_output = self.stdout.splitlines(keepends=True)
            other_output = other.stdout.splitlines(keepends=True)
            diff = ''.join(unified_diff(
                self_output, 
                other_output, 
                fromfile=self_name, 
                tofile=other_name
            )).strip()

            self.has_output_diff = True # Michael's thingy

            return (f"{StatusMessage('Difference in printed output:', 'info')}"
                    f"\n"
                    f"{diff}")

        # Case 3: Difference in return value.
        return_error = self.output != other.output

        if return_error:
            return (
                f"{StatusMessage('Difference in value:', 'info')}\n"
                f"{self_name}: {repr(self.output)}\n"
                f"{other_name}: {repr(other.output)}"
            )

        # Case 4: Warning!
        warning = self.warning or other.warning

        if warning:
            both_warned = self.warning and other.warning
            if not both_warned:
                # Problem: one raised a warning.
                if self.error:
                    header = f"{self_name} caused a warning:"
                    warning_line = f"{self.warning}"
                else:
                    header = f"{other_name} caused a warning:"
                    warning_line = f"{other.warning}"

                return (
                    f"{StatusMessage(header, 'warning')} "
                    f"{warning_line}"
                )

        # Otherwise: No issues!