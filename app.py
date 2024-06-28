import flask
from flask import Flask, request, jsonify, render_template, redirect, make_response, send_file
import backend
from neuralnetworkforsite import neuralnet

app = flask.Flask(__name__)
HOST = 5000

@app.route('/makereview')
def index():
    resp = make_response(render_template('review.html'))
    return resp
@app.route('/reviewresult', methods=['POST'])
def review():
    data = request.form["content"]
    print(data)
    prediction = net.predict_sentiment(data)
    return render_template('postreview.html', review=round(prediction*100, 3))

if __name__ == '__main__':
    net = neuralnet('imdb_model.keras')
    print(f"✅ Flask server running at http://127.0.0.1:{HOST} ✅")
    app.run(debug=True, port=HOST)