from flask import Flask, redirect, url_for, render_template, send_from_directory, make_response
import re, random
from aleph_functions import *
from functools import wraps

regex_mathmatch = re.compile( r'^[0-9\+\-*\\\^)(\ ]*$' )
regex_nummatch = re.compile( r'[^0-9]' )


#######################################################

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 4096

@app.route('/')
def landing():

    try:
        return render_template("index.html")
    except Exception, e:
        return str(e)


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

def dontcache(f):
	"""This decorator prepends Cache-Control: private"""
	@wraps(f)
	@add_response_headers({'Cache-Control': 'private'})
	def decorated_function(*args, **kwargs):
		return f(*args, **kwargs)
	return decorated_function


@app.route('/rand')
@app.route('/random')
@dontcache
def redirect_random():
	# pick a random integer between [0,99999999], and redirect there

	the_int = random.randint(0,999999999)
	return redirect( url_for('page', num=the_int), 302 )




@app.route('/<int:num>')
def page(num):
    # show the post with the given id, the id is an integer
    
	lines = get_lines_from_db(num)

	# if no dblines, try 
	if not lines:
		lines = get_lines_from_wolfram(num)

		# we got some lines, awesome.
		if lines:
			write_lines_to_db(num,lines)
		else:
			lines = [ ('' ,"We don't know anything about %d yet!  We will soon!" % num ) ]


	return render_template( "numpage.html", num=int(num), paragraph=lines, h=h(num) )


#########################################################################################################
## REDIRECTION PAGES BEYOND THIS POINT
#########################################################################################################
## This is for doing redirection for unknown paths
@app.route('/<float:num>')
def redirect_float2num(num):
	# redirect to the integer page
	return redirect( url_for('page', num=int(round(num))), 301 )



@app.route('/db/<path:filename>')
def db_static(filename):
    return send_from_directory(app.root_path + '/db/', filename)


@app.route('/<path:junk>')
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
    app.run(host='128.199.143.78', port=1337, passthrough_errors=True)


