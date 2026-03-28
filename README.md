
![Purpose](https://img.shields.io/badge/purpose-learning-blue)
![Status](https://img.shields.io/badge/status-experimental-orange)

# pyframex7

Pyframex7 is a custom Python web framework created for learning purposes. 

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


## Simple Use Cases

### 1. Function-Based Handler Example
```python
from pyframe.app import PyFramework
from pyframe.response import Response

app = PyFramework()

# Function-based route handler
@app.router("/hello/{name}")
def hello(request, response, name):
    # Set plain text response
    response.text = f"Hello, {name}!"

# To run: Use a WSGI server like gunicorn 
# Example: gunicorn main:app
```

### 2. Class-Based Handler Example
```python
from pyframe.app import PyFramework

app = PyFramework()

# Class-based handler for /greet/
@app.router("/greet/")
class Greet:
    def get(self, request, response):
        response.text = "Greetings from a class-based handler!"

    def post(self, request, response):
        # You can access POST data from request.params
        name = request.params.get("name", "Anonymous")
        response.text = f"Posted by {name}"
```

### 3. Using Middleware
```python
from pyframe.middleware import Middleware

class LoggingMiddleware(Middleware):
    def process_request(self, request):
        print(f"Request path: {request.path}")

    def process_response(self, request, response):
        print(f"Response status: {response.status_code}")

# Add middleware to the app
app.add_middleware(LoggingMiddleware)
```



### 4. Simple ORM Model and Usage
```python
from pyframe.orm import Table, Column, Database

# Define a User model/table
class User(Table):
    id = Column(int)
    name = Column(str)
    age = Column(int)

# Create a database instance (in-memory for demo)
db = Database(":memory:")

# Register the model and create the table
db.create(User)

# Now the User model is bound to the database

# Create and save multiple users
user1 = User(id=1, name="Alice", age=30)
user2 = User(id=2, name="Bob", age=25)
user3 = User(id=3, name="Charlie", age=35)
user1.save()
user2.save()
user3.save()


# Fetch all users (using Manager)
users = User.objects.all()
print("All users:", users)

# Get a single user by field (raises if not found or multiple found)
try:
    alice = User.objects.get(name="Alice")
    print("Get Alice:", alice)
except Exception as e:
    print(e)

# Filter users by age
filtered = User.objects.filter(age=25).all()
print("Users with age=25:", filtered)

# Delete a user by id
User.objects.delete(id=2)
print("After deleting Bob:", User.objects.all())

# Drop the table (removes all data and table)
db.drop(User)
```

---


#### Comments
- The framework supports both function-based and class-based route handlers.
- Middleware can be added for logging, authentication, etc.
- The ORM allows you to define models as Python classes and map them to SQL tables.
- Each model gets an `objects` attribute (a Manager) for querying, filtering, and deleting records in a Pythonic way (e.g., `User.objects.all()`, `User.objects.get(...)`, `User.objects.filter(...)`).
- You must bind a database connection to your model before saving data.
- Table creation and data insertion are handled via class methods and instance methods.

---


## Use Cases
- Learning how web frameworks work
- Experimenting with middleware and routing
- Building simple web applications for educational purposes

## License
This project is for learning and educational purposes only.
