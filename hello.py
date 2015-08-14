from flask import Flask, redirect, render_template
import os, wolframalpha, re

notnumber_pattern = re.compile(r'[^0-9]')


app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the landing page with zero!'

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/why')
def why_page():
	return "This page exists because people should stop talking about how big the deep web / dark web is."


@app.route('/random')
def why_page():
	return "This page selects a random /number page from the cache."

@app.route('/wolfram')
def wolfram():

	app_id = 'E7W676-QR2UE4PUR4'
	client = wolframalpha.Client(app_id)
	res = client.query('temperature in Washington, DC on October 3, 2012')

	stuff = []
	for r in res.results:
		stuff.append( r.text )
	return '<br>'.join(stuff)


@app.route('/<int:num>')
def page(num):
    # show the post with the given id, the id is an integer
    if num < 0:
    	return "Naturals numbers only!"

    return 'This is the page for the glorious natural number: %d' % num


## This is for doing redirection for unknown paths
@app.route('/<path:junk>')
def redirect_url(junk):
	global notnumber_pattern
	junk = re.sub( notnumber_pattern, '', junk )
	
	# if junk exists, make it an int (to remove initial 0s, else make it a zero)
	junk = int(junk) if junk else ''
	
	redirect('/%s' % junk, 302)

