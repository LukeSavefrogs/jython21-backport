import os
import re
import sys

import unittest

def discover_tests(package='src'):
	""" Find all files containing at least one Test Case class. """
	package_directory = None

	test_files = []
	for (root, dirs, files) in os.walk(package):
		if "__pycache__" in root:
			continue

		if not "__init__.py" in files:
			print("Directory %s is not a package" % root)
			continue
		elif package_directory is None:
			package_directory = root
			package_name = os.path.basename(root)


		for file in files:
			if not file.endswith('.py'):
				continue
			
			file_path = os.path.join(root, file)

			# Check if file contains at least one Test Case class
			with open(file_path, 'r') as f:
				contents = f.read()
				contains_test_case = re.search('^\s*class (Test.*?|.*?TestCase\s*)\(.*?\.TestCase\)\s*:\s*(#.*)?$', contents, re.MULTILINE)
				
				if contains_test_case:
					file_in_package = file_path[len(package_directory) + 1:][:-3]
					test_files.append(package_name + "." + file_in_package.replace(os.sep, '.'))

	return test_files


if __name__ == '__main__':
	test_files = discover_tests()

	# Add the package path to the PYTHONPATH
	# package_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
	package_path = "./src/"
	sys.path.append(package_path)

	print("Found %d test files:" % len(test_files))
	print('\n'.join(["- " + file for file in test_files]) + '\n')

	suite = unittest.TestLoader().loadTestsFromNames(test_files)
	test_result = unittest.TextTestRunner(verbosity=2).run(suite)

	sys.exit(not test_result.wasSuccessful())