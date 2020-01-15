from os import makedirs, remove, getcwd, listdir
from os.path import exists, isfile, join
import re


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


def check_file(path, verbose=True):
    """Check a file by given name, if exist, then delete and return 0,
    else, return 1.
    Parameters
    ----------
    path : str
        A file path.
    verbose : boolean
        If True (default), prints results.
    Returns
    --------
    int
        0 if file already exist and delete the file, otherwise, returns 1.
    """
    if exists(path) and isfile(path):
        remove(path)
        if verbose:
            print("[*] delete original %s ..." % path)
        return 0
    else:
        return 1


def load_file_list(path=None, regx=r'\.csv$', printable=True):
    """Return a file list in a folder by given a path and regular expression.
    Parameters
    ----------
    path : a string or None
        A folder path.
    regx : a string
        The regx of file name.
    printable : boolean, whether to print the files infomation.
    """
    if not path:
        path = getcwd()
    file_list = listdir(path)
    return_list = []
    for f in file_list:
        if re.search(regx, f):
            return_list.append(join(path, f))
    if printable:
        print('Match file example = %s' % (str(return_list[0])))
        print('Number of files = %d in path: %s' % (len(return_list), path))
    return return_list
