import wolframalpha
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
	app_id = 'E7W676-QR2UE4PUR4'
	client = wolframalpha.Client(app_id)
	res = client.query('temperature in Washington, DC on October 3, 2012')

	#res = client.query('1337')

	stuff = []
	for r in res.results:
		stuff.append( r.text )
	return '<br>'.join(stuff)


