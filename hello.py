from flask import Flask, redirect, url_for
from flask import render_template
from flask import Markup
import os, re, json
import wolframalpha



app = Flask(__name__)

@app.route('/')
def landing():

    title = ""

    # intro text here
    intro_paragraphs = [ ]    
    paragraph = ["wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!","wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!"]


    # add code here for displaying zero

    try:
        return render_template("test.html", title=title, paragraph=paragraph)
    except Exception, e:
        return str(e)


@app.route('/why')
def why_page():


    title = "Why this site exists"
    paragraph = ["This page exists because people should stop talking about how big the deep web / dark web is."]

    pageType = 'about'

    return render_template("test.html", title=title, paragraph=paragraph, pageType=pageType)


@app.route('/random')
def redirect_random():
	return "This page selects a random /number page from the cache."


@app.route('/<int:num>')
def page(num):
    # show the post with the given id, the id is an integer
	
	# make the connection to the backend    
	app_id = 'E7W676-QR2UE4PUR4'
	params = { 'scanner': 'Integer', 'assumption': '*C.1337-_*NonNegativeDecimalInteger-' }
	client = wolframalpha.Client(app_id)
	

	res = client.query( str(num) )
	lines = []
	the_pods = [ pod for pod in res.pods ]

	for pod in the_pods:
		if pod.id == 'Property':
			for s in pod:
				if 'img' in s.children:
					lines.append( ('', img2html(s.children['img']) ) )

				elif 'plaintext' in s.children:
					lines.append( ('', s.text) )


	for pod in the_pods:
		if pod.id == 'BaseConversions':
			for s in pod:
				if 'img' in s.children:
					lines.append( ("Base conversion: %s = " % num, img2html(s.children['img'])) )

				elif 'plaintext' in s.children:
					lines.append( ("Base conversion: %s = " % num, s.text) )


		elif pod.id == 'PrimeFactorization':
			for s in pod:
				if 'img' in s.children:
					lines.append( ("Prime factors: ", img2html(s.children['img'])) )

				elif 'plaintext' in s.children:
					lines.append( ("Prime factors: ", s.text) )

	if num == 1:
		lines.append( ('',"1 is the most solipistic number.") )

	pageType = 'about'

	return render_template( "numpage.html", num=int(num), paragraph=lines )
    

def img2html( imgdict ):
	'''returns the HTML from img dictionary'''

	z = '<img src="%(src)s" alt="%(alt)s" title="%(title)s" height="%(height)s" width="%(width)s"/>' % imgdict
	return z


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
    app.run(host='128.199.143.78', passthrough_errors=True, debug=True)


