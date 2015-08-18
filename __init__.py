from flask import Flask, redirect, url_for
#from flash import render_template
import os, wolframalpha, re


app = Flask(__name__)

@app.route('/')
def landing():

    title = "THE LANDING PAGE"
    paragraph = ["wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!","wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!"]

    try:
        return render_template("index.html", title=title, paragraph=paragraph)
    except Exception, e:
        return str(e)


@app.route('/why')
def why_page():


    title = "Why this site exists"
    paragraph = ["This page exists because people should stop talking about how big the deep web / dark web is."]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)


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
    app.run(host='128.199.143.78', passthrough_errors=True, debug=True)

