from flask import Flask, render_template, request, redirect, url_for
from utils.util import DotsAndBoxes

app = Flask(__name__)

game = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])
    game = DotsAndBoxes(rows, cols)
    return redirect(url_for('play_game'))

@app.route('/play_game', methods=['GET', 'POST'])
def play_game():
    global game
    if game is None:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        line_type = request.form['line_type']
        row = int(request.form['row'])
        col = int(request.form['col'])
        
        if game.is_valid_line(line_type, row, col):
            game.draw_line(line_type, row, col)
        
        if game.is_game_over():
            winner = game.get_winner()
            return render_template('game_over.html', winner=winner)
    
    return render_template('play_game.html', game=game)

if __name__ == '__main__':
    app.run(debug=True)