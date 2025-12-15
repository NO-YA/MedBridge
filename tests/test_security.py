import os
import sys
import pytest

# Ensure project root is on sys.path when running tests directly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from medbridge import security


def test_hash_and_verify_short_password():
    pwd = "mysecretpassword"
    hashed = security.hash_password(pwd)
    assert hashed is not None
    assert security.verify_password(pwd, hashed)


def test_hash_and_verify_long_password():
    # bcrypt classic limit is 72 bytes; using bcrypt_sha256 should allow longer inputs
    long_pwd = "p" * 200
    hashed = security.hash_password(long_pwd)
    assert hashed is not None
    assert security.verify_password(long_pwd, hashed)
