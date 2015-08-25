import wolframalpha, md5
import os, json, urllib
from urlparse import urlparse

h = lambda x: md5.new(str(x)).hexdigest()


def num2path( num ):
	'''takes the num, returns the database path'''

	myhash = h(num)
	first, second = myhash[0], myhash[1]
	dname = "db/%s/%s/%s/" % ( first, second, myhash )

	# if the path doesn't exist, create it.
	if not os.path.exists(dname):
		os.makedirs( dname )

	return dname


def next_img_fname(num):
	'''returns the next available digit for the number'''
	dname = num2path(num)

	digit_files = [ int(x) for x in os.listdir( dname ) if x.isdigit() ]

	max_digit = max(digit_files) if digit_files else 0

	next_digit = max_digit + 1

	return "%s%s" % (dname, next_digit)



def write_lines_to_db( num, lines ):
	'''write these lines into the database overwriting any previous num'''

	my_hash, dname = h(num), num2path(num)

	# if the directory doesn't exist, make it
	if not os.path.exists(dname):
		os.makedirs( dname )

	fname = '%s/%s.json' % (dname, my_hash)
    # now write it
	with open(fname,'w') as f:
		json.dump(lines, f, sort_keys=True)


def get_lines_from_db(num):
	'''gets all lines about num from mysql database'''


	my_hash = h(num)
	dname = num2path(num)

	fname = '%s/%s.json' % (dname, my_hash)

	# if the directory doesn't exist, make it
	if not os.path.isfile( fname ):
		return None


	with open(fname, 'r') as f:
		return json.load(f)

	return None


def write_lines_to_db( num, lines ):
	'''write these lines into the database overwriting any previous num'''

	my_hash, dname = h(num), num2path(num)

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
					#lines.append( ('', 'adding stuff to dict' ) )
					#lines.append( ((''), 'dict=%s' % s.children['img']) )

					local_img = wolframdict2localdict( s.children['img'], num )

					#lines.append( ((''), 'dict=%s' % local_img) )					

					# this might come back False					
					if local_img:
						lines.append( ('', img2html(local_img) ) )

				elif 'plaintext' in s.children:
					lines.append( ('', s.text) )

	
	for pod in the_pods:
		if pod.id == 'BaseConversions':
			for s in pod:
				if 'img' in s.children:
					local_img = wolframdict2localdict( s.children['img'], num )

					# this might come back False
					if local_img:
						lines.append( ("Binary conversion: %s = " % num, img2html(local_img)) )

				elif 'plaintext' in s.children:
					lines.append( ("Base conversion: %s = " % num, s.text) )


		elif pod.id == 'PrimeFactorization':
			for s in pod:
				if 'img' in s.children:
					local_img = wolframdict2localdict( s.children['img'], num )

					# this might come back False
					if local_img:
						lines.append( ("Prime factors: ", img2html(local_img)) )

				elif 'plaintext' in s.children:
					lines.append( ("Prime factors: ", s.text) )

	if num == 1:
		lines.append( ('',"1 is NOT prime.  Nor is it composite.") )
		lines.append( ('',"1 is the most solipistic number.") )

	elif num == 0:
		lines.append( ('By definition: ', '0! = 1') )
		lines.append( ('', "There remains some debate as to when zero was discovered.  But most recent science put the origin in Cambodia around 680 Common Era.") )
		lines.append( ('', "0<sup>0</sup> = 1") )
		lines.append( ('', 'In Roman numerals, 0 is "nulla".') )

	return lines


def get_lines_from_db(num):
	'''gets all lines about num from mysql database'''


	my_hash = h(num)
	dname = num2path(num)

	fname = '%s/%s.json' % (dname, my_hash)

	# if the directory doesn't exist, make it
	if not os.path.isfile( fname ):
		return None


	with open(fname, 'r') as f:
		return json.load(f)

	return None


def wolframdict2localdict( imgdict, num ):
	'''downloads the wolfram image to local file, returns the a dict pointing to the local image'''

	# derive the directory from num
	relative_http_path = '/' + next_img_fname(num)
	absolute_local_path = os.getcwd() + relative_http_path


	try:

		img_url = imgdict['src']
		image_on_web = urllib.urlopen(img_url)

		if image_on_web.headers.maintype == 'image':
			buf = image_on_web.read()
			downloaded_image = file(absolute_local_path, "wb")
			downloaded_image.write(buf)
			downloaded_image.close()
			image_on_web.close()
		else:
			return False

	except:
		return False

	imgdict['src'] = relative_http_path
	
	return imgdict


def img2html( imgdict ):
	'''returns the HTML for displaying an image dictionary'''
	z = '<img src="%(src)s" alt="%(alt)s" title="%(title)s" height="%(height)s" width="%(width)s"/>' % imgdict
	return z
