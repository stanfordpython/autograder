__version__ = '0.2.1'
__author__ = 'Parth Sarin'
__license__ = 'MIT'

import py_compile
import pycodestyle
import contextlib
import io

from .printing import StatusMessage, HeaderMessage, SuperHeaderMessage

class Autograder:
    """
    The basic autograder class.
    """

    def __init__(self,
                 module_name=None,
                 module_overrides={},
                 has_compile_check=True,
                 has_custom_tests=False,
                 has_style_tests=True):
        """
        Initializes the autograder.

        Arguments
        ---------
        module_name (str or None) -- The name of the student module.
        module_overrides (dict) -- Namespace overrides for the module.
        has_compile_check (bool) -- Whether to run a basic compile check.
        has_custom_tests (bool) -- Whether the autograder has a functioning
            run_custom_tests function.
        has_style_tests (bool) -- Whether to run PEP8 style checking on the
            module.
        """
        self.module_name = module_name
        if module_name.endswith('.py'):
            self.module_name = self.module_name[:-3]
        self.module_overrides = module_overrides

        self.has_compile_check = has_compile_check
        self.has_custom_tests = has_custom_tests
        self.has_style_tests = has_style_tests


    def run(self):
        """
        Run the autograder.
        """
        print(SuperHeaderMessage(
            f"Starting Autograder for {self.module_name}...",
            "info"
        ))

        self._load_module()

        # Overwrites on the module
        self.module.__dict__.update(self.module_overrides)

        if self.has_custom_tests:
            print(HeaderMessage(
                "Running custom tests on {}...".format(self.module_name)
            ))
            self.run_custom_tests()

        if self.has_style_tests:
            self.run_style_tests()


    def _load_module(self):
        """
        Loads the module by either checking compile or directly importing,
        based on the preferences given in __init__.
        """
        if self.has_compile_check:
            self.run_compile_check() # will import the module
        else:
            self.module = __import__(self.module_name)

        return self.module


    def run_compile_check(self):
        """
        Checks that the module does not have syntax errors.
        """
        print(HeaderMessage(
            "Checking {} for syntax errors...".format(self.module_name)
        ))

        # Check for syntax errors
        py_compile.compile(self.module_name + '.py')
        print(StatusMessage("No syntax errors found.", "success"))

        # Import module
        self.module = __import__(self.module_name)

        print()

        return True


    def run_custom_tests(self):
        raise NotImplementedError('No functionality tests implemented...')


    def run_style_tests(self):
        """Runs PEP8 compliance checking on student code"""
        print()
        print(HeaderMessage(
            "Checking {} for PEP8 compliance...".format(self.module_name)
        ))

        # Get the PEP8 results quietly
        style = pycodestyle.StyleGuide()

        with contextlib.redirect_stdout(io.StringIO()):
            result = style.check_files([self.module_name + '.py'])

        # Pretty print results
        result._deferred_print.sort()

        if not result._deferred_print:
            print(StatusMessage('No PEP8 violations found!', 'success'))
            return

        num_errors, num_warnings = 0, 0
        for line_number, offset, code, text, doc in result._deferred_print:
            if code[0] == 'E':
                num_errors += 1
            else:
                num_warnings += 1

        # Print out the counts
        err_msg = StatusMessage(
            f'{num_errors} error(s)',
            'fail'
        )

        warning_msg = StatusMessage(
            f'{num_warnings} warning(s)',
            'warning'
        )

        code_cmd = StatusMessage(
            f'$ pycodestyle {self.module_name}.py',
            'bold'
        )

        print(f"{err_msg} and {warning_msg} were found and suppressed.\n"
              f"Run {code_cmd} to see them.")

        print()
