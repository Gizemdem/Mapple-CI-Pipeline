import httpimport
from error import InputException
from typing import Callable
from inspect import getmembers, isfunction
import re


def get_funcs_from_url(url: str) -> [Callable]:
    """
    Gets a list of spec functions by importing the module at the 
        url via httpimport

    Args:
        url: Must be a Github Gist url which doesn't end in /filename.py

    Returns:
        [Callable] List of Functions

    """
    # TODO: Support more types of urls
    if not is_github_gist(url):
        raise InputException("Url is not a Github Gist")

    url = prepare_url(url)

    with httpimport.remote_repo(url):
        import specs

    funcs = [func[1] for func in getmembers(specs, isfunction)]
    return funcs


def is_github_gist(url: str) -> bool:
    """
    Checks if a passed string is a github gist

    Args:
        url: a url to check

    Returns: True if url is a github Gist
    """
    pattern = re.compile(
        r"^https:\/\/gist\.githubusercontent\.com\/"
    )
    # Check if the URL matches the pattern
    return bool(pattern.match(url))


def prepare_url(url: str) -> str:
    """
    Removes 'filename.py' at the end of the github gist url if any

    Args:
        url: a github gist url

    Returns: the clean url
    """
    if url.endswith(".py"):
        remove_from_index = url.rfind("/")
        url = url[:remove_from_index]
    return url
