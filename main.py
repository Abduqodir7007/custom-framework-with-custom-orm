from app import PyFramework

app = PyFramework()


@app.router('/home/{name}')
def home(request, response, name):
    response.text = f"Hello {name}"

@app.router("/books/")
class Books:

    def get(self, request, response):
        response.text = "Getting boooks\n"

    def post(self, request, response):
        response.text = "Created a book\n   "
