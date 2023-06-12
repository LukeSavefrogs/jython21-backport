"""
Drop-in replacement for the original unittest `discover` feature (which 
is not present in older Python/Jython versions).

Jython's `unittest` also has only `--help`, `--verbose` and `--quiet` CLI options.
This script provides support for the missing ones.

--------------------------------------------------------------------------------------------------------------
python -m unittest -h       
usage: python.exe -m unittest [-h] [-v] [-q] [--locals] [-f] [-c] [-b] [-k TESTNAMEPATTERNS] [tests ...]

positional arguments:
  tests                a list of any number of test modules, classes and test methods.

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbose        Verbose output
  -q, --quiet          Quiet output
  --locals             Show local variables in tracebacks
  -f, --failfast       Stop on first fail or error
  -c, --catch          Catch Ctrl-C and display results so far
  -b, --buffer         Buffer stdout and stderr during tests
  -k TESTNAMEPATTERNS  Only run tests which match the given substring

Examples:
  python.exe -m unittest test_module               - run tests from test_module
  python.exe -m unittest module.TestClass          - run tests from module.TestClass
  python.exe -m unittest module.Class.test_method  - run specified test method
  python.exe -m unittest path/to/test_file.py      - run tests from test_file.py

usage: python.exe -m unittest discover [-h] [-v] [-q] [--locals] [-f] [-c] [-b] [-k TESTNAMEPATTERNS] [-s START]        
                                       [-p PATTERN] [-t TOP]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output
  -q, --quiet           Quiet output
  --locals              Show local variables in tracebacks
  -f, --failfast        Stop on first fail or error
  -c, --catch           Catch Ctrl-C and display results so far
  -b, --buffer          Buffer stdout and stderr during tests
  -k TESTNAMEPATTERNS   Only run tests which match the given substring
  -s START, --start-directory START
                        Directory to start discovery ('.' default)
  -p PATTERN, --pattern PATTERN
                        Pattern to match tests ('test*.py' default)
  -t TOP, --top-level-directory TOP
                        Top level directory of project (defaults to start directory)

For test discovery all test modules must be importable from the top level directory of the project.
--------------------------------------------------------------------------------------------------------------
"""

import getopt
import os
import re
import sys
import traceback

import unittest
import fnmatch

def discover_tests(start_directory="src", file_pattern="test*.py", package_path=None):
    # type: (str, str, str|None) -> list[str]
    """ Find all files containing at least one Test Case class.

    This function is a recursive version of the original discover_tests function.
    It is more flexible and allows for more complex package structures.

    Args:
        start_directory (str): The directory where to search the test files.
        package_path (str): The full path to the package (will be used to format the package name).

    Returns:
        list: A list of test files.
    """
    if package_path is None:
        package_path = detect_package_folder(start_directory)
        print("[AUTO] Project folder is '%s'" % package_path)



    def walk_folder(root, file_pattern, package_directory=None):
        # type: (str, str, str|None) -> list[str]
        """ Traverses a directory and returns a list of all files containing at least one Test Case class.

        Args:
            root (str): Start directory.
            package_directory (str, optional): First package directory found. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            list[str]: A list of test files.
        """
        test_files = []

        # ----> Directory
        if os.path.isdir(root):
            if os.path.basename(root) == "__pycache__":
                return []

            if os.listdir(root) == []:
                return []

            if package_directory is None and "__init__.py" in os.listdir(root):
                print("Detected package: %s" % root)
                package_directory = root

            for entry in os.listdir(root):
                test_files.extend(
                    walk_folder(os.path.join(root, entry), file_pattern, package_directory)
                )

        # ----> File
        elif os.path.isfile(root):
            if not re.match(fnmatch.translate(file_pattern), os.path.basename(root)):
                return []

            # Check if file contains at least one Test Case class
            try:
                try:
                    f = open(root, "r")
                    contents = f.read()
                except:
                    print(
                        "Could not open or read file %s: %s" % (root, sys.exc_info()[1])
                    )
                    return []
            finally:
                try:
                    f.close()
                except:
                    pass

            contains_test_case = re.search(
                "^\s*class (Test.*?|.*?TestCase\s*)\(.*?\.TestCase\)\s*:\s*(#.*)?$",
                contents,
                re.MULTILINE,
            )

            if contains_test_case:
                file_in_package = root[len(package_directory) + 1 :][:-3]
                test_files.append(
                    os.path.basename(package_directory)
                    + "."
                    + file_in_package.replace(os.sep, ".")
                )

        # ----> Unknown
        else:
            raise Exception("Unknown file type: %s" % root)

        return test_files

    return walk_folder(start_directory, file_pattern.strip(), package_path)


def detect_package_folder(current_directory=os.getcwd()):
    """Detect the package name of the current working directory.

    Args:
        current_directory (str): The current working directory.

    Returns:
        str: The path to the package root.
    """
    if current_directory is None:
        current_directory = os.getcwd()
    elif not os.path.isdir(current_directory):
        raise Exception("Not a directory: %s" % current_directory)
    elif not os.path.exists(current_directory):
        raise Exception("Directory does not exist: %s" % current_directory)

    # Traverse upwards until we find the FIRST directory containing an __init__.py file
    previous_directory = None
    while "__init__.py" in os.listdir(current_directory):
        previous_directory = current_directory
        current_directory = os.path.dirname(current_directory)

    if previous_directory is not None:
        return previous_directory

    # Traverse downwards until we find the FIRST directory containing an __init__.py file
    while "__init__.py" not in os.listdir(current_directory):
        children_directories = [
            entry
            for entry in os.listdir(current_directory)
            if os.path.isdir(os.path.join(current_directory, entry))
            and entry != "__pycache__"
        ]

        if len(os.listdir(current_directory)) == 0:
            raise Exception("Could not find package directory")

        elif len(children_directories) > 1:
            if "src" in children_directories:
                current_directory = os.path.join(current_directory, "src")
                continue

            raise Exception("Could not find package directory")

        for directory in children_directories:
            current_directory = os.path.join(current_directory, directory)
            break
    else:
        return current_directory


def discovery(verbosity=1, start_directory="./src/", file_pattern="test*.py"):
    test_files = discover_tests(start_directory, file_pattern=file_pattern)

    print("Found %d test files:" % len(test_files))
    print("\n".join(["- " + file for file in test_files]) + "\n")

    # Add the package path to the PYTHONPATH so that tests can import the package
    sys.path.append(os.path.dirname(detect_package_folder(start_directory)))

    # Run the tests
    suite = unittest.TestLoader().loadTestsFromNames(test_files)
    test_result = unittest.TextTestRunner(verbosity=verbosity).run(suite)

    return test_result.wasSuccessful()


# Command line interface
if __name__ == "__main__":
    tests_verbosity = 1
    tests_start_directory = "./src/"
    tests_file_pattern = "test*.py"

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvqs:p:",
            ["help", "verbose", "quiet", "start-directory=", "pattern="],
        )
    except getopt.GetoptError:
        traceback.print_exc()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage: run_tests.py [-h] [-v] [-q]")
            sys.exit()

        elif opt in ("-v", "--verbose"):
            tests_verbosity = 2

        elif opt in ("-q", "--quiet"):
            tests_verbosity = 0

        elif opt in ("-s", "--start-directory"):
            tests_start_directory = arg
        
        elif opt in ("-p", "--pattern"):
            tests_file_pattern = arg

    sys.exit(
        not discovery(
            verbosity=tests_verbosity,
            start_directory=tests_start_directory,
            file_pattern=tests_file_pattern,
        )
    )
