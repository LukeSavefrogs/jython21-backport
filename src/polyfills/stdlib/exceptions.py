""" Polyfill for newer Exception types that are not available in Python 2.1. """

# Introduced in Python 2.2
class NotImplementedError(RuntimeError):
	"""Method or function hasn't been implemented yet."""
	def __init__(self, message=None):
		RuntimeError.__init__(message or "Method or function hasn't been implemented yet.")