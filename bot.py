from ws4py.client.threadedclient import WebSocketClient
import requests

def getIpPortAndToken():
	r = requests.post('http://m.agar.io', data='US-Atlanta\n154669603')
	print(r.text)
	rs = r.text.split('\n')
	ip = rs[0].split(':')[0]
	port = rs[0].split(':')[1]
	token = rs[1]
	return ip, port, token

class AgarClient(WebSocketClient):
    def opened(self):
       self.send('80'+self.token)

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        print(m)
    
    def setToken(self, token):
    	self.token = token

if __name__ == '__main__':
    try:
    	ip, port, token = getIpPortAndToken()
    	url = 'ws://'+ip+':'+port+'/'
    	print(url, token)
    	ws = AgarClient(url, headers=[('Origin', 'http://agar.io')])
    	if not any(x for x in [('Origin', 'http://agar.io')] if x[0].lower() == 'origin'):
    		print('adding unnecessary header')
    	print('what ws client is actually sending:')
    	
    	ws.key = token.encode()
    	print(ws.host, ws.port, ws.key.decode())
    	ws.connect()
    	ws.run_forever()
    except KeyboardInterrupt:
    	ws.close()