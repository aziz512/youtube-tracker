def add_routes(app):
	@app.route('/hello_world')
	def hello_world():
		return 'Hello World!'
