import getopt
import os
import re
import sys

import unittest


def discover_tests(package="src"):
    """Find all files containing at least one Test Case class.

    This function is a recursive version of the original discover_tests function.
    It is more flexible and allows for more complex package structures.

    Args:
        package (str): The package name where to search for test files.

    Returns:
        list: A list of test files.
    """

    def walk_folder(root, package_directory=None):
        test_files = []

        # ----> Directory
        if os.path.isdir(root):
            if os.path.basename(root) == "__pycache__":
                return []

            if not "__init__.py" in os.listdir(root):
                return []

            elif package_directory is None:
                print("Detected package: %s" % root)
                package_directory = root

            for entry in os.listdir(root):
                test_files.extend(
                    walk_folder(os.path.join(root, entry), package_directory)
                )

        # ----> File
        elif os.path.isfile(root):
            if not root.endswith(".py"):
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

    return walk_folder(package)


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


def discovery(verbosity=1):
    package_path = detect_package_folder("./src/polyfills")
    print("Project folder is '%s'" % package_path)

    test_files = discover_tests("./src/polyfills")

    print("Found %d test files:" % len(test_files))
    print("\n".join(["- " + file for file in test_files]) + "\n")

    # Add the package path to the PYTHONPATH so that tests can import the package
    sys.path.append(os.path.dirname(package_path))

    # Run the tests
    suite = unittest.TestLoader().loadTestsFromNames(test_files)
    test_result = unittest.TextTestRunner(verbosity=verbosity).run(suite)

    return test_result.wasSuccessful()


# Command line interface
if __name__ == "__main__":
    tests_verbosity = 1

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvq",
            ["help", "verbose", "quiet"],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage: run_tests.py [-h] [-v] [-q]")
            sys.exit()

        elif opt in ("-v", "--verbose"):
            tests_verbosity = 2

        elif opt in ("-q", "--quiet"):
            tests_verbosity = 0

    sys.exit(not discovery(verbosity=tests_verbosity))
