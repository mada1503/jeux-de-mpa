from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Configuration des chemins
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.static_folder = STATIC_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tetris')
def tetris():
    return app.send_static_file('tetris.html')

@app.route('/subway')
def subway():
    return app.send_static_file('subway.html')

@app.route('/scores', methods=['GET', 'POST'])
def scores():
    score_file = os.path.join(app.static_folder, 'highscores.json')
    
    if request.method == 'POST':
        data = request.get_json()
        scores = {}
        try:
            with open(score_file, 'r') as f:
                scores = json.load(f)
        except:
            pass
            
        scores.update(data)
        with open(score_file, 'w') as f:
            json.dump(scores, f)
        return jsonify({'status': 'success'})
    
    try:
        with open(score_file, 'r') as f:
            scores = json.load(f)
            return jsonify(scores)
    except:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
