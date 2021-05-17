from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    with open('about.txt','r') as file:
        x = file.readlines()
        l_games = x[0].split(',')
        l = len(l_games)

        return render_template('home.html',l_games=l_games, len=l)


if __name__ == '__main__':
    app.run(debug=True)
