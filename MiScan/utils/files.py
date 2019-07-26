from os import makedirs
from os.path import exists, isfile


def exists_or_mkdir(path, verbose=False):
    """Check a folder by given name, if not exist, create the folder and return False,
    if directory exists, return True.
    Parameters
    ----------
    path : str
        A folder path.
    verbose : boolean
        If True (default), prints results.
    Returns
    --------
    boolean
        True if folder already exist, otherwise, returns False and create the folder.
    """
    if not exists(path):
        if verbose:
            print("[*] creates %s ..." % path)
        makedirs(path, exist_ok=True)
        return False
    else:
        if verbose:
            print("[!] %s exists ..." % path)
        return True


def file_exists(filepath):
    """Check whether a file exists by given file path."""
    return isfile(filepath)

