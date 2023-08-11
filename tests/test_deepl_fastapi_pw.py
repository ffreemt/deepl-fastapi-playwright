"""Test version."""
from deepl_fastapi_pw import __version__


def test_version():
    """Test sanity."""
    assert __version__[:3] == "0.1"
