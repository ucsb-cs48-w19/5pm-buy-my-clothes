import pytest

from app import parse_filename
   
def test_parse_filename1():
	assert parse_filename("image.png") == ('image', 'png')

def test_parse_filename2():
	assert parse_filename("image.jpg") == ('image', 'jpg')

def test_parse_filename3():
	assert parse_filename("image.gif") == ('image', 'gif')

def test_parse_filename4():
	assert parse_filename("image.jpeg") == ('image', 'jpeg')

def test_parse_filename5():
	assert parse_filename("image.exe") == ('None', 'None')
