from __future__ import division

# imports
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g, json, make_response
from functools import wraps
import json
import finance as fin
import numpy as np
import random
import ast
import matplotlib.pyplot as plt

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
    num_loans = int(values.get('num_loans',1000) if values.get('num_loans', 1000) != '' else 1000)
    int_rate = float(values.get('int_rate',1000) if values.get('int_rate', 1000) != '' else 1000)
    loan_amount = float(values.get('loan_amount',1000) if values.get('loan_amount', 1000) != '' else 1000)
    term = int(values.get('term',1000) if values.get('term', 1000) != '' else 1000)
    pd = float(values.get('pd',1000) if values.get('pd', 1000) != '' else 1000)
    shape = float(values.get('shape',2) if values.get('shape', 2) != '' else 2)

    # num_loans = 1000
    # int_rate = 10
    # loan_amount = 100000
    # term = 36
    # pd = 0.1
    # shape = 2

    num_good = int((1-pd)*num_loans)
    weib_dist = np.random.weibull(shape,50000)
    weib_dist_nrom = weib_dist/np.max(weib_dist)*term
    # plt.hist(weib_dist_nrom)
    # plt.show()

    cashflow_array = []
    x = 0
    while x < num_good:
        row = {}
        row[x] = np.array([-loan_amount] + [fin.payment_amortized(loan_amount,int_rate,term)]*term)
        cashflow_array.append(row)
        x+=1
    while x < num_loans:
        row = {}
        DT = int(np.round(random.choice(weib_dist_nrom)))
        if DT == 0:
            row[x] = np.array([-loan_amount] + [0]*(term))
        else:
            row[x] = np.array([-loan_amount] + [fin.payment_amortized(loan_amount,int_rate,term)]*(DT-1) + [0]*(term-(DT-1)))
        cashflow_array.append(row)
        x+=1

    loss = 0
    for i in range(num_good,num_loans):
        loss += sum(cashflow_array[i][i])
    LGD = abs(loss/((num_loans-num_good)*loan_amount))

    cashflow_sum = [0]*(term+1)
    for i in range(0,len(cashflow_array)):
        cashflow_sum = np.add(cashflow_sum,cashflow_array[i][i])

    RAR = fin.IRR(cashflow_sum)
    rate_cash = fin.risk_adj_rate(loan_amount,term,pd,LGD,RAR)

    mult_val = RAR
    print mult_val
    resp = {
        'mult_val': mult_val,
        'rate_cash':rate_cash,
        'LGD':LGD,
        'RAR':RAR
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
