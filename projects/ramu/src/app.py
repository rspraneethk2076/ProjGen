from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__,template_folder='D:/Downloads/genMaya/projects/project1/templates')
import logging
import traceback
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    filemode='w',  
)

app.config['SECRET_KEY'] = 'a938397f9079d5a52a74310bd2606a7b96a8986661139196'
@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            result = num1 + num2
            return render_template('add.html', result=result)
        except ValueError:
            return "Invalid input. Please enter valid numbers."
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)