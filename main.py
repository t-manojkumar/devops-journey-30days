import string
import random
# What: We are importing the necessary tools from the Flask library.
# Why: Flask provides the main application object. `request` lets us see incoming data.
#      `redirect` sends the user's browser to another URL. `jsonify` creates a
#      properly formatted JSON response.
from flask import Flask, request, redirect, jsonify

# Create the Flask application instance
app = Flask(__name__)

# Our in-memory "database" from Day 3
url_mapping = {}


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(length))
    return short_code


# What: This is a "decorator". It links a URL path ('/shorten') and an HTTP
#       method (POST) to our `shorten_url` Python function.
# Why: This is how Flask knows which code to run when a user sends a POST
#      request to http://your-server/shorten
@app.route('/shorten', methods=['POST'])
def shorten_url():
    # Get the JSON data from the incoming request
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    while short_code in url_mapping:
        short_code = generate_short_code()

    url_mapping[short_code] = original_url
    
    # What: We are creating a JSON response.
    # Why: APIs communicate using structured data formats, and JSON is the most common.
    #      The '201' is the HTTP status code for "Created", which is the correct
    #      response when a new resource (our short link) is created.
    return jsonify({
        "message": "URL shortened successfully",
        "short_code": short_code,
        "short_url": request.host_url + short_code
    }), 201


# What: Another decorator. This one has a dynamic part: <short_code>.
# Why: This allows us to handle requests for any possible short code, like /aB1xZ2
#      or /zY9wQ1. Flask will pass the value from the URL into the function.
@app.route('/<short_code>', methods=['GET'])
def get_original_url(short_code):
    original_url = url_mapping.get(short_code)

    if original_url:
        # What: We are sending a browser redirect.
        # Why: This is the primary function of a URL shortener. It tells the user's
        #      browser to go to the long, original URL.
        return redirect(original_url)
    else:
        # Return a 404 Not Found error if the code doesn't exist
        return jsonify({"error": "Short code not found"}), 404