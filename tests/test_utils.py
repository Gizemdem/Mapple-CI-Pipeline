from utils import prepare_url, is_github_gist


def test_clean_url():
    url = "https://gist.githubusercontent.com/andrsbtrg/1c6ebcfca23492b2dd899b43817ea88a/raw/4183c73c61816a36f0cfe0fc51ef0e2459aaf253/specs.py"

    fixed_url = "https://gist.githubusercontent.com/andrsbtrg/1c6ebcfca23492b2dd899b43817ea88a/raw/4183c73c61816a36f0cfe0fc51ef0e2459aaf253"

    assert prepare_url(url) == fixed_url

    assert prepare_url(fixed_url) == fixed_url


def test_is_github_gist():
    url = "https://gist.githubusercontent.com/andrsbtrg/1c6ebcfca23492b2dd899b43817ea88a/raw/4183c73c61816a36f0cfe0fc51ef0e2459aaf253/specs.py"

    assert is_github_gist(url) == True

    other_url = "https://gist.githubusercontent.com/operatorequals/ee5049677e7bbc97af2941d1d3f04ace/raw/e55fa867d3fb350f70b2897bb415f410027dd7e4"

    assert is_github_gist(other_url) == True

    assert is_github_gist("https://google.com/") == False
