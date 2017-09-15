import json
from flask import (Flask, render_template, redirect, 
                    url_for, request, make_response)

from options import DEFAULTS

# In Flask cookies are set on response, which is different
# from other frameworks and languages. That's why we import
# make_response

app = Flask(__name__)

def get_saved_data():
    try:
        # make data into dict
        data = json.loads(request.cookies.get('character'))
    except TypeError:
        # if we don't get what we expect, return an empty dict
        data = {}
    return data

@app.route('/')
def index():
    data = get_saved_data() # get cookie information
    return render_template('index.html', saves=data) # pass data from cookie to template

# character builder
@app.route('/builder')
def builder():
    return render_template('builder.html',
                            saves=get_saved_data(),
                            options=DEFAULTS)

@app.route('/save', methods=['POST'])
def save():
    response = make_response(redirect(url_for('builder')))  
    data = get_saved_data()
    data.update(dict(request.form.items()))  
    # we call the cookie 'character' and turn value into dict 
    # cause req.form return a tuple
    # json.dumps creates a json string
    response.set_cookie('character', json.dumps(data))
    return response

app.run(debug=True, host='localhost', port=8000)