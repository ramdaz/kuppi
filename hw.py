from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

run(host='127.0.0.1', port=8080, debug=True)
