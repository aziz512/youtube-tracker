from flask import Flask
from . import routes

def create_app(watchlist=None):
	app = Flask(__name__)

	# watchlist is a path to a file
	if watchlist is None:
		app.config['watchlist'] = 'watchlist'
	else:
		app.config['watchlist'] = watchlist

	routes.add_routes(app)
	return app
