# CS 41 Autograder

![Language](https://img.shields.io/github/languages/top/stanfordpython/autograder)
![Issues](https://img.shields.io/github/issues/stanfordpython/autograder)
![PyPi Version](https://img.shields.io/pypi/v/sp-autograder)
![MIT License](https://img.shields.io/github/license/stanfordpython/autograder)

CS 41: Hap.py Code is a course at Stanford about the Python programming language. This autograder, implemented entirely in Python allows the user to run student code, run solution code, and compare the output of the two. The autograder allows the user to implement several tests which can be executed concurrently and allows the user to hook into the module and provide logic to post-process the results of the tests.

<p align="center">
  <img height="400" alt="A terminal screen with text that appears from running the CS 41 autograder." src="https://i.ibb.co/W3mxdzD/autograder-img.png" /><br />
  <i>A sample run of the CS 41 autograder.</i>
</p>

## Getting off the Ground
Here are steps to getting off the ground with this autograder:
1. *Instantiate `autograder.Autograder`*. Create an object that inherits from `autograder.Autograder` like `class TestAutograder(Autograder):`.
2. *Initialize the parent instance*. I tend to do this inside the `__init__` method of my subclass with `super().__init__`. The only required argument to that function is the name of the student module, provided as a string `module_name`. If you'd like to add to the autograder, specify `has_custom_tests=True`.
3. *Write `run_custom_tests`*. Override the `run_custom_tests(self)` function and add any custom tests. When that function is executed, `self.module` will contain the student module object.

### Tests
The autograder module has numerous tests which inherit from each other in a linear hierarchy.
* `BaseTest`: The `BaseTest` must be provided the `student_obj` and the `solution_obj`. It simply compares the two objects and passes if they are the same and fails otherwise.
* `ArgTest`: `ArgTest` can additionally be provided with `args` and `kwargs`. The autograder runs the functions in a sandboxed environment and compares their return values, output, and any errors they threw.
* `IOTest`: The `IOTest` allows the autograder to overwrite `sys.stdin` and provide input to the student and solution programs when they call `input`. The text inputs should be provided as `in_params`.
* `FileIOTest`: A `FileIOTest` is provided a `filename` and generates an `IOTest` from the contents of that file.

### The Test Suite
`autograder.testsuite` contains a class called `TestSuite`. This class allows the user to add several tests to the autograder, run them concurrently, and tabulate the results. You can enable concurrency by passing `multiprocess=True` to the constructor of the `TestSuite`. You can also hook into the test suite using a machine learning algorithm by passing in a function as the argument `ml`. After all tests have finished, `ml` will be called with a list of ones and zeros where the `i`th entry corresponds to the `i`th test (one indicates that the student passed the test and zero indicates that the student failed).

## Advanced Features
### Module Overrides
The autograder supports a `module_overrides` argument that should be a dictionary mapping strings to objects. The autograder will override the associated mappings at the module level within the student file.

### Setup and Cleanup
Each test supports a `setup_fn` and a `cleanup_fn` that will be called before and after the test runs, respectively. These functions can be used to modify the filesystem and inputs or otherwise clean up before and after the test runs

### Progressive Diff
If the autograder is called with a `--progressive` or `-p` flag at the command line, it will stop when it hits the first output error in each program. It will prompt the grader to enter either PRIOR, SUBSEQ, or BOTH which will display the prior lines, subsequent lines, or display the entire diff, respectively.

## Known Issues
### Multiprocessing Issues
Module overrides and the progressive diff features do not work in multiprocessing mode. The progressive diff feature cannot be repaired because the OS restricts access to `sys.stdin` so the autograder can't ask the grader for input. It is possible to repair the issue with module overrides, but that will require significant refactoring.
