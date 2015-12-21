import asyncio
import websockets
import requests

def getIpPortAndToken():
	r = requests.post('http://m.agar.io', data='US-Atlanta\n154669603')
	rs = r.text.split('\n')
	ip = rs[0].split(':')[0]
	port = rs[0].split(':')[1]
	token = rs[1]
	return ip, port, token

@asyncio.coroutine
def hello():
	ip, port, token = getIpPortAndToken()
	print('Attempting to connect to: '+'ws://'+ip+':'+port+'/')
	websocket = yield from websockets.connect('ws://'+ip+':'+port+'/', extra_headers={'Origin':'http://agar.io'})
	yield from websocket.send('80'+token)
	while True:
		r = yield from websocket.recv()
		print(r)

asyncio.get_event_loop().run_until_complete(hello())