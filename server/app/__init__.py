from flask import Flask
from flask_cors import CORS
from . import watchlist
from . import routes

def create_app(rss_watchlist=None):
	app = Flask(__name__)
	CORS(app, origins='http://localhost:*')

	# rss_watchlist is a path to a file
	if rss_watchlist is None: # pragma: no cover
		app.config['watchlist'] = 'watchlist.ini'
	else:
		app.config['watchlist'] = rss_watchlist
	watchlist.Watchlist.create_if_not_exist(app.config['watchlist'])

	routes.add_routes(app)
	return app
