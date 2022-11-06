# Import flask
from flask import Flask

# Create a new Flask app instance
app = Flask(__name__) # Name denotes the name of the current function. 

# Create the first route
@app.route('/') # defines the starting point. '/' denots that we want to put our data at the root of our routes.

# Create hello world function
def hello_world():
    return 'Hello World'    

