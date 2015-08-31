from flask import Flask, redirect, url_for, render_template, send_from_directory, make_response, request
import re, random
from aleph_functions import *
from functools import wraps
from os.path import isfile
from sys import exit
import copy

regex_mathmatch = re.compile( r'^[0-9\+\-*\\\^)(\ ]*$' )
regex_nummatch = re.compile( r'[^0-9]' )


#######################################################

app = Flask(__name__)

######################################################################
app.config['MAX_CONTENT_LENGTH'] = 4096
HOST_IP = '0.0.0.0'
HTTP_PORT = 1337
DAYS_TO_CACHE = 4

# can set this here or in file 'wolfram.apikey'
WOLFRAM_APIKEY = None
######################################################################
def add_response_headers(headers={}):
	"""This decorator adds the headers passed in to the response"""
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			resp = make_response(f(*args, **kwargs))
			h = resp.headers
			for header, value in headers.items():
				h[header] = value
			return resp
		return decorated_function
	return decorator


def show_req_headers(f):
	"""This decorator prepends the HTTP request headers"""
	@wraps(f)

	new_headers = {}
	for key, value in request.headers.items():
		new_key = "x-req-%s" % key
		new_headers[new_key] = value
	@add_response_headers( new_headers )
	def decorated_function(*args, **kwargs):
		return f(*args, **kwargs)
	return decorated_function


def dontcache(f):
	"""This decorator prepends Cache-Control: private"""
	@wraps(f)
	@add_response_headers({'Cache-Control': 'private', 'X-testurl': 'http://7g5v3hvx5x2zkoqe.onion/555' } )
	def decorated_function(*args, **kwargs):
		return f(*args, **kwargs)
	return decorated_function


def cacheit(f):
	"""This decorator prepends Cache-Control header for caching for 3 days"""
	@wraps(f)
	@add_response_headers({'Cache-Control': 'max-age=%d' % (86400 * DAYS_TO_CACHE) })
	def decorated_function(*args, **kwargs):
		return f(*args, **kwargs)
	return decorated_function



@app.route('/')
@cacheit
def landing():

    try:
        return render_template("index.html")
    except Exception, e:
        return str(e)


@app.route('/rand')
@app.route('/random')
@dontcache
@show_req_headers
def redirect_random():

	the_int = random.randint(0,999999999)
	return redirect( "/%s" % (the_int), 302 )




@app.route('/<int:num>')
@cacheit
def page(num):
    # show the post with the given id, the id is an integer
    
	lines = get_lines_from_db(num)

	# if no dblines, try 
	if not lines:
		lines = []
		#lines.append( ('', 'getting from wolfram...' ) )

		try:
			#lines.append( ('', 'oh hai!') )
			lines = get_lines_from_wolfram(num, WOLFRAM_APIKEY)

			
			# we got some lines, awesome.
			if lines:
				write_lines_to_db(num,lines)
			else:
				lines = [ ('' ,"We don't know anything about %d yet!  We will soon!" % num ) ]
			

		except ValueError, e:
			lines = [ ('' ,"Backend Error: %s" % e ) ]


	return render_template( "numpage.html", num=int(num), paragraph=lines, h=h(num) )


#########################################################################################################
## REDIRECTION PAGES BEYOND THIS POINT
#########################################################################################################
## This is for doing redirection for unknown paths
@app.route('/<float:num>')
@cacheit
def redirect_float2num(num):
	# redirect to the integer page
	return redirect( url_for('page', num=int(round(num))), 301 )



@app.route('/db/<path:filename>')
@cacheit
def db_static(filename):
    return send_from_directory(app.root_path + '/db/', filename)


@app.route('/<path:junk>')
@cacheit
def redirect_path2num(junk):

	z = ''

	# if this junk only contains math...
	if re.match( regex_mathmatch, junk):

		z = junk.replace('^','**').strip()

		try:
			z = str(eval(z, {'__builtins__': None}))

		except:
			pass

	# if it's a digit, redirect to the number page.
	z = re.sub( regex_nummatch, '', z )

	if z.isdigit():
		return redirect( url_for('page', num=int(z) ), 301 )

	# else, redirect to the frontpage
	return redirect( url_for('landing'), 301 )



if __name__ == '__main__':

	# uead the APIKEY from wolfram.apikey
	if WOLFRAM_APIKEY is None:

		if not isfile('wolfram.apikey'):
			print("You must specify the key in file wolfram.apikey or specify the WOLFRAM_APIKEY in app.py")
			exit(1)

		assert isfile('wolfram.apikey') 

		with open('wolfram.apikey','r') as f:
			WOLFRAM_APIKEY = f.read().strip()


	if not WOLFRAM_APIKEY:
		print "Wolfram API key was empty.  Cannot start."
		exit(1)

	print("Running with wolfram key='%s'" % WOLFRAM_APIKEY )
	app.run(host=HOST_IP, port=HTTP_PORT, passthrough_errors=True)


