from flask import Flask
from . import watchlist
from . import routes

def create_app(rss_watchlist=None):
	app = Flask(__name__)

	# rss_watchlist is a path to a file
	if rss_watchlist is None: # pragma: no cover
		app.config['watchlist'] = 'watchlist'
	else:
		app.config['watchlist'] = rss_watchlist
	watchlist.create_if_not_exist(app.config['watchlist'])

	routes.add_routes(app)
	return app
