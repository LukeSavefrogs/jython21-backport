""" Polyfill for newer Exception types that are not available in Python 2.1. """

# Introduced in Python 2.2
class NotImplementedError(RuntimeError):
	"""Method or function hasn't been implemented yet."""
