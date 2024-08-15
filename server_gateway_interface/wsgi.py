def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b'hello world']

# Start WSGI with the next command (unix system): gunicorn wsgi_app:app
# For the windows install waitress and use the next command (from AsyncPractice dir):
# waitress-serve --port=8000 server_gateway_interface.wsgi:app

# To check if the wsgi works:
# curl http://localhost:8000
