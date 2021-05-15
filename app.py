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


@app.route('/book')
class BooksResource:

    def get(self, request, response):
        response.text = 'Books Page'

    def post(self, request, response):
        response.text = 'Endpoint to create a book'


def handler01(request, response):
    response.text = 'YOLO 01'


def handler02(request, response):
    response.text = 'YOLO 02'


app.add_route('/yolo_01', handler01)
app.add_route('/yolo_02', handler02)


@app.route('/home')
def home(request, response):
    context = {'title': 'Awesome Framework', 'name': 'Bumbo'}
    response.body = app.template('home.html', context=context).encode()
