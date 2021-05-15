import pytest

from api import API


def test_basic_route_adding(api):
    @api.route('/')
    def index(request, response):
        response.text = 'YOLO'

def test_route_overlap_throws_exception(api):
    @api.route('/')
    def index(request, response):
        response.text = 'YOLO'

    with pytest.raises(AssertionError):
        @api.route('/')
        def home(request, response):
            response.text = 'YOLO'


def test_bumbo_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = 'THIS IS COOL'

    @api.route('/hey')
    def cool(request, response):
        response.text = RESPONSE_TEXT

    assert client.get('http://testserver/hey').text == RESPONSE_TEXT


def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"


def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found."


def test_class_based_handler_get(api, client):
    response_text = "this is a get request"

    @api.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text

    assert client.get("http://testserver/book").text == response_text


def test_class_based_handler_post(api, client):
    response_text = "this is a post request"

    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    assert client.post("http://testserver/book").text == response_text


def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = "yolo"

    with pytest.raises(AttributeError):
        client.get("http://testserver/book")


def test_alternative_route(api, client):
    response_text = 'Alternative way to add a route'

    def index(request, response):
        response.text = response_text

    api.add_route('/alternative', index)
    assert client.get('http://testserver/alternative').text == response_text


def test_template(api, client):
    @api.route('/html')
    def html_handler(request, response):
        context = {'title': 'Awesome Framework', 'name': 'Bumbo'}
        response.body = api.template('home.html', context=context).encode()

    response = client.get('http://testserver/html')

    assert 'text/html' in response.headers['Content-Type']
    assert 'Awesome Framework' in response.text
    assert 'Bumbo' in response.text
