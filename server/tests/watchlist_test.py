import os
from app.watchlist import Watchlist

def test_watchlist(watchlist):
	correct_list = [
		'UCBR8-60-B28hp2BmDPdntcQ',
		'UCsBjURrPoezykLs9EqgamOA',
		'UCYO_jab_esuFRV4b17AJtAw',
	]
	assert correct_list == list(map(lambda x: x['id'], watchlist))

def test_create_if_not_exist():
	path = 'tests/testdir/watchlist.ini'
	if os.path.exists(path):
		if os.path.isdir(path):
			os.rmdir(path)
		else:
			os.remove(path)
	Watchlist.create_if_not_exist(path)
	assert os.path.exists(path)
	os.remove(path)
	os.mkdir(path)
	try:
		Watchlist.create_if_not_exist(path)
	except Exception as e:
		assert isinstance(e, IsADirectoryError)
	os.rmdir(path)

def test_borked_watchlist(borked_watchlist):
	# only one valid entry
	print(list(borked_watchlist))
	assert list(borked_watchlist) == [
		{
			'id': 'UCsBjURrPoezykLs9EqgamOA',
			'name': 'Fireship',
			'source': 'youtube',
			'site': 'www.youtube.com',
		}
	]

def test_is_invalid(watchlist, borked_watchlist):
	assert watchlist.is_invalid() is False
	assert borked_watchlist.is_invalid() is True

def test_add_to_watchlist():
	path = 'tests/testdir/test_add_to_watchlist.ini'
	if os.path.exists(path):
		os.remove(path)
	Watchlist.create_if_not_exist(path)
	watchlist = Watchlist(path)

	try:
		watchlist.add_channel()
	except TypeError:
		pass

	try:
		watchlist.add_channel(
			id = 'UCYO_jab_esuFRV4b17AJtAw',
			source = 'non-existant',
		)
	except ValueError:
		pass

	watchlist.add_channel(
		name = '3Blue1Brown',
		id = 'UCYO_jab_esuFRV4b17AJtAw',
	)
	assert list(watchlist)[-1]['source'] == 'youtube'
	assert list(watchlist)[-1]['site'] == 'www.youtube.com'

	watchlist.add_channel(
		name = 'Fireship',
		id = 'UCsBjURrPoezykLs9EqgamOA',
		source = 'Invidious',
	)
	assert list(watchlist)[-1]['source'] == 'invidious'
	assert list(watchlist)[-1]['site'] == 'vid.puffyan.us'

	watchlist.write()

	read_list = Watchlist(path)
	assert list(read_list) == [
		{
			'name': 'Youtube',
			'id': 'UCBR8-60-B28hp2BmDPdntcQ',
			'source': 'youtube',
			'site': 'www.youtube.com',
		},
		{
			'name': '3Blue1Brown',
			'id': 'UCYO_jab_esuFRV4b17AJtAw',
			'source': 'youtube',
			'site': 'www.youtube.com',
		},
		{
			'name': 'Fireship',
			'id': 'UCsBjURrPoezykLs9EqgamOA',
			'source': 'invidious',
			'site': 'vid.puffyan.us',
		},
	]
	os.remove(path)

def test_remove_from_watchlist():
	path = 'tests/testdir/test_remove_from_watchlist.ini'
	if os.path.exists(path):
		os.remove(path)
	Watchlist.create_if_not_exist(path)
	watchlist = Watchlist(path)

	watchlist.add_channel(
		name = '3Blue1Brown',
		id = 'UCYO_jab_esuFRV4b17AJtAw',
	)

	assert watchlist.remove_channel('UCBR8-60-B28hp2BmDPdntcQ')
	assert not watchlist.remove_channel('UCBR8-60-B28hp2BmDPdntcQ')
	assert list(watchlist) == [
		{
			'name': '3Blue1Brown',
			'id': 'UCYO_jab_esuFRV4b17AJtAw',
			'source': 'youtube',
			'site': 'www.youtube.com',
		},
	]

	watchlist.add_channel(
		name = '3Blue1Brown',
		id = 'UCYO_jab_esuFRV4b17AJtAw',
		source = 'invidious',
		site = 'vid.puffyan.us',
	)

	assert watchlist.remove_channel('UCYO_jab_esuFRV4b17AJtAw')
	watchlist.write()
	read_list = Watchlist(path)
	assert list(read_list) == []
	os.remove(path)
