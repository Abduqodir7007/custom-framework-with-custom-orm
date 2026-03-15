
![Purpose](https://img.shields.io/badge/purpose-learning-blue)
![Status](https://img.shields.io/badge/status-experimental-orange)
![License](https://img.shields.io/badge/license-MIT-green)

# PyFrame

PyFrame is a custom Python web framework created for learning purposes. It is designed to help you understand the inner workings of web frameworks by providing a simple, minimal, and easy-to-read codebase.

## Features
- Minimal and easy to understand
- Custom middleware support
- Simple request/response handling
- Supports both class-based and function-based handlers
- Designed for educational use

## Installation

You can install PyFrame locally by cloning this repository and installing it in editable mode:




## Running the Project

It is recommended to use Gunicorn to run your PyFrame project for production-like environments. Install Gunicorn if you haven't already:

```bash
pip install gunicorn
```

Then run your project with:

```bash
gunicorn main:app
```

Replace `main:app` with the appropriate module and app variable if your entry point is different.


PyFrame supports both function-based and class-based handlers for defining routes.

### Function-Based Handler Example
```python
from app import App
from response import Response

app = App()

@app.route("/")
def home(request):
    return Response("Hello, World!")

if __name__ == "__main__":
    app.run()
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

if __name__ == "__main__":
    app.run()
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
