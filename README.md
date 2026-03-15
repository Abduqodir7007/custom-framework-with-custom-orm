
![Purpose](https://img.shields.io/badge/purpose-learning-blue)
![Status](https://img.shields.io/badge/status-experimental-orange)

# pyframex7

pyframex7 is a custom Python web framework created for learning purposes. 

## Features
- Minimal and easy to understand
- Custom middleware support
- Simple request/response handling
- Supports both class-based and function-based handlers
- Designed for educational use

## Installation

pyframex7 is available on PyPI and can be installed with:

```bash
pip install pyframex7
```

### Function-Based Handler Example
```python
from app import App
from response import Response

app = App()

@app.route("/")
def home(request):
    return Response("Hello, World!")

```

### Class-Based Handler Example
```python
from app import App, Handler
from response import Response

app = App()

class HelloHandler(Handler):
    def get(self, request):
        return Response("Hello from class-based handler!")

app.add_route("/hello", HelloHandler)
```

- Define your routes using the `@app.route` decorator for function-based handlers or `app.add_route` for class-based handlers.
- Return a `Response` object from your route handlers.
- Run your application with `app.run()`.
    app.run()
```

- Define your routes using the `@app.route` decorator.
- Return a `Response` object from your route handlers.
- Run your application with `app.run()`.


## Use Cases
- Learning how web frameworks work
- Experimenting with middleware and routing
- Building simple web applications for educational purposes

## License
This project is for learning and educational purposes only.
