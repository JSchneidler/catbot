import logging
import socketserver
from http import server
from urllib.parse import urlparse
from Camera import Camera
from json import dumps

PORT = 12345;

PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<img src="/stream" width="640" height="480" />
</body>
</html>
""";

def buildQueryObject(queryString):
    queryObject = {};
    queryString = queryString.split('&');
    for query in queryString:
        query = query.split('=');
        queryObject[query[0]] = query[1];

    return queryObject;

class StreamingHandler(server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*');
        super(StreamingHandler, self).end_headers(self);

    def do_GET(self):
        if self.path == '/stream':
            self.send_response(200);
            self.send_header('Age', 0);
            self.send_header('Cache-Control', 'no-cache, private');
            self.send_header('Pragma', 'no-cache');
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME');
            self.end_headers();
            try:
                while True:
                    with camera.output.condition:
                        camera.output.condition.wait();
                        frame = camera.output.frame;
                    self.wfile.write(b'--FRAME\r\n');
                    self.send_header('Content-Type', 'image/jpeg');
                    self.send_header('Content-Length', len(frame));
                    self.end_headers();
                    self.wfile.write(frame);
                    self.wfile.write(b'\r\n');
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e));
        elif self.path.startswith('/camera'):
            queryString = urlparse(self.path).query;

            if (queryString): response = camera.updateCamera(buildQueryObject(queryString));
            else: response = camera.getState();

            if isinstance(response, object) or isinstance(response, list):
                response = dumps(response, separators=(',',':'));
            response = response.encode('utf-8');

            self.send_response(200);
            self.send_header('Content-Type', 'text/plain');
            self.send_header('Content-Length', len(response));
            self.end_headers();
            self.wfile.write(response);
        else:
            self.send_error(404);
            self.end_headers();

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True;
    daemon_threads = True;

camera = Camera();

try:
    address = ('', PORT);
    server = StreamingServer(address, StreamingHandler);
    server.serve_forever();
finally:
    camera.close();