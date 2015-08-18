from flask import Flask, redirect, url_for
#from flash import render_template
import os, wolframalpha, re


app = Flask(__name__)

@app.route('/')
def landing():
    return 'This is the landing page!'

@app.route('/why')
def why_page():
	return "This page exists because people should stop talking about how big the deep web / dark web is."


@app.route('/random')
def redirect_random():
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

    return 'This is the page for the glorious natural number: %d' % num




#########################################################################################################
## REDIRECTION PAGES BEYOND THIS POINT
#########################################################################################################
## This is for doing redirection for unknown paths
@app.route('/<float:num>')
def redirect_float2num(num):
	# redirect to the integer page
	return redirect( url_for('page', num=int(round(num))), 301 )


@app.route('/<path:junk>')
def redirect_path2num(junk):

	junk = re.sub( r'[^0-9]', '', junk )

	# if it's a digit, redirect to the number page.
	if junk.isdigit():
		return redirect( url_for('page', num=int(junk) ), 301 )

	# else, redirect to the frontpage
	return redirect( url_for('landing'), 301 )
	
	
	


if __name__ == '__main__':
    app.run(host='128.199.143.78', debug=True)

