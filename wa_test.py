import wolframalpha, sys
from pprint import pprint

app_id = 'E7W676-55P6J8Q4UL'
client = wolframalpha.Client(app_id)
num = 5

try:
	#res = client.query( str(num), scanner='Integer', format='mathml', assumption='*C.1337-_*NonNegativeDecimalInteger-' )
	res = client.query( str(num), scanner='Integer', assumption='*C.1337-_*NonNegativeDecimalInteger-' )

except Exception, e:

	msg = e[0]
	if 'Account blocked' in msg or "Error 10" in msg:
		print("Account was blocked.  Lame.")
	else:
		print( "code: %s" % e[0])
	#print( "msg: %s" % e[1])

	sys.exit(1)

#res = client.query( str(num), params )

print( 'Getting new lines from Wolfram...' )

the_pods = [ pod for pod in res.pods ]

prop_pods = [ x for x in the_pods if x.id == 'Property' ]
assert len(prop_pods) == 1

prop_pod = prop_pods[0]
lines = []

def img2html( imgdict ):
	'''returns the HTML for displaying an image dictionary'''
	z = '<img src="%(src)s" alt="%(alt)s" title="%(title)s" height="%(height)s" width="%(width)s"/>' % imgdict
	return z


for spod in prop_pod:

	for spod in pod:

		if 'img' in spod.children:
			img_node_title = (spod.children['img'])['title']

			# skip the "is an (odd|even) number."
			if img_node_title.endswith('is an odd number.') or img_node_title.endswith('is an even number'):
				continue

			local_img = spod.children['img']

			#lines.append( ((''), 'dict=%s' % local_img) )					

			# this might come back False					
			if local_img:
				lines.append( ('', img2html(local_img) ) )

		elif 'plaintext' in spod.children:
			lines.append( ('', spod.text) )	

pprint( lines )

