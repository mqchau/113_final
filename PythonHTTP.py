import SimpleHTTPServer
import SocketServer
import threading
PORT = 80



def runServer():

	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

	httpd = SocketServer.TCPServer(("", PORT), Handler)

	print "serving at port", PORT
	server_thread = threading.Thread(target=httpd.serve_forever)
	server_thread.start()
	return server_thread
	
if __name__ == "__main__":
	new_thread = runServer()
	print "Hello world"
	new_thread.join()