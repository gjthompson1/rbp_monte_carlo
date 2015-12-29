from __future__ import division

# imports
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g, json, make_response
from functools import wraps
import json
import ast

app = Flask(__name__)

# pulls in configurations by looking for UPPERCASE variables
app.config.from_object('_config')


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or\
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            # session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)


@app.route('/main', methods=['GET'])
@login_required
def main():
    return render_template('app_temp.html')

@app.route('/calc', methods=['POST'])
@login_required
def api_calc():
    values = request.get_json()
    val = values.get('term', 0) if values.get('term', 0) != '' else 0
    mult_val = float(val)*12
    print mult_val
    resp = {
        'mult_val': mult_val
    }
    resp = json.dumps(resp)
    return make_response(resp)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
