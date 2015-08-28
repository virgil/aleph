import wolframalpha, sys

app_id = 'E7W676-QR2UE4PUR4'
client = wolframalpha.Client(app_id)
num = 5

try:
	res = client.query( str(num), scanner='Integer', format='mathml', assumption='*C.1337-_*NonNegativeDecimalInteger-' )

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

for spod in prop_pod:

	if 'mathml' in spod.children:
		print( "Found mathml in spod.children!" )
		
		the_math = spod.flatten('mathml/')
		#the_math = spod.flatten('/mathml/math/node()')

		the_math = the_math.replace('<mtext>','<mspace/><mtext>')
		the_math = the_math.replace('</mtext>','</mtext><mspace/>')

		print( "the_math=%s" % the_math )
