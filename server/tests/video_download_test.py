import asyncio
import os
import pytest
from app.video_download import url_to_video_id

url_to_video_id_params = [
	( 'UCBR8-60-B28hp2BmDPdntcQ', 'youtube'  ),
	( 'UCsBjURrPoezykLs9EqgamOA', 'Fireship' ),
	( 'UCYO_jab_esuFRV4b17AJtAw', '3blue1brown' ),
]

@pytest.mark.parametrize('id, name', url_to_video_id_params)
def test_url_to_video_id(id, name):
	urls_fetch = [
		f'https://www.youtube.com/c/{name}',
		f'https://www.youtube.com/c/{name}/featured',
		f'https://www.youtube.com/c/{name}/videos',
	]
	urls_no_fetch = [
		f'https://www.youtube.com/channel/{id}',
		f'https://www.youtube.com/channel/{id}/featured',
		f'https://www.youtube.com/channel/{id}/videos',
	]
	if os.getenv('FETCH_TEST') == 'true':
		for url in urls_fetch:
			assert asyncio.run(url_to_video_id(url)) == id

	for url in urls_no_fetch:
		assert asyncio.run(url_to_video_id(url)) == id

def test_fail_url_to_video_id():
	assert asyncio.run(url_to_video_id('not an url')) is None
