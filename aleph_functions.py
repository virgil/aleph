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

	

def get_lines_from_wolfram( num, app_id ):
	'''get all of the lines about num from wolframalpha'''

	lines = []

	lines.append( ('wolfram id:', app_id) )

	# make the connection to the backend
	client = wolframalpha.Client(app_id)

	return lines
	
	try:	
		res = client.query( str(num), scanner='Integer', assumption='*C.1337-_*NonNegativeDecimalInteger-' )

		the_pods = [ pod for pod in res.pods ]

		for pod in the_pods:
			if pod.id == 'Property':

				for spod in pod:

					# remains of an attempt to make MathML work.  Eventually gave up.  Images it is!
					if 'mathml' in spod.children:
						the_math = spod.flatten('mathml/')
						
						the_math = the_math.replace('<mtext>','<mspace depth="0.5ex" height="0.5ex" width="1ex"/></mspace><mtext>')
						the_math = the_math.replace('</mtext>','</mtext><mspace depth="0.5ex" height="0.5ex" width="1ex"></mspace>')

						lines.append( ('', the_math) )

					elif 'img' in spod.children:
						img_node_title = (spod.children['img'])['title']

						# skip the "is an (odd|even) number."
						if img_node_title.endswith('is an odd number.') or img_node_title.endswith('is an even number.'):
							continue

						local_img = wolframdict2localdict( spod.children['img'], num )

						#lines.append( ((''), 'dict=%s' % local_img) )					

						# this might come back False					
						if local_img:
							lines.append( ('', img2html(local_img) ) )

					elif 'plaintext' in spod.children:
						lines.append( ('', spod.text) )

			'''
			elif pod.id == 'PrimeFactorization':
				for spod in pod:

					if 'mathml' in spod.children:
						lines.append( ('', "Found mathml!") )
						the_math = spod.flatten('mathml/')
						lines.append( ('', the_math) )

					elif 'img' in spod.children:
						img_node_title = (spod.children['img'])['title']

						# if this is a prime number, just add the raw text
						if 'is a prime number' in img_node_title:
							lines.append( ('', "%s is a prime number." % num) )

						# print the image
						else:
							local_img = wolframdict2localdict( spod.children['img'], num )

							# this might come back False
							if local_img:
								lines.append( ("Prime factors: ", img2html(local_img)) )

					elif 'plaintext' in spod.children:
						lines.append( ("Prime factors: ", spod.text) )
			'''
	# there was some error getting information from wolfram alpha
	except Exception, e:
		
		if 'Account blocked' in e[0] or "Error 10" in e[0]:
			raise ValueError, "Error 10"
		
		# propogate the exception upwards
		raise e
	

	if num == 1:
		lines.append( ('',"1 is NOT prime.  Nor is it composite.") )
		lines.append( ('',"1 is the most solipistic number.") )

	elif num == 0:
		lines.append( ('By definition: ', '0! = 1.') )
		lines.append( ('', "There remains some debate as to when zero was discovered.  But most recent science put the origin in Cambodia around 680 Common Era.") )
		#lines.append( ('By definition: ', "0<sup>0</sup> = 1.") )
		lines.append( ('', 'In Roman numerals, 0 is "nulla".') )


	# print the base conversions
	base2 = str(bin(num))[2:]
	lines.append( ('In binary: ', base2) )
	lines.append( ('In hexadecimal: ', str("%x" % num)) )

	return lines




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

