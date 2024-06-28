import flask
from flask import Flask, request, jsonify, render_template, redirect, make_response, send_file
import backend
from neuralnetworkforsite import neuralnet

app = flask.Flask(__name__)
HOST = 5000

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    if 'username' not in request.cookies:
        return redirect('/login')
    
    resp = make_response(render_template('home.html'))
    return resp

@app.route('/makereview')
def makereview():
    if 'username' not in request.cookies:
        return redirect('/login')
    resp = make_response(render_template('review.html'))
    return resp

@app.route('/reviewresult', methods=['POST'])
def review():
    if 'username' not in request.cookies:
        return redirect('/login')
    data = request.form["content"]
    print(data)
    prediction = net.predict_sentiment(data)
    return render_template('postreview.html', review=round(prediction*100, 3))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in request.cookies:
        return redirect('/home')
    
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        if 'loginsubmit' in request.form:
            
            if(request.form['name'] != '' and request.form['password'] != '' and request.form['loginsubmit'] != ''):
                if backend.login(request.form['name'], request.form['password']) == True:
                    resp = make_response(redirect('/home'))
                    resp.set_cookie('username', request.form['name'])
                    return resp
                else:
                    return "<html><body><h1>Error 3, password incorrect, please try again </h1></body></html>"
            
        elif(request.form['name'] != '' and request.form['password'] != '' and request.form['new'] != ''):
            
            if len(request.form['password']) < 8 or len(request.form['password']) > 20 or len(request.form['name']) > 20:
                return "<html><body><h1>Error 4, password too long or short, please try again, you need 8 characters </h1></body></html>"
            backend.createuser(request.form['name'], request.form['password'])
            resp = make_response(redirect('/home'))
            resp.set_cookie('username', request.form['name'])
            return resp
        else:
            return "<html><body><h1>Error, username or password is empty, please try again </h1></body></html>"

@app.route('/addmovie', methods=['GET', 'POST'])
def addmovie():
    if 'username' not in request.cookies:
        return redirect('/login')
    
    if request.method == 'GET':
        return render_template('addmovie.html')
    
    if request.method == 'POST':
        pass #TODO

@app.errorhandler(404)
def page_not_found(e):
    return render_template('placeholder.html'), 404

if __name__ == '__main__':
    net = neuralnet('imdb_model.keras')
    backend.initialize()
    print(f"✅ Flask server running at http://127.0.0.1:{HOST} ✅")
    app.run(debug=True, port=HOST)