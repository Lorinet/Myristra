from http.server import BaseHTTPRequestHandler, HTTPServer
import mycommands
import myio
import re

hostname = "localhost"
port = 1030

class MyristraServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Myristra Print Server</title></head><body>", "utf-8"))
        params = re.split(r'(?<!\\)/', self.path)[1:]
        for i in range(len(params)):
            params[i] = params[i].replace("\\/", "/").replace("&nbsp;", " ").replace("&lsquo;", "'").replace("&ldquo;", "\"").replace("%20", " ")
        if params[0] == 'favicon.ico':
            return
        print(params)
        try:
            getattr(mycommands, params[1])(int(params[0]), *params[2:])
            self.wfile.write(bytes("Command executed", "utf-8"))
        except IndexError:
            self.wfile.write(bytes("Cannot communicate with device", "utf-8"))
        except AttributeError:
            self.wfile.write(bytes("Invalid command: " + str(params), "utf-8"))
            pass
        self.wfile.write(bytes("</body></html>", "utf-8"))

def serve():
    webserver = HTTPServer((hostname, port), MyristraServer)
    print("Print server started: http://" + hostname + ":" + str(port))
    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass
    webserver.server_close()
    print("Print server stopped.")
