import flask
from flask import Flask, request, jsonify, render_template, redirect, make_response, send_file
import backend
from neuralnetworkforsite import neuralnet
import base64

app = flask.Flask(__name__)
HOST = 5000

@app.route('/')
def index():
    return redirect('/home')

@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('username', '', expires=0)
    return resp

@app.route('/home')
def home():
    if 'username' not in request.cookies:
        return redirect('/login')
    
    resp = make_response(render_template('home.html', movies=backend.getmovies()))
    return resp

@app.route('/movies/<int:movie_id>')
def movie(movie_id):
    if 'username' not in request.cookies:
        return redirect('/login')
    
    movie = backend.getmovie(movie_id)
    reviews = backend.getreviews(movie_id)
    return render_template('movie.html', movie=movie, reviews=reviews)

@app.route('/movies/<int:movie_id>/makereview', methods=['GET', 'POST'])
def makereviewform(movie_id):
    if 'username' not in request.cookies:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('review.html', movie_id=movie_id)
    if request.method == 'POST':
        data = request.form["content"]
        score = net.predict_sentiment(data)
        prediction = round(score*100, 3)
        backend.addreview(movie_id, backend.getuserid(request.cookies['username']), data, prediction)
        return redirect(f'/movies/{movie_id}')

@app.route("/users/<int:user_id>")
def userprofile(user_id):
    if 'username' not in request.cookies:
        return redirect('/login')
    return render_template('profile.html', user=backend.getuser(user_id), reviews = backend.getuserreviews(user_id))

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
        content = request.form['text']
        photo = request.files['image']
        
        photo_b64 = base64.b64encode(photo.read()).decode('utf-8')
        backend.addmovie(content, photo_b64)
        resp = make_response(redirect('/home'))
        return redirect('/home')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('placeholder.html'), 404

if __name__ == '__main__':
    net = neuralnet('imdb_model.keras')
    backend.initialize()
    print(f"✅ Flask server running at http://127.0.0.1:{HOST} ✅")
    app.run(debug=True, port=HOST)