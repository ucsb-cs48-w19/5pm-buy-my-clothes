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

@app.route('/')
def accessories():
    return render_template('accessories.html')

@app.route('/accessories', methods=['GET', 'POST'])
def accessories_func():
    if request.method == 'POST':
        # do stuff when the form is submitted                                                              
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('accessories'))
    return render_template('accessories.html')

@app.route('/')
def bags():
    return render_template('bags.html')

@app.route('/')
def coatsAndJackets():
    return render_template('coats-and-jackets.html')

@app.route('/')
def dresses():
    return render_template('dresses.html')

@app.route('/dresses', methods=['GET', 'POST'])
def dresses_func():
    if request.method == 'POST':
        # do stuff when the form is submitted                                                                         
        # redirect to end the POST handling                                                                            
        # the redirect can be to the same route or somewhere else                                              
        return redirect(url_for('dresses'))
    return render_template('dresses.html')

@app.route('/')
def jeans():
    return render_template('jeans.html')

@app.route('/')
def jewelry():
    return render_template('jewelry.html')

@app.route('/')
def mensAccessories():
    return render_template('mens-accessories.html')

@app.route('/')
def mensCoatsAndJackets():
    return render_template('mens-coats-and-jackets.html')

@app.route('/')
def mensHats():
    return render_template('mens-hats.html')

@app.route('/')
def mensJeans():
    return render_template('mens-jeans.html')

@app.route('/')
def mensPants():
    return render_template('mens-pants.html')

@app.route('/')
def mensShirts():
    return render_template('mens-Shirts.html')

@app.route('/')
def mensShoes():
    return render_template('mens-shoes.html')

@app.route('/')
def mensShorts():
    return render_template('mens-Shorts.html')

@app.route('/')
def mensSweatersAndSweatshirts():
    return render_template('mens-sweaters-and-sweatshirts.html')

@app.route('/')
def mensSwimwear():
    return render_template('mens-swimwear.html')

@app.route('/')
def mensTshirts():
    return render_template('mens-tshirts.html')

@app.route('/')
def pants():
    return render_template('pants.html')

@app.route('/')
def rompersAndJumpsuits():
    return render_template('rompers-and-jumpsuits.html')

@app.route('/')
def shirtsAndBlouses():
    return render_template('shirts-and-blouses.html')

@app.route('/')
def shoes():
    return render_template('shoes.html')

@app.route('/')
def shorts():
    return render_template('shorts.html')

@app.route('/')
def skirts():
    return render_template('skirts.html')

@app.route('/')
def sweatersAndCardigans():
    return render_template('sweaters-and-cardigans.html')

@app.route('/')
def swimwear():
    return render_template('swimwear.html')

@app.route('/')
def tshirtsAndTanks():
    return render_template('tshirts-and-tanks.html')

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
