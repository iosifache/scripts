# From https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7

import http.server
import ssl
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

class Handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def main() -> None:
    if (len(sys.argv) != 4): 
        print(f"{sys.argv[0]} <crt_certificate> <pem_key> <port>")
        
        exit(1)

    certificate = sys.argv[1]
    key = sys.argv[2]
    port = int(sys.argv[3])

    logging.basicConfig(level=logging.INFO)

    server_address = ('localhost', port)

    httpd = http.server.HTTPServer(server_address, Handler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile=certificate,
                                   keyfile=key,
                                   ssl_version=ssl.PROTOCOL_TLS)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
