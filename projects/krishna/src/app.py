from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__,template_folder='')
app.config['SECRET_KEY'] = 'a938397f9079d5a52a74310bd2606a7b96a8986661139196'
counter = 0

import logging
import traceback
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    filemode='w',  
)

@app.errorhandler(Exception)
def handle_error(e):

    app.logger.error(f"Exception occurred: \n{traceback.format_exc()}")

    return "Internal Server Error", 500
app = Flask(__name__,template_folder='')
app.config['SECRET_KEY'] = 'a938397f9079d5a52a74310bd2606a7b96a8986661139196'
counter = 0

@app.route('/', methods=['GET', 'POST'])
def add():
    global counter
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            result = num1 + num2
            counter += 1
            return render_template('add.html', result=result, counter=counter)
        except ValueError:
            return render_template('add.html', error='Invalid input')
    return render_template('add.html', counter=counter)

if __name__ == '__main__':
    app.run(debug=True)