from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__,template_folder='D:/Downloads/genMaya/projects/project1/templates')
app.config['SECRET_KEY'] = 'a938397f9079d5a52a74310bd2606a7b96a8986661139196'
counter = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global counter
    if request.method == 'POST':
        if request.form['action'] == 'increment':
            counter += 1
        elif request.form['action'] == 'decrement':
            counter -= 1
        elif request.form['action'] =='reset':
            counter = 0
    return render_template('index.html', counter=counter)

if __name__ == '__main__':
    app.run(debug=True)