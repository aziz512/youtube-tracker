def test_watchlist(watchlist):
	correct_list = [
		'UCBR8-60-B28hp2BmDPdntcQ',
		'UCsBjURrPoezykLs9EqgamOA',
		'UCYO_jab_esuFRV4b17AJtAw',
	]
	assert correct_list == list(watchlist)
