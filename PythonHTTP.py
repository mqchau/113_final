import SimpleHTTPServer
import SocketServer
import thread
PORT = 80

def runServer():

	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

	httpd = SocketServer.TCPServer(("", PORT), Handler)

	print "serving at port", PORT
	thread.start_new_thread(httpd.serve_forever, ())
	