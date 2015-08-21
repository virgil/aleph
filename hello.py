from flask import Flask, redirect, url_for, render_template
import os, re, json
import wolframalpha, md5, random
#from flask.ext.mysql import MySQL

app = Flask(__name__)

# MySQL configurations
md5.new('0').hexdigest()

h = lambda x: md5.new(str(x)).hexdigest()

@app.route('/')
@app.route('/about')
def landing():

    try:
        return render_template("index.html")
    except Exception, e:
        return str(e)




 

@app.route('/random')
def redirect_random():
	# pick a random integer between [0,99999999], and redirect there

	the_int = random.randint(0,99999999)
	return redirect( url_for('page', num=the_int), 302 )


def get_lines_from_db(num):
	'''gets all lines about num from mysql database'''


	my_hash = h(num)
	fname = 'db/%s/%s/%s.json' % (my_hash[0], my_hash[1], my_hash)

	# if the directory doesn't exist, make it
	if not os.path.isfile( fname ):
		return None


	with open(fname, 'r') as f:
		return json.load(f)

	return None


def write_lines_to_db( num, lines ):
	'''write these lines into the database overwriting any previous num'''

	my_hash = h(num)
	dname = 'db/%s/%s' % (my_hash[0], my_hash[1])

	# if the directory doesn't exist, make it
	if not os.path.exists(dname):
		os.makedirs( dname )

	fname = '%s/%s.json' % (dname, my_hash)
    # now write it
	with open(fname,'w') as f:
		json.dump(lines, f, sort_keys=True)

	

def get_lines_from_wolfram( num ):
	'''get all of the lines about num from wolframalpha'''

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
		lines.append( ('',"1 is NOT prime.  Nor is it composite.") )
		lines.append( ('',"1 is the most solipistic number.") )

	elif num == 0:
		lines.append( 'By definition: ', '0! = 1')

	return lines	

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
			lines = ["We don't know anything about %d yet!  We will soon!" % num]

	return render_template( "numpage.html", num=int(num), paragraph=lines, h=h(num) )
    

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


