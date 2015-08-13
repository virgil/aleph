import wolframalpha
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the landing page with zero!'

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/<int:num>')
def page(num):
    # show the post with the given id, the id is an integer
    if num < 0:
    	return "Naturals numbers only!"

    return 'This is the page for the glorious natural number: %d' % num


@app.route('/why')
def why_page():
	return "This page exists because people should stop talking about how big the deep web / dark web is."


@app.route('/wolfram')
def wolfram():

	app_id = 'E7W676-QR2UE4PUR4'
	client = wolframalpha.Client(app_id)
	res = client.query('temperature in Washington, DC on October 3, 2012')

	stuff = []
	for r in res.results:
		stuff.append( r.text )
	return '<br>'.join(stuff)



'''
@app.route('/')
def hello():


	#res = client.query('1337')

	stuff = []


	the_path = "my path is=%s " % request.path
	return the_path

'''