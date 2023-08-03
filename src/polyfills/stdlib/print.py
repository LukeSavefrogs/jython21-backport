import sys as _sys

def print(*args, sep=" ", end="\n", file=None):
    """ Print the given objects to the given file, separated by sep and followed by end.
    
    Args:
        *args: Objects to the printed
        sep (str, optional): Separator between objects. Defaults to " ".
        end (str, optional): End of the print. Defaults to "\n".
        file (file, optional): File to write the output. Defaults to None.
    """
    if file is None:
        file = _sys.stdout

    file.write(sep.join([str(arg) for arg in args]) + end)

if __name__ == "__main__":
    file_handler = _sys.stdout    # open("test.txt", "w+")
    print("Hello world 1!", {"a": 1, "b": 2}, [1, 2, 3], sep=" | ", file=file_handler)
    print("Hello world 2!", {"a": 1, "b": 2}, [1, 2, 3], sep=" | ", file=file_handler)
    print("Hello world 3!", {"a": 1, "b": 2}, [1, 2, 3], sep=" | ", file=file_handler)