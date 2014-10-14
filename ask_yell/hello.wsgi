def application(environ, start_response):
    status = '200 OK' 
    output = 'Hello world!!!'

    response_headers = [('Content-type', 'text/html; charset=utf-8'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output] 
