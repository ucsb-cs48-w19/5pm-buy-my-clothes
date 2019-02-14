from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def index_func():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    # show the form, it wasn't submitted
    return render_template('index.html')

@app.route('/accessories')
def category_func():
    return render_template('accessories.html')

@app.route('/')
def browse():
    return render_template('browse.html')

@app.route('/browse', methods=['GET', 'POST'])
def browse_func():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('browse')) 
    # show the form, it wasn't submitted
    return render_template('browse.html')

if __name__ == "__main__":
    app.run()
