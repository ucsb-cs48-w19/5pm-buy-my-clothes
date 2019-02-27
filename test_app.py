import pytest

from app import parse_filename
   
def test_parse_filename1():
   assert parse_filename("image.png") == "image"
   
