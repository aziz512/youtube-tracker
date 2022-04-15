import os
import unittest
from app.watchlist import create_if_not_exist

def test_watchlist(watchlist):
	correct_list = [
		'UCBR8-60-B28hp2BmDPdntcQ',
		'UCsBjURrPoezykLs9EqgamOA',
		'UCYO_jab_esuFRV4b17AJtAw',
	]
	assert correct_list == list(map(lambda x: x['id'], watchlist))

def test_create_if_not_exist():
	path = 'tests/testdir/watchlist'
	if os.path.exists(path):
		if os.path.isdir(path):
			os.rmdir(path)
		else:
			os.remove(path)
	create_if_not_exist(path)
	assert os.path.exists(path)
	os.remove(path)
	os.mkdir(path)
	try:
		create_if_not_exist(path)
	except Exception as e:
		assert isinstance(e, IsADirectoryError)
	os.rmdir(path)

def test_borked_watchlist(borked_watchlist):
	# only one valid entry
	assert borked_watchlist.channels == [
		{
			'name': 'Fireship',
			'id': 'UCsBjURrPoezykLs9EqgamOA',
			'source': 'youtube',
			'site': 'www.youtube.com',
		}
	]
