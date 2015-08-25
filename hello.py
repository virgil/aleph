from flask import Flask, redirect, url_for, render_template, send_from_directory
import re, random
from aleph_functions import *


#######################################################

app = Flask(__name__)


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

	junk = re.sub( r'[^0-9]', '', junk )

	# if it's a digit, redirect to the number page.
	if junk.isdigit():
		return redirect( url_for('page', num=int(junk) ), 301 )

	# else, redirect to the frontpage
	return redirect( url_for('landing'), 301 )
	
	
	


if __name__ == '__main__':
    app.run(host='128.199.143.78', passthrough_errors=True, debug=True)


