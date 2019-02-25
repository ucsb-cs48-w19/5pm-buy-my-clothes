import pytest

from app import user_password
   
def test_user_password1():
   assert user_password("user") == "pass"
   
