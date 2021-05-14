from api import API


app = API()


@app.route('/')
def index(request, response):
    response.text = 'Hello from the INDEX page'


@app.route('/about')
def about(request, response):
    response.text = 'Hello from the ABOUT page'


@app.route('/hello/{name}')
def hello(request, response, name):
    response.text = f'Hello, {name}'


@app.route('/sum/{x:d}/{y:d}')
def sum(request, response, x, y):
    total = int(x) + int(y)
    response.text = f'{x} + {y} = {total}'
