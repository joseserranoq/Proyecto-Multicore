from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    with open('Proyecto-Multicore\\templates\game_data.txt','r',encoding="utf-8") as file:
        l_games = file.readlines()
        l = len(l_games)

        return render_template('home.html',data=l_games, len=l)


if __name__ == '__main__':
    app.run(debug=True)
