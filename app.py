from wsgiref.simple_server import make_server
import urllib.parse

# Storing messages in memory (not persistent)
messages = []

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    if environ['PATH_INFO'] == '/':
        return [open('index.html', 'rb').read()]
    elif environ['PATH_INFO'] == '/chat':
        if environ['REQUEST_METHOD'] == 'POST':
            # Handling incoming messages
            try:
                content_length = int(environ.get('CONTENT_LENGTH', 0))
                post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
                message = urllib.parse.parse_qs(post_data)['message'][0]
                messages.append(message)
                return [b"Message sent successfully"]
            except KeyError:
                return [b"No message sent"]

        # Serving messages to the client
        elif environ['REQUEST_METHOD'] == 'GET':
            response_body = '\n'.join(messages[-1:]).encode('utf-8')
            return [response_body]

    return [b"Not Found"]

if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
